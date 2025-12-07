"""
Root entry point for Streamlit Cloud deployment.
This file allows Streamlit Cloud to find the app at the repository root.
"""

import sys
import os
from pathlib import Path

# Add projects/collegebustracker to the path
project_path = Path(__file__).parent.absolute() / "projects" / "collegebustracker"
sys.path.insert(0, str(project_path))

# Change to project directory for proper relative imports
original_dir = os.getcwd()
os.chdir(str(project_path))

try:
    # Import and run the actual app
    if project_path.exists():
        import runpy
        runpy.run_path(str(project_path / "app.py"), run_name="__main__")
    else:
        raise FileNotFoundError(f"Project path not found: {project_path}")
finally:
    os.chdir(original_dir)
