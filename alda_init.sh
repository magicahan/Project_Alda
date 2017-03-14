#!/bin/bash  
 
# Bash script for installing most modules for Whiteboard.

sudo apt-get clean
sudo apt-get update
sudo python3 -m pip install Django==1.10.6
sudo python3 -m pip install selenium
sudo python3 -m pip install numpy
sudo python3 -m pip install re
sudo python3 -m pip install openpyxl
cd AldaCourse/aldacourse/
python3 manage.py runserver
