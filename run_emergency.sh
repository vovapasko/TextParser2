#!/bin/bash

venv_dir="venv/"

if [ ! -d "$venv_dir" ]; then
  echo "venv doesn't exist"
  echo "Creating venv"
  python3.6 -m venv venv
  echo "venv created!"
  source venv/bin/activate
  echo "Updating pip..."
  pip install --upgrade pip
  echo "pip updated!"
  echo "installing requirements"
  pip install -r requirements.txt
  echo "Requirements are installed!"
  source venv/bin/activate
else
  source venv/bin/activate
fi

python3 main.py run_emergency
deactivate

