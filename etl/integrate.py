"""
Integrate datasets for analysis: join/merge on common keys and create integrated views.
"""
import pandas as pd
from typing import Dict
from .logger import get_logger

logger = get_logger('etl.integrate')

def integrate_datasets(dfs: Dict[str, pd.DataFrame]) -> Dict[str, pd.DataFrame]:
    # Example: merge SUD facilities and provider listing on county and zip
    integrated = {}
    if 'sud_recovery_facilities' in dfs and 'ffs_providers_profile' in dfs:
        sud = dfs['sud_recovery_facilities']
        ffs = dfs['ffs_providers_profile']
        if not sud.empty and not ffs.empty:
            merged = pd.merge(sud, ffs, left_on=['CountyName', 'Facility_Zip'], right_on=['County', 'Zip'], how='inner', suffixes=('_sud', '_ffs'))
            integrated['sud_ffs_integrated'] = merged
            logger.info(f"Integrated SUD and FFS: {len(merged)} rows")
    # Add more integrations as needed
    return integrated

if __name__ == '__main__':
    from etl.config import DATA_SOURCES
    from etl.download import load_all
    dfs = load_all(DATA_SOURCES)
    integrated = integrate_datasets(dfs)
    print({k: v.shape for k, v in integrated.items()})
