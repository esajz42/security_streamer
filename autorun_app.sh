#!/usr/bin/env bash

# Kill all running apache instances
sudo pkill apache

# Start security cam streaming server
python app.py
