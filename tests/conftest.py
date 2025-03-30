import sys
import os

# Add the project root directory to sys.path so that "schemas" can be found.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))