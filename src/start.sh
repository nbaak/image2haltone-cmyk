#!/bin/bash

THIS_DIR=$(dirname $(readlink -f $0)) 

python3 ${THIS_DIR}/App.py
