#!/bin/bash

kill `ps -ef | grep 'uvicorn main:app'| grep -v grep | awk '{print $2}'`
cd /data2/chatgpt-web-share/backend
source ../venv/bin/activate
nohup uvicorn main:app --workers 4 &