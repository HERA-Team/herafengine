#!/usr/bin/env python
import redis
import time
import json
import argparse
import os
import datetime
import socket
from subprocess import Popen, PIPE
from hera_corr_f import HeraCorrelator, __version__, __package__


def create_status(r, command, command_time, status, **kwargs):
    command_status = {
        "command": command,
        "time": command_time,
        "args": json.dumps(kwargs),
        "status": status,
        "update_time": time.time(),
    }
    # bool(empty dict) is false.
    # If it is not empy, clear out the status dict from last command
    if bool(r.hgetall("corr:cmd_status")):
        r.hdel("corr:cmd_status", *r.hkeys("corr:cmd_status"))

    r.hmset("corr:cmd_status", command_status)


def update_status(r, status, **kwargs):
    command_status = {
        "status": status,
        "update_time": time.time(),
    }

    # some corr_f commands return "err"
    # want to be able to update the args dict
    args = r.hget("corr:cmd_status", "args")
    args = json.loads(args)
    args.update(kwargs)

    args = json.dumps(args)
    command_status["args"] = args

    if status == "complete":
        command_status["completion_time"] = time.time()

    r.hmset("corr:cmd_status", command_status)


def cmd_handler(corr, r, message, testmode=False):
    d = json.loads(message)
    corr.logger.info("Got command: %s" % d)
    command = d["command"]
    command_time = d["time"]
    args = d["args"]
    if testmode:
        print "Got command:", command
        print "       args:", args
        return
    if command == "phase_switch":
        create_status(r, command, command_time, status="running", **args)
        corr.reestablish_dead_connections(programmed_only=True)
        if args["activate"]:
            corr.phase_switch_enable()
        else:
            corr.phase_switch_disable()
        update_status(r, status="complete")
        return
    elif command == "rf_switch":
        create_status(r, command, command_time, status="running", **args)
        if args["input_sel"] not in ["antenna", "noise", "load"]:
            update_status(r, status="errored", err="Unrecognized switch input")
            return
        if args["ant"] is not None:
            try:
                feng_e = corr.ant_to_snap[str(args["ant"])]['e']
                feng_n = corr.ant_to_snap[str(args["ant"])]['n']
                feng_e_host = feng_e['host']
                feng_n_host = feng_n['host']
                feng_e_chan = feng_e['channel']//2
                feng_n_chan = feng_n['channel']//2
            except KeyError:
                update_status(r, status="errored", err="Can't find F-engine for selected antenna")
                return
            if (feng_e_host != feng_n_host):
                update_status(r, status="errored", err="E/N pols not on matching SNAP")
                return
            if (isinstance(feng_e_host, basestring)):
                update_status(r, status="errored", err="Required F-engine is not connected")
                return
            if (feng_e_chan != feng_n_chan):
                update_status(r, status="errored", err="E/N pols not on matching I2C channel")
                return
            # If we made it to here, hopefully we're good
            # initialize the I2C if necessary
            if not feng.i2c_initialized:
                feng_e_host._add_i2c()
            # Try the write 5 times
            for i in range(5):
                feng_e_host.fems[feng_e_chan].switch(name=args["input_sel"])
                switch_pos = feng_e_host.fems[feng_e_chan].switch()
                if switch_pos == args["input_sel"]:
                    update_status(r, status="complete")
                    return
            # Retries exceeded
            update_status(r, status="errored", err="Retries exceeded")
            return
        else:
            corr.reestablish_dead_connections(programmed_only=True)
            if args["input_sel"] == "noise":
                corr.noise_diode_enable()
            elif args["input_sel"] == 'load':
                corr.load_enable()
            elif args["input_sel"] == "antenna":
                corr.antenna_enable()
            update_status(r, status="complete")
            return
    elif command == "snap_eq":
        create_status(r, command, command_time, status="running", **args)
        if "coeffs" not in args.keys():
            update_status(r, status="errored", err="No `coeffs` argument provided!")
            return
        if "ant" not in args.keys():
            update_status(r, status="errored", err="No `ant` argument provided!")
            return
        if "pol" not in args.keys():
            update_status(r, status="errored", err="No `pol` argument provided!")
            return
        try:
            coeffs = args['coeffs']
        except:
            corr.logger.exception("Failed to cast coeffs to numpy array")
            update_status(r, status="errored", err="Provided coefficients couldn't be coerced into a numpy array")
            return
        try:
            corr.set_eq(str(args["ant"]), args["pol"], eq=coeffs)
            update_status(r, status="complete")
        except:
            corr.logger.exception("snap_eq command failed!")
            update_status(r, status="errored", err="Command failed! Check server logs")
    elif command == "pam_atten":
        create_status(r, command, command_time, status="running", **args)
        corr.disable_monitoring(30, wait=True)
        if "rw" not in args.keys():
            update_status(r, status="errored", err="No `rw` argument provided!")
            return
        if args["rw"] == "w" and "val" not in args.keys():
            update_status(r, status="errored", err="No `val` argument provided!")
            return
        if "ant" not in args.keys():
            update_status(r, status="errored", err="No `ant` argument provided!")
            return
        if "pol" not in args.keys():
            update_status(r, status="errored", err="No `pol` argument provided!")
            return
        try:
            feng = corr.ant_to_snap[str(args["ant"])][args["pol"]]
            feng_host = feng['host']
            feng_chan = feng['channel']//2
        except KeyError:
            update_status(r, status="errored", err="Can't find F-engine for selected antenna")
            return
        if (isinstance(feng_host, basestring)):
            update_status(r, status="errored", err="Required F-engine is not connected")
            return
        # If we made it to here, hopefully we're good
        # initialize the I2C if necessary
        if not feng_host.i2c_initialized:
            feng._add_i2c()
        if args["rw"] == "w":
            # Try the write 3 times
            for i in range(3):
                if args["pol"] == "e":
                    feng_host.pams[feng_chan].set_attenuation(args["val"], None)
                    atten_e_rb, atten_n_rb = feng_host.pams[feng_chan].get_attenuation()
                    if atten_e_rb == args["val"]:
                        update_status(r, status="complete")
                        return
                if args["pol"] == "n":
                    feng_host.pams[feng_chan].set_attenuation(None, args["val"])
                    atten_e_rb, atten_n_rb = feng_host.pams[feng_chan].get_attenuation()
                    if atten_n_rb == args["val"]:
                        update_status(r, status="complete")
                        return
            # Retries exceeded
            update_status(r, status="errored", err="Retries exceeded")
            return
        if args["rw"] == "r":
            atten_e_rb, atten_n_rb = feng_host.pams[feng_chan].get_attenuation()
            if args["pol"] == "e":
                update_status(r, status="complete", val=atten_e_rb)
                return
            if args["pol"] == "n":
                update_status(r, status="complete", val=atten_n_rb)
                return

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process commands from the corr:command key channel.',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-r', dest='redishost', type=str, default='redishost',
                        help ='Hostname of redis server')
    parser.add_argument('-t', dest='testmode', action='store_true', default=False,
                        help ='Use this flag to run in test mode, where no commands are executed')
    args = parser.parse_args()

    r = redis.Redis(args.redishost, decode_responses=True)

    corr = HeraCorrelator()

    # load this module's version into redis
    corr.r.hmset('version:%s:%s' % (__package__, os.path.basename(__file__)), {'version':__version__, 'timestamp':datetime.datetime.now().isoformat()})
    # Create key for this module's status
    hostname = socket.gethostname()
    script_redis_key = "status:script:%s:%s" % (hostname, __file__)


    retry_tick = 0
    # Seconds between SNAP reconnection attempts
    RETRY_TIME = 300

    last_command_time = None
    while(True):
        # sleep 1s between each attempt
        time.sleep(1)
        message = r.get("corr:command")
        if message is not None:
            command_time = float(json.loads(message)["time"])
            if last_command_time is not None:
                if command_time > last_command_time:
                    last_command_time = command_time
                    cmd_handler(corr, r, message, testmode=args.testmode)
            else:
                # daemon was probably restarted.
                # log the execution time but take no action
                last_command_time = command_time

        corr.r.set(script_redis_key, "alive", ex=120)
