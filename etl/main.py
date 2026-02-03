# etl/main.py
"""
Main entry point for the ETL pipeline. Downloads, processes, validates, and exports data for Tableau.
"""
from etl.config import DATA_SOURCES, OUTPUT_EXCEL, LOG_FILE
from etl.logger import get_logger
from etl.download import load_all
from etl.process_clean import validate_and_summarize, process_all
from etl.export import export_to_excel, export_to_parquet, export_to_csv
from rich.console import Console
from tqdm import tqdm

logger = get_logger('etl.main', log_file=LOG_FILE)

def main():
    console = Console()
    logger.info("Starting ETL pipeline...")
    dfs = load_all(DATA_SOURCES)
    validate_and_summarize(dfs)
    processed = process_all(dfs)
    
    # Export to CSV and Parquet first (fast), then Excel (slow)
    export_to_csv(processed, output_dir="output_csv")
    export_to_parquet(processed, output_dir="output_parquet")
    
    # Optional Excel export (slower for large datasets)
    try:
        export_to_excel(processed, OUTPUT_EXCEL)
    except KeyboardInterrupt:
        logger.warning("Excel export interrupted - data available in CSV and Parquet formats")
    except Exception as e:
        logger.warning(f"Excel export failed ({e}) - using CSV/Parquet instead")
    
    # Export to SQLite database
    from etl.export import export_to_sqlite
    export_to_sqlite(processed, db_path="output_data.sqlite")
    logger.info("ETL pipeline complete.")
    console.print("[bold green]ETL pipeline complete. Data exported to CSV, Parquet, SQLite, and Excel (if available).[/bold green]")

if __name__ == "__main__":
    main()
