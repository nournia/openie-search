#!/bin/bash

ps -ef | grep openiesearch | awk '{print $2}' | xargs kill -9

gunicorn --bind=0.0.0.0:8000 --workers=1 app --timeout 10 --name openiesearch --log-file -
