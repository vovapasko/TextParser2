#!/bin/bash

echo "Creating Python3.6 venv..."
python3.6 -m venv venv
echo "venv Created!"
echo "Updated pip and installing all libs from requirements.txt"
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
deactivate
echo "Script finished successfully"