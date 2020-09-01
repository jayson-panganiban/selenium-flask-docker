#!/bin/bash
app="pythonbot"
docker build -t ${app} .
docker run --rm -d -p 127.0.0.1:5000:5000 --name=${app} ${app}