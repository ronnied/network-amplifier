#!/usr/bin/env python

from distutils.core import setup

setup(name='ronniedAmp',
      version='1.0',
      description='Python library for interfacing custom network (i2c controlled) amplifier',
      author='Ronald Diaz',
      author_email='ronald@ronalddiaz.net',
      url='http://github.com/ronnied/network-amplifier/',
      license = 'LICENSE.txt',
      long_description=open('README.txt').read(),
      packages=['ronniedAmp'],
)
