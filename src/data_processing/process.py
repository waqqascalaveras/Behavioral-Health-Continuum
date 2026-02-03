import pandas as pd
from typing import Dict
from rich.console import Console
from rich.table import Table
import pandera.pandas as pa
from pandera.pandas import DataFrameSchema, Column
from src.utils.logger import get_logger
from src.config.datasets import DATASET_PROCESSING

logger = get_logger('data_processing.process')
console = Console()

def validate_and_summarize(dfs: Dict[str, pd.DataFrame]) -> None:
    for key, df in dfs.items():
        logger.info(f"--- {key} ---")
        logger.info(f"Rows: {len(df)} | Columns: {list(df.columns)}")
        table = Table(title=f"{key} (first 5 rows)")
        if not df.empty:
            for col in df.columns:
                table.add_column(str(col))
            for _, row in df.head(5).iterrows():
                table.add_row(*[str(x) for x in row.values])
            missing = df.isnull().sum()
            logger.info(f"Missing values:\n{missing}")
            logger.info(f"Describe:\n{df.describe(include='all')}")
        else:
            logger.warning(f"{key} is empty!")
            table.add_column("No data")
            table.add_row("")
        console.print(table)

def process_all(dfs: Dict[str, pd.DataFrame]) -> Dict[str, pd.DataFrame]:
    # Example: Standardize county/zip, validate with schema, dataset-specific hooks
    schemas = {}  # TODO: Move schemas to config/datasets.py
    for key, df in dfs.items():
        if 'county' in df.columns:
            df['county'] = df['county'].astype(str).str.title()
        if 'zip_code' in df.columns:
            df['zip_code'] = df['zip_code'].astype(str).str.zfill(5)
        if key in schemas:
            try:
                df = schemas[key].validate(df, lazy=True)
            except pa.errors.SchemaErrors as e:
                logger.error(f"Schema validation failed for {key}: {e.failure_cases}")
        if key in DATASET_PROCESSING:
            notes = DATASET_PROCESSING[key].get('notes', '')
            logger.info(f"Processing notes for {key}: {notes}")
            # Custom cleaning hooks here
        dfs[key] = df
    return dfs
