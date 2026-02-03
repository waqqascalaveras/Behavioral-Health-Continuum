"""
Streamlit Dashboard Launcher
Runs the behavioral health dashboard via Python module (no exe required)
Can be double-clicked or run from command line.

Usage: python run_dashboard.py
"""
import sys
import os
import subprocess
import webbrowser
import time

# Auto-install dependencies if missing
def ensure_dependencies():
    """Install required packages if not already installed"""
    required = ['pandas', 'streamlit', 'plotly', 'openpyxl']
    missing = []
    for package in required:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)
    
    if missing:
        print(f"\n📦 Installing missing packages: {', '.join(missing)}\n")
        subprocess.run([sys.executable, "-m", "pip", "install", "--user", *missing], check=True)
        print("\n✅ Dependencies installed!\n")

try:
    ensure_dependencies()
except Exception as e:
    print(f"\n⚠️  Warning: Could not install dependencies: {e}\n")

def main():
    # Ensure we're in the right directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Set PYTHONPATH for ETL imports
    os.environ['PYTHONPATH'] = script_dir
    
    print("=" * 60)
    print("🏥 CALAVERAS COUNTY BEHAVIORAL HEALTH DASHBOARD")
    print("=" * 60)
    print(f"\nStarting from: {script_dir}")
    print("\n📊 Dashboard URL: http://localhost:8501")
    print("\n⏹️  Press Ctrl+C to stop the dashboard\n")
    
    # Try to open browser automatically after a short delay
    def open_browser():
        time.sleep(3)  # Give Streamlit time to start
        try:
            webbrowser.open('http://localhost:8501', new=2)
        except Exception:
            pass  # Browser open failed, but dashboard is still running
    
    import threading
    browser_thread = threading.Thread(target=open_browser, daemon=True)
    browser_thread.start()
    
    # Run streamlit as a subprocess using -m flag (module mode, no exe required)
    try:
        subprocess.run([
            sys.executable,
            "-m",
            "streamlit",
            "run",
            "dashboards.py",
            "--logger.level=warning",
            "--client.toolbarMode=minimal",
            "--client.showErrorDetails=true"
        ], check=False)
    except KeyboardInterrupt:
        print("\n✅ Dashboard stopped.\n")
        sys.exit(0)
    except FileNotFoundError:
        print("\n❌ Error: Streamlit is not installed or Python executable not found.")
        print("   Please install Streamlit: pip install streamlit")
        input("\nPress Enter to exit...")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error starting dashboard: {e}")
        input("\nPress Enter to exit...")
        sys.exit(1)

if __name__ == "__main__":
    main()

