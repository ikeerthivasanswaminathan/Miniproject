"""
Root entry point for Streamlit Cloud deployment.
This file allows Streamlit Cloud to find the app at the repository root.
"""

import sys
import os
from pathlib import Path

# Add projects/collegebustracker to the path and set it as working directory
project_path = Path(__file__).parent / "projects" / "collegebustracker"
sys.path.insert(0, str(project_path))
os.chdir(str(project_path))

# Import and run the actual app
exec(open(str(project_path / "app.py")).read())
