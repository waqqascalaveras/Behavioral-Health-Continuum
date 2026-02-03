from src.config.datasets import DATASET_DEFINITIONS
from src.data_acquisition.download import load_all
from src.data_processing.process import validate_and_summarize, process_all
from src.data_processing.export import export_to_excel, export_to_parquet, export_to_csv, export_to_sqlite
from src.utils.logger import get_logger
from rich.console import Console

logger = get_logger('main')

OUTPUT_EXCEL = 'behavioral_health_dashboard_data.xlsx'


def main():
    console = Console()
    logger.info("Starting ETL pipeline...")
    # Use DATASET_DEFINITIONS for sources
    dfs = load_all(DATASET_DEFINITIONS)
    validate_and_summarize(dfs)
    processed = process_all(dfs)
    export_to_excel(processed, OUTPUT_EXCEL)
    export_to_parquet(processed, output_dir="output_parquet")
    export_to_csv(processed, output_dir="output_csv")
    export_to_sqlite(processed, db_path="output_data.sqlite")
    logger.info("ETL pipeline complete.")
    console.print("[bold green]ETL pipeline complete. Data exported to Excel, Parquet, CSV, and SQLite.[/bold green]")

if __name__ == "__main__":
    main()
