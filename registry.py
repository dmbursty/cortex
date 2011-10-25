#!/usr/bin/python

import script_init

import logging.config

from cortex.registry.Registry import Registry

logging.config.fileConfig("logs/configs/registry_logging.conf")
Registry().start()
