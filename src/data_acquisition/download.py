import os
import pandas as pd
import requests
from io import BytesIO
from tqdm import tqdm
from typing import Dict, Optional
from src.utils.logger import get_logger

logger = get_logger('data_acquisition.download')

def load_data(source: str) -> Optional[pd.DataFrame]:
    """
    Load a CSV, Excel, Parquet, or text file from a URL or local file. Returns DataFrame or None on error.
    Handles manual/restricted/local sources by logging a warning and returning None.
    """
    try:
        if source.startswith('manual:') or source.startswith('restricted:'):
            logger.warning(f"Manual or restricted source, skipping: {source}")
            return None
        if source.startswith('http://') or source.startswith('https://'):
            logger.info(f"Downloading: {source}")
            response = requests.get(source, timeout=60)
            response.raise_for_status()
            if source.endswith('.parquet'):
                import pyarrow.parquet as pq
                df = pq.read_table(BytesIO(response.content)).to_pandas()
            elif source.endswith('.xlsx') or source.endswith('.xls'):
                df = pd.read_excel(BytesIO(response.content))
            elif source.endswith('.txt'):
                df = pd.read_csv(BytesIO(response.content), delimiter=None, engine='python')
            else:
                df = pd.read_csv(BytesIO(response.content))
        else:
            logger.info(f"Loading local file: {source}")
            if not os.path.exists(source):
                logger.error(f"File not found: {source}")
                return None
            if source.endswith('.parquet'):
                df = pd.read_parquet(source, engine='pyarrow')
            elif source.endswith('.xlsx') or source.endswith('.xls'):
                df = pd.read_excel(source)
            elif source.endswith('.txt'):
                df = pd.read_csv(source, delimiter=None, engine='python')
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
        df = load_data(src)
        if df is not None:
            dfs[key] = df
        else:
            dfs[key] = pd.DataFrame()
    return dfs
