#!/bin/bash

kill `ps -ef | grep 'python main.py'| grep -v grep | awk '{print $2}'`
cd /data2/chatgpt-web-share/backend
source ../venv/bin/activate
nohup python main.py &