
import os
import sys
import time
import threading

# Always add project root to sys.path so etl absolute imports work
if __name__ == '__main__':
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from etl.config import DATA_SOURCES
from etl.download import load_data
from etl.process_clean import validate_and_summarize, process_all
from etl.export import export_to_excel, export_to_parquet, export_to_csv, export_to_sqlite
from etl.logger import get_logger

logger = get_logger('cli_app')

MENU = '''
========================================
 Behavioral Health ETL - DOS CLI
========================================
1. List all datasets
2. Download a dataset
3. Download all datasets
4. Process all datasets
5. Export all datasets
6. Run full ETL pipeline
7. Show log file
8. Exit
========================================
Choose an option (1-8): '''

DATASET_STATUS = {k: 'Not started' for k in DATA_SOURCES}
DATASET_FRAMES = {}

LOG_FILE = 'etl.log'

def persistent_window(msg):
    try:
        import tkinter as tk
        root = tk.Tk()
        root.title('Behavioral Health ETL CLI')
        text = tk.Text(root, height=20, width=80)
        text.insert('1.0', msg)
        text.pack()
        btn = tk.Button(root, text='Close', command=root.destroy)
        btn.pack()
        root.mainloop()
    except Exception:
        pass


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_status():
    print('\nDataset Status:')
    for k, v in DATASET_STATUS.items():
        print(f'  {k:35} : {v}')
    print()

def list_datasets():
    print('\nAvailable datasets:')
    for i, k in enumerate(DATA_SOURCES, 1):
        print(f'  {i}. {k}')
    print()

def download_dataset(name):
    print(f'\nDownloading {name}...')
    DATASET_STATUS[name] = 'Downloading...'
    try:
        df = load_data(DATA_SOURCES[name])
        if df is not None:
            DATASET_FRAMES[name] = df
            DATASET_STATUS[name] = f'Downloaded ({len(df)} rows)'
            print(f'  Success: {len(df)} rows loaded.')
        else:
            DATASET_STATUS[name] = 'Failed (no data)'
            print('  Failed: No data.')
    except Exception as e:
        DATASET_STATUS[name] = f'Failed ({e})'
        print(f'  Error: {e}')
    time.sleep(1)

def download_all():
    for k in DATA_SOURCES:
        download_dataset(k)

def process_all():
    print('\nProcessing all datasets...')
    if not DATASET_FRAMES:
        print('  No data loaded. Download first!')
        return
    try:
        validate_and_summarize(DATASET_FRAMES)
        DATASET_STATUS.update({k: 'Processed' for k in DATASET_FRAMES})
        print('  Processing complete.')
    except Exception as e:
        print(f'  Error: {e}')
    time.sleep(1)

def export_all():
    print('\nExporting all datasets...')
    if not DATASET_FRAMES:
        print('  No data loaded. Download first!')
        return
    try:
        export_to_excel(DATASET_FRAMES, 'behavioral_health_dashboard_data.xlsx')
        export_to_parquet(DATASET_FRAMES, 'output_parquet')
        export_to_csv(DATASET_FRAMES, 'output_csv')
        export_to_sqlite(DATASET_FRAMES, 'output_data.sqlite')
        print('  Export complete: Excel, Parquet, CSV, SQLite.')
    except Exception as e:
        print(f'  Error: {e}')
    time.sleep(1)

def show_log():
    print(f'\n--- {LOG_FILE} ---')
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r', encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()[-30:]
            for line in lines:
                print(line.rstrip())
    else:
        print('  Log file not found.')
    input('\nPress Enter to continue...')

def run_full_etl():
    download_all()
    process_all()
    export_all()
    print('\nFull ETL pipeline complete!')
    time.sleep(2)

def main():
    try:
        if not sys.stdin.isatty():
            persistent_window('This CLI must be run in a terminal window.\n\nDouble-clicking may not work.\n\nOpen a command prompt, navigate to the project folder, and run:\n\n    python etl/cli_app.py\n\nOr use Windows Terminal or PowerShell.\n')
            return
        input('Welcome to the Behavioral Health ETL CLI!\nPress Enter to start...')
        while True:
            clear_screen()
            print_status()
            choice = input(MENU).strip()
            if choice == '1':
                list_datasets()
                input('Press Enter to continue...')
            elif choice == '2':
                list_datasets()
                idx = input('Enter dataset number: ').strip()
                try:
                    idx = int(idx) - 1
                    name = list(DATA_SOURCES)[idx]
                    download_dataset(name)
                except Exception:
                    print('Invalid selection.')
                input('Press Enter to continue...')
            elif choice == '3':
                download_all()
                input('Press Enter to continue...')
            elif choice == '4':
                process_all()
                input('Press Enter to continue...')
            elif choice == '5':
                export_all()
                input('Press Enter to continue...')
            elif choice == '6':
                run_full_etl()
                input('Press Enter to continue...')
            elif choice == '7':
                show_log()
            elif choice == '8':
                print('Goodbye!')
                break
            else:
                print('Invalid option.')
                time.sleep(1)
    except Exception as e:
        msg = f"[ERROR] {e}\n\n"
        import traceback
        import io
        buf = io.StringIO()
        traceback.print_exc(file=buf)
        msg += buf.getvalue()
        if not sys.stdin.isatty():
            persistent_window(msg)
        else:
            print(f"\n{msg}")
    finally:
        if sys.stdin.isatty():
            input('\nPress Enter to exit...')

if __name__ == '__main__':
    main()
