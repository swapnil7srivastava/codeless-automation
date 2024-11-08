import sys
import os

# Get the absolute path to the 'code' directory
folder_a_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Add 'code' to the system path
sys.path.append(folder_a_path)

# Now import the modules
from pyDefinitions import *  # Import everything from pyDefinitions.py
from system_pyDefinitions import *  # Import everything from system_pyDefinitions.py