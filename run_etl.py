"""
ETL Pipeline Runner
Executes the Behavioral Health data ETL pipeline
Downloads, validates, processes, and exports data to multiple formats

Usage: python run_etl.py
"""
import sys
import os
import subprocess

# Auto-install dependencies if missing
def ensure_dependencies():
    """Install required packages if not already installed"""
    required = ['pandas', 'openpyxl', 'pandera', 'polars']
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
    
    # Set PYTHONPATH for module imports
    os.environ['PYTHONPATH'] = script_dir
    
    print("=" * 60)
    print("🔄 BEHAVIORAL HEALTH ETL PIPELINE")
    print("=" * 60)
    print(f"\nStarting from: {script_dir}")
    print("\n📥 Pipeline will:")
    print("   1. Load all configured datasets")
    print("   2. Validate schemas and data quality")
    print("   3. Apply county filtering (Calaveras County)")
    print("   4. Export to CSV, Parquet, SQLite, and Excel\n")
    print("⏹️  Press Ctrl+C to cancel\n")
    
    # Run ETL pipeline
    try:
        result = subprocess.run([
            sys.executable,
            "-m",
            "etl.main"
        ], check=False)
        
        if result.returncode == 0:
            print("\n✅ ETL Pipeline completed successfully!")
            print("\n📊 Data exported to:")
            print("   • CSV:      output_csv/")
            print("   • Parquet:  output_parquet/")
            print("   • SQLite:   output_data.sqlite")
            print("   • Excel:    behavioral_health_dashboard_data.xlsx")
            print("\n💡 Tip: Run 'python run_dashboard.py' to view the dashboard\n")
        else:
            print(f"\n⚠️  Pipeline exited with code {result.returncode}")
            
    except KeyboardInterrupt:
        print("\n\n⏹️  Pipeline cancelled by user.\n")
        sys.exit(1)
    except FileNotFoundError:
        print("\n❌ Error: Python executable not found.")
        print("   Make sure Python is installed and in your PATH.")
        input("\nPress Enter to exit...")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error running pipeline: {e}")
        input("\nPress Enter to exit...")
        sys.exit(1)

if __name__ == "__main__":
    main()
