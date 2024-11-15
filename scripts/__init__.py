import os
import sys

# Get the current directory of this file
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the Src directory
src_dir = os.path.join(current_dir, '..', '..', 'Src')

# Add the Src directory to the system path
sys.path.insert(0, src_dir)
