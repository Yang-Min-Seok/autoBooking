#!/bin/bash

# move to script dir
cd "$(dirname "$0")"

# activate virtuatl env
source venv/bin/activate

# run test_maim.py
python test_main.py