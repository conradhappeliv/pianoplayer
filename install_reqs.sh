#!/bin/sh

# midicsv
mkdir tmp
curl http://www.fourmilab.ch/webtools/midicsv/midicsv-1.1.tar.gz | tar xvz -C ./tmp
cd ./tmp/midicsv-1.1
make && make install
cd ../..
rm -Rf tmp

# pip
if pip; then
    echo "pip already installed"
else
    curl https://bootstrap.pypa.io/get-pip.py | python
fi

# pyserial
pip install pyserial