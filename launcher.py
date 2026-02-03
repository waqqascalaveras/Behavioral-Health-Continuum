"""
Behavioral Health Project Launcher
Easy-to-use menu for running ETL pipeline and dashboard

This is the main entry point for the project.
- Double-click launcher.py to run
- Or use: python launcher.py
"""
import sys
import os
import subprocess

# Auto-install dependencies if missing
def ensure_dependencies():
    """Install required packages if not already installed"""
    required = [
        'pandas',
        'streamlit',
        'plotly',
        'openpyxl',
        'pandera',
        'polars'
    ]
    
    missing = []
    for package in required:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)
    
    if missing:
        print(f"\n📦 Installing missing packages: {', '.join(missing)}\n")
        subprocess.run([
            sys.executable,
            "-m",
            "pip",
            "install",
            "--user",
            *missing
        ], check=True)
        print("\n✅ Dependencies installed successfully!\n")

# Install dependencies on startup
try:
    ensure_dependencies()
except Exception as e:
    print(f"\n⚠️  Warning: Could not install dependencies: {e}\n")

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    os.environ['PYTHONPATH'] = script_dir
    
    while True:
        print("\n" + "=" * 60)
        print("🏥 BEHAVIORAL HEALTH ETL & DASHBOARD")
        print("=" * 60)
        print("\nOptions:")
        print("  1️⃣  Run ETL Pipeline (process data)")
        print("  2️⃣  Launch Dashboard (view results)")
        print("  3️⃣  Run Both (ETL then Dashboard)")
        print("  4️⃣  Exit")
        print("\n" + "-" * 60)
        
        choice = input("Select option (1-4): ").strip()
        
        if choice == "1":
            run_etl()
        elif choice == "2":
            run_dashboard()
        elif choice == "3":
            run_etl()
            if input("\nStart dashboard? (y/n): ").lower() == 'y':
                run_dashboard()
        elif choice == "4":
            print("\n👋 Goodbye!\n")
            sys.exit(0)
        else:
            print("\n⚠️  Invalid option. Please select 1-4.")

def run_etl():
    """Run the ETL pipeline"""
    print("\n" + "=" * 60)
    print("🔄 RUNNING ETL PIPELINE")
    print("=" * 60 + "\n")
    
    try:
        result = subprocess.run([
            sys.executable,
            "-m",
            "etl.main"
        ], check=False)
        
        if result.returncode == 0:
            print("\n✅ ETL Pipeline completed successfully!")
        else:
            print(f"\n⚠️  Pipeline exited with code {result.returncode}")
            
    except KeyboardInterrupt:
        print("\n⏹️  Pipeline cancelled by user.")
    except Exception as e:
        print(f"\n❌ Error: {e}")

def run_dashboard():
    """Run the Streamlit dashboard"""
    print("\n" + "=" * 60)
    print("📊 LAUNCHING DASHBOARD")
    print("=" * 60)
    print("\n🌐 Dashboard URL: http://localhost:8501")
    print("⏹️  Press Ctrl+C to stop\n")
    
    try:
        import webbrowser
        import threading
        import time
        
        # Open browser in background
        def open_browser():
            time.sleep(3)
            try:
                webbrowser.open('http://localhost:8501', new=2)
            except Exception:
                pass
        
        browser_thread = threading.Thread(target=open_browser, daemon=True)
        browser_thread.start()
        
        subprocess.run([
            sys.executable,
            "-m",
            "streamlit",
            "run",
            "dashboards.py",
            "--logger.level=warning",
            "--client.toolbarMode=minimal"
        ], check=False)
        
    except KeyboardInterrupt:
        print("\n✅ Dashboard stopped.")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!\n")
        sys.exit(0)
