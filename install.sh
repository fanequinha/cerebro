#!/bin/bash

sudo apt-get update
sudo apt-get install -y \
    libxml2-dev libxslt-dev \
    python-dev python-pip python3-pip \
    libopenjp2-7-dev libtiff5-dev

pip install -r commander/req_2.txt
pip install -r mastermind/req_3.txt
