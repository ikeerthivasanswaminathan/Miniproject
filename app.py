"""
Root entry point for Streamlit Cloud deployment.
This file allows Streamlit Cloud to find the app at the repository root.
"""

import sys
from pathlib import Path

# Add projects/collegebustracker to the path so imports work correctly
project_path = Path(__file__).parent / "projects" / "collegebustracker"
sys.path.insert(0, str(project_path))

# Import and run the actual app
from projects.collegebustracker.app import *  # noqa: F401, F403
