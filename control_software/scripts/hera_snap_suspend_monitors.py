#! /usr/bin/env python

import argparse
import redis
import logging
from hera_corr_cm.handlers import add_default_log_handlers

logger = add_default_log_handlers(logging.getLogger(__file__))

parser = argparse.ArgumentParser(description='Suspend snap monitors for a specified time period',
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-r', dest='redishost', type=str, default='redishost',
                    help='Host servicing redis requests')
parser.add_argument('-t', dest='suspend_mins', type=float, default=5.0,
                    help='Time, in minutes, for which to suspend monitor processes')

args = parser.parse_args()

logger.info('Connecting to redis server %s' % args.redishost)
connection_pool = redis.ConnectionPool(host=args.redishost)
r = redis.Redis(connection_pool=connection_pool, max_connections=100)

suspend_secs = int(60*args.suspend_mins)
logger.info('Disabling snap monitoring for %.1f minutes (%d seconds)' % (args.suspend_mins, suspend_secs))
r.set('disable_monitoring', 1, ex=suspend_secs)
