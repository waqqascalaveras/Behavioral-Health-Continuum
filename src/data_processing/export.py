import pandas as pd
import sqlite3
import os
from typing import Dict
from src.utils.logger import get_logger

logger = get_logger('data_processing.export')

def export_to_excel(dfs: Dict[str, pd.DataFrame], output_path: str) -> None:
    try:
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            for key, df in dfs.items():
                df.to_excel(writer, sheet_name=key[:31], index=False)
                logger.info(f"Sheet '{key[:31]}': {len(df)} rows")
        logger.info(f"Exported data to {output_path}")
    except Exception as e:
        logger.error(f"Failed to export to Excel: {e}", exc_info=True)

def export_to_parquet(dfs: Dict[str, pd.DataFrame], output_dir: str) -> None:
    os.makedirs(output_dir, exist_ok=True)
    for key, df in dfs.items():
        out_path = os.path.join(output_dir, f"{key}.parquet")
        try:
            df.to_parquet(out_path, engine='pyarrow', index=False)
            logger.info(f"Exported {key} to {out_path} ({len(df)} rows)")
        except Exception as e:
            logger.error(f"Failed to export {key} to Parquet: {e}", exc_info=True)

def export_to_csv(dfs: Dict[str, pd.DataFrame], output_dir: str) -> None:
    os.makedirs(output_dir, exist_ok=True)
    for key, df in dfs.items():
        out_path = os.path.join(output_dir, f"{key}.csv")
        try:
            df.to_csv(out_path, index=False)
            logger.info(f"Exported {key} to {out_path} ({len(df)} rows)")
        except Exception as e:
            logger.error(f"Failed to export {key} to CSV: {e}", exc_info=True)

def export_to_sqlite(dfs: Dict[str, pd.DataFrame], db_path: str) -> None:
    try:
        conn = sqlite3.connect(db_path)
        for key, df in dfs.items():
            df.to_sql(key, conn, if_exists='replace', index=False)
            logger.info(f"Exported {key} to SQLite table ({len(df)} rows)")
        conn.close()
        logger.info(f"Exported all data to {db_path}")
    except Exception as e:
        logger.error(f"Failed to export to SQLite: {e}", exc_info=True)
