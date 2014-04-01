# coding=utf-8
from __future__ import unicode_literals

from wowinst import install, uninstall, enable, os, logging

logging.getLogger().setLevel(logging.INFO)

install(os.path.expanduser('~/Hämtningar/DBM-Core-5.4.12.zip'), 'DBM-Core', '5.4.12')
enable('DBM-Core', '5.4.12')
uninstall('DBM-Core', '5.4.12')
