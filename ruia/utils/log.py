#!/usr/bin/env python

import logging


def get_logger(name='Ruia'):
    logging_format = '[%(levelname)-7s][%(asctime)s][module:%(module)-7s][%(filename)s][line:%(lineno)s]: %(message)s'
    logging.basicConfig(
        format=logging_format,
        level=logging.DEBUG
    )
    logging.getLogger("asyncio").setLevel(logging.INFO)
    logging.getLogger("pyppeteer").setLevel(logging.INFO)
    logging.getLogger("websockets").setLevel(logging.INFO)
    return logging.getLogger(name)
