================================================================
                      Network Amplifier
================================================================

Collection of tools used for my custom network amplifier.

python/
	network-enabled python web process allowing fine control
	of all modules and features of the amplifier via HTTP.
  Modules installed:
    Audio - PT2314 i2c amplifier mixer 
    Radio - si4703 FM Tuner controlled via i2c
    MP3 - localhost 6600 connection to mpd daemon    

html/
  HTML / CSS / Javascript frontend controller via HTTP.
  Hosted locally with an nginx server.

android-app/
	Android application used to control amplifier via HTTP

android-widget/
	Home screen widget used to control amplifier via HTTP

node/
	Node text processor used to control amplifier via HTTP


================================================================
                Network Amplifier Python Library
================================================================

A library for my custom amplifier hardware with the Raspberry Pi.

Prerequisites
=============
python2.7
ConfigObj
wiringpi2
wiringpi
gaugette

Usage
=====
sudo python startServer.py

runs the amplifier's web server on localhost, port 8241


================================================================
https://github.com/ronnied/network-amplifier
