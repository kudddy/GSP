#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import requests
import logging

from GeoService.ext.Pickler import PclWorker as pcl


class NTLogger:
    def __init__(self, context, verbose):
        self.context = context
        self.verbose = verbose

    def info(self, msg, **kwargs):
        print('I:%s:%s' % (self.context, msg), flush=True)

    def debug(self, msg, **kwargs):
        if self.verbose:
            print('D:%s:%s' % (self.context, msg), flush=True)

    def error(self, msg, **kwargs):
        print('E:%s:%s' % (self.context, msg), flush=True)

    def warning(self, msg, **kwargs):
        print('W:%s:%s' % (self.context, msg), flush=True)


def set_logger(context, verbose=False):
    logger = logging.getLogger(context)
    logger.setLevel(logging.DEBUG if verbose else logging.INFO)
    formatter = logging.Formatter(
        '%(asctime)s:%(levelname)-s:' + context + ':[%(filename)s:%(funcName)s:%(lineno)3d]:%(message)s', datefmt=
        '%Y-%m-%d %H:%M:%S')
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG if verbose else logging.INFO)
    console_handler.setFormatter(formatter)
    logger.handlers = []

    logger.addHandler(console_handler)

    fh = logging.FileHandler('vac_bot_logs.log')
    fh.setLevel(logging.DEBUG if verbose else logging.INFO)
    fh.setFormatter(formatter)

    logger.addHandler(fh)
    return logger


def get_response(url, data):
    headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
    payload = json.dumps(data)
    r = requests.post(url, data=payload, headers=headers)
    result = r.json()
    return result
