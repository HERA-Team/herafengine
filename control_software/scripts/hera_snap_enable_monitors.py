#! /usr/bin/env python

import argparse
import redis
import logging
from hera_corr_cm.handlers import add_default_log_handlers

logger = add_default_log_handlers(logging.getLogger(__file__))

parser = argparse.ArgumentParser(description='Delete the "disable monitoring" redis key',
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-r', dest='redishost', type=str, default='redishost',
                    help='Host servicing redis requests')

args = parser.parse_args()

logger.info('Connecting to redis server %s' % args.redishost)
r = redis.Redis(args.redishost, decode_responses=True)

logger.info('Enabling snap monitoring')
r.delete('disable_monitoring')
