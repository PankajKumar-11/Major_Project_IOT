"""
Main Entry Point for Streamlit Dashboard.
Allows running: streamlit run app.py
"""
import sys
from pathlib import Path

# Add project root to path
ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# Execute the dashboard app
import runpy
runpy.run_path(str(ROOT_DIR / "dashboard" / "app.py"), run_name="__main__")

