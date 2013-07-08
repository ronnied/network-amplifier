================================================================
                   RonnieD's Network Amplifier
================================================================


Collection of tools used for my custom network amplifier.


python/
	network-enabled python web process allowing fine control
	of all features of PT2314 i2c amplifier mixer via HTTP

android-app/
	Android application used to control amplifier via HTTP

android-widget/
	Home screen widget used to control amplifier vua HTTP

node/
	Node text processor used to control amplifier via HTTP


================================================================
           RonnieD's Network Amplifier Python Library
================================================================

A library for my custom amplifier hardware with the Raspberry Pi.

Prerequisites
=============
wiringpi
gaugette

Usage
=====
sudo python startServer.py

runs the amplifier's web server
and child controller on localhost, port 8241


================================================================
https://github.com/ronnied/
