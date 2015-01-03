#!/bin/sh

# midicsv
wget -q0- http://www.fourmilab.ch/webtools/midicsv/midicsv-1.1.tar.gz | tar xvz -C ./tmp
cd tmp && make && make install
rm -R tmp

# pip
wget -q0- https://bootstrap.pypa.io/get-pip.py | python

# pyserial
pip install pyserial