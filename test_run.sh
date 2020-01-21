#!/bin/bash

venv_dir="venv/"


if [ ! -d "$venv_dir" ]; then 
  echo "venv doesn't exist"
  echo "Updating pip..."
  pip install --upgrade pip
  echo "pip updated!"
  echo "Creating venv"
  python3.6 -m venv venv
  echo "venv created!"
else
  
fi

echo "The end"

