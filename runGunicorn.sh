#!/bin/bash

gunicorn -b 127.0.0.1:8081 ask_semenov.wsgi