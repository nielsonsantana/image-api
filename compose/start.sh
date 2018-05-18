#!/bin/bash

pip install -r requirements/test.txt 
python setup.py develop &> /dev/null

echo -e "\n\n"
echo "Starting server on port 0.0.0.0:8000"
pserve development.ini --reload