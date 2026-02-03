"""
Summary statistics for ETL datasets.
"""
import pandas as pd
from typing import Dict

def summary_stats(dfs: Dict[str, pd.DataFrame]) -> Dict[str, pd.DataFrame]:
    stats = {}
    for key, df in dfs.items():
        if not df.empty:
            desc = df.describe(include='all', datetime_is_numeric=True)
            stats[key] = desc
    return stats

if __name__ == '__main__':
    from etl.config import DATA_SOURCES
    from etl.download import load_all
    dfs = load_all(DATA_SOURCES)
    stats = summary_stats(dfs)
    for k, v in stats.items():
        print(f"--- {k} ---\n{v}\n")
