#!/bin/sh

# pip
if pip &> /dev/null; then
    echo "pip already installed"
else
    curl https://bootstrap.pypa.io/get-pip.py | python
fi

# pyserial
pip install pyserial

# mido
pip install mido