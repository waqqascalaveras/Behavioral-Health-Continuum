"""
Facility map visualization for SUD Recovery Treatment Facilities.
"""
import pandas as pd
import matplotlib.pyplot as plt

def plot_facility_map(df: pd.DataFrame):
    if 'Latitude' in df.columns and 'Longitude' in df.columns:
        plt.figure(figsize=(8, 8))
        plt.scatter(df['Longitude'], df['Latitude'], alpha=0.5)
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.title('SUD Recovery Treatment Facilities Map')
        plt.show()

if __name__ == '__main__':
    from etl.config import DATA_SOURCES
    from etl.download import load_all
    dfs = load_all(DATA_SOURCES)
    df = dfs.get('sud_recovery_facilities', pd.DataFrame())
    plot_facility_map(df)
