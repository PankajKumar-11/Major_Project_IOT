"""
Main Entry Point for Streamlit Dashboard.
Allows running: streamlit run app.py  OR  streamlit run dashboard/app.py
"""
import sys
from pathlib import Path

# Add project root to path before anything else
ROOT_DIR = Path(__file__).resolve().parent  # This is Major_project/
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# Also inject ROOT_DIR into builtins so dashboard/app.py can find it
# even if its own __file__ resolution fails under runpy
import builtins
builtins._ZT_ROOT_DIR = str(ROOT_DIR)

# Execute the dashboard app
import runpy
runpy.run_path(str(ROOT_DIR / "dashboard" / "app.py"), run_name="__main__")

