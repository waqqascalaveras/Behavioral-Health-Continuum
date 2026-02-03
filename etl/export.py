import sqlite3
def export_to_sqlite(dfs: Dict[str, pd.DataFrame], db_path: str) -> None:
    try:
        conn = sqlite3.connect(db_path)
        non_empty_dfs = {k: v for k, v in dfs.items() if len(v) > 0}
        logger.info(f"Exporting {len(non_empty_dfs)} non-empty datasets to SQLite")
        for key, df in non_empty_dfs.items():
            df.to_sql(key, conn, if_exists='replace', index=False)
            logger.info(f"[OK] Exported {key} ({len(df):,} rows)")
        conn.close()
        logger.info(f"[SUCCESS] Exported to {db_path}")
    except Exception as e:
        logger.error(f"Failed to export to SQLite: {e}", exc_info=True)
# etl/export.py
"""
Export processed data to Excel for Tableau.
"""
import pandas as pd
from typing import Dict
from .logger import get_logger

logger = get_logger('etl.export')

def export_to_excel(dfs: Dict[str, pd.DataFrame], output_path: str) -> None:
    import re
    # Pattern for illegal XML characters that Excel/openpyxl doesn't allow
    ILLEGAL_CHARACTERS_RE = re.compile(r'[\000-\010]|[\013-\014]|[\016-\037]')
    
    def clean_for_excel(val):
        """Remove illegal characters from cell values"""
        if isinstance(val, str):
            return ILLEGAL_CHARACTERS_RE.sub('', val)
        return val
    
    try:
        # Filter out empty datasets to speed up export
        non_empty_dfs = {k: v for k, v in dfs.items() if len(v) > 0}
        logger.info(f"Exporting {len(non_empty_dfs)} non-empty datasets (skipping {len(dfs) - len(non_empty_dfs)} empty ones)")
        
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            for idx, (key, df) in enumerate(non_empty_dfs.items(), 1):
                logger.info(f"[{idx}/{len(non_empty_dfs)}] Writing {key} ({len(df):,} rows)...")
                
                # Clean all string columns to remove illegal characters
                df_clean = df.copy()
                for col in df_clean.columns:
                    if df_clean[col].dtype == 'object':
                        df_clean[col] = df_clean[col].apply(clean_for_excel)
                
                df_clean.to_excel(writer, sheet_name=key[:31], index=False)
                logger.info(f"  [OK] Sheet '{key[:31]}': {len(df_clean):,} rows written")
        logger.info(f"[SUCCESS] Exported {len(non_empty_dfs)} sheets to {output_path}")
    except Exception as e:
        logger.error(f"Failed to export to Excel: {e}", exc_info=True)

def export_to_parquet(dfs: Dict[str, pd.DataFrame], output_dir: str) -> None:
    import os
    os.makedirs(output_dir, exist_ok=True)
    non_empty_dfs = {k: v for k, v in dfs.items() if len(v) > 0}
    logger.info(f"Exporting {len(non_empty_dfs)} non-empty datasets to Parquet")
    for key, df in non_empty_dfs.items():
        out_path = os.path.join(output_dir, f"{key}.parquet")
        try:
            # Fix mixed types: convert object columns with mixed types to string
            df_clean = df.copy()
            for col in df_clean.columns:
                if df_clean[col].dtype == 'object':
                    # Check for mixed numeric/string values
                    try:
                        pd.to_numeric(df_clean[col], errors='coerce')
                        # If conversion works, convert to string for consistency
                        df_clean[col] = df_clean[col].astype(str)
                    except:
                        pass
            
            df_clean.to_parquet(out_path, engine='pyarrow', index=False)
            logger.info(f"[OK] Exported {key} ({len(df_clean):,} rows)")
        except Exception as e:
            logger.error(f"Failed to export {key} to Parquet: {e}", exc_info=True)

def export_to_csv(dfs: Dict[str, pd.DataFrame], output_dir: str) -> None:
    import os
    os.makedirs(output_dir, exist_ok=True)
    non_empty_dfs = {k: v for k, v in dfs.items() if len(v) > 0}
    logger.info(f"Exporting {len(non_empty_dfs)} non-empty datasets to CSV")
    for key, df in non_empty_dfs.items():
        out_path = os.path.join(output_dir, f"{key}.csv")
        try:
            df.to_csv(out_path, index=False)
            logger.info(f"[OK] Exported {key} ({len(df):,} rows)")
        except Exception as e:
            logger.error(f"Failed to export {key} to CSV: {e}", exc_info=True)
