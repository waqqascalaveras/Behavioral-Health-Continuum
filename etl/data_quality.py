"""
Data quality report for ETL datasets. Checks missing values, outliers, invalid data, and exports summary.
"""
import os
import pandas as pd
from typing import Dict
from .logger import get_logger

logger = get_logger('etl.data_quality')

REPORT_PATH = os.path.join(os.path.dirname(__file__), 'data_quality_report.md')

def check_quality(dfs: Dict[str, pd.DataFrame]) -> None:
    report_lines = ['# Data Quality Report\n']
    for key, df in dfs.items():
        report_lines.append(f'## {key}\n')
        if df.empty:
            report_lines.append('No data loaded.\n')
            continue
        missing = df.isnull().sum()
        report_lines.append('### Missing Values\n')
        report_lines.append(missing.to_string())
        report_lines.append('\n')
        report_lines.append('### Data Types\n')
        report_lines.append(df.dtypes.to_string())
        report_lines.append('\n')
        report_lines.append('### Describe\n')
        report_lines.append(df.describe(include="all", datetime_is_numeric=True).to_string())
        report_lines.append('\n')
        # Outlier detection (simple)
        for col in df.select_dtypes(include=['float', 'int']).columns:
            vals = df[col].dropna()
            if len(vals) > 0:
                q1 = vals.quantile(0.25)
                q3 = vals.quantile(0.75)
                iqr = q3 - q1
                outliers = ((vals < (q1 - 1.5 * iqr)) | (vals > (q3 + 1.5 * iqr))).sum()
                report_lines.append(f'Outliers in {col}: {outliers}\n')
        report_lines.append('\n')
    with open(REPORT_PATH, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report_lines))
    print(f'Data quality report written to {REPORT_PATH}')

if __name__ == '__main__':
    # Example usage: run after ETL main
    from etl.config import DATA_SOURCES
    from etl.download import load_all
    dfs = load_all(DATA_SOURCES)
    check_quality(dfs)
