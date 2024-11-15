import sys
import os

# Get the directory of the 'scripts' directory
scripts_dir = os.path.dirname(os.path.abspath(__file__))

# Get the project root directory (parent of 'scripts')
project_root = os.path.abspath(os.path.join(scripts_dir, '..'))

# Add the project root to sys.path if it's not already there
if project_root not in sys.path:
    sys.path.insert(0, project_root)