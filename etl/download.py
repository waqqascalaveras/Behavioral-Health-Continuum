# etl/download.py
"""
Download or load data from URLs or local files with robust error handling and logging.
"""


import os
import json
import pandas as pd
import requests
from io import BytesIO
from typing import Dict, Optional
from tqdm import tqdm
from .logger import get_logger

# Set to True to bypass SSL certificate verification (not recommended for production)
BYPASS_SSL_VERIFY = True

logger = get_logger('etl.download')


def load_data(source: str, key: Optional[str] = None) -> Optional[pd.DataFrame]:
    """
    Load a CSV, Excel, Parquet, or text file from a URL or local file. Returns DataFrame or None on error.
    Handles manual/restricted/local sources by logging a warning and returning None.
    """
    try:
        if source.startswith('manual:') or source.startswith('restricted:'):
            logger.warning(f"Manual or restricted source, skipping: {source}")
            return None
        if source.startswith('http://') or source.startswith('https://'):
            logger.warning(f"Remote download disabled. Please place the file in etl/downloads and update config.py: {source}")
            return None
        else:
            logger.info(f"Loading local file: {source}")
            if not os.path.exists(source):
                logger.error(f"File not found: {source}")
                return None
            if source.endswith('.parquet'):
                df = pd.read_parquet(source, engine='pyarrow')
            elif source.endswith('.xlsx') or source.endswith('.xls'):
                sheet_name = None
                if key == 'acs_5yr_estimates':
                    sheet_name = 'Data'
                elif key == 'foster_care_entries_exits':
                    sheet_name = 'CWSOutcomes'
                df = pd.read_excel(source, sheet_name=sheet_name)
            elif source.endswith('.geojson'):
                with open(source, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                features = data.get('features', [])
                records = []
                for feature in features:
                    props = feature.get('properties', {})
                    geom = feature.get('geometry', {})
                    coords = geom.get('coordinates')
                    props['geometry_type'] = geom.get('type')
                    props['geometry_coordinates'] = coords
                    records.append(props)
                df = pd.DataFrame(records)
            elif source.endswith('.rdata') or source.endswith('.rda'):
                try:
                    import pyreadr  # type: ignore
                except Exception:
                    logger.error("pyreadr is required to load .RData/.rda files. Skipping.")
                    return None
                result = pyreadr.read_r(source)
                if len(result) == 0:
                    logger.warning("RData file contains no objects.")
                    return pd.DataFrame()
                df = next(iter(result.values()))
            elif source.endswith('.txt'):
                df = pd.read_csv(source, delimiter=None, engine='python')
            else:
                # Special handling for Core Set Mental Health - skip first title row
                if key == 'core_set_mental_health':
                    df = pd.read_csv(source, skiprows=1)
                else:
                    df = pd.read_csv(source)
        logger.info(f"Loaded {len(df)} rows from {source}")
        return df
    except Exception as e:
        logger.error(f"Failed to load {source}: {e}", exc_info=True)
        return None

def load_all(sources: Dict[str, str]) -> Dict[str, pd.DataFrame]:
    dfs = {}
    for key, src in tqdm(sources.items(), desc="Loading datasets", unit="dataset"):
        df = load_data(src, key=key)
        if df is not None:
            dfs[key] = df
        else:
            dfs[key] = pd.DataFrame()  # Empty placeholder
    return dfs
