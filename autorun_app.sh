#!/usr/bin/env bash

# Kill all running apache instances
sudo pkill apache

# Start security cam streaming server
python /home/pi/Documents/security_streamer/app.py
