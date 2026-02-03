# Setup & Usage Guide

## Installation

### 1. Clone or Download the Project
```bash
git clone <repository>
cd behavioral_health_etl
```

### 2. Create Python Virtual Environment (Recommended)
```powershell
# Create virtual environment
python -m venv .venv

# Activate it
.venv\Scripts\Activate.ps1  # PowerShell
# or
.venv\Scripts\activate.bat  # Command Prompt
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

**Key dependencies:**
- pandas — Data processing
- pandera — Schema validation
- plotly — Interactive visualizations
- streamlit — Dashboard framework
- openpyxl — Excel export
- pyarrow — Parquet format
- geopandas — Geospatial analysis

## Quick Start

### Option 1: Double-Click to Launch (Easiest)
Just double-click any of these files:
- **`run_dashboard.py`** — View the dashboard immediately
- **`run_etl.py`** — Process and export data
- **`launcher.py`** — Show menu with all options

### Option 2: Command Line
```powershell
# Launch interactive dashboard
python run_dashboard.py

# Process data with ETL pipeline
python run_etl.py

# Show menu with all options
python launcher.py
```

## Running the Dashboard

**Easiest way:**
```powershell
python run_dashboard.py
```

This script will:
✅ Set up the Python path
✅ Launch Streamlit server
✅ Open browser automatically to http://localhost:8501
✅ Display all 5 interactive dashboards

**Manual way:**
```powershell
python -m streamlit run dashboards.py
```

### Dashboard Pages
1. 🏥 **Providers** — Medi-Cal FFS providers in Calaveras County
2. 👨‍👩‍👧 **Foster Care** — Child welfare outcomes and metrics
3. 📈 **Census** — Population demographics (ACS 5-Year)
4. ⚖️ **Grievances & Appeals** — Behavioral health service complaints
5. 🧠 **Depression** — Adult depression prevalence trends

## Running the ETL Pipeline

**Easiest way:**
```powershell
python run_etl.py
```

This will:
✅ Load all configured datasets
✅ Validate data schemas
✅ Filter to Calaveras County (where applicable)
✅ Export to CSV, Parquet, SQLite, and Excel

**Manual way:**
```powershell
python -m etl.main
```

### Output Files
After running ETL, you'll find:
- `output_csv/` — CSV files for each dataset
- `output_parquet/` — Parquet files (for big data tools)
- `output_data.sqlite` — SQLite database
- `behavioral_health_dashboard_data.xlsx` — Excel workbook for Tableau

## Configuration

### Adding New Data Sources

**Edit:** `etl/config.py`
```python
DATA_SOURCES = {
    'my_dataset': 'path/to/file.csv',
    # or
    'my_dataset': 'https://example.com/data.csv',
}
```

### Customizing Data Processing

**Edit:** `etl/process_clean.py`
1. Add schema validation in `_schemas()` function
2. Add county filtering in `_filter_by_county()` function
3. Add custom cleaning logic for your dataset

### Adding Dashboard Pages

**Edit:** `dashboards.py`
1. Create new function `def show_my_dashboard():`
2. Add to navigation sidebar
3. Load and visualize your data

## Troubleshooting

### "ModuleNotFoundError: No module named 'streamlit'"
**Fix:** Install dependencies
```bash
pip install -r requirements.txt
```

### "Port 8501 is already in use"
**Fix:** The dashboard is already running. Either:
- Stop the existing dashboard (Ctrl+C)
- Or use a different port:
```powershell
python -m streamlit run dashboards.py --server.port=8502
```

### "Python not found"
**Fix:** Make sure Python is installed and in your PATH
```powershell
python --version
```

### ETL Pipeline Fails
**Fix:** Check the logs
```powershell
# Run with detailed output
python -m etl.main
```

## Data Sources

### Calaveras County Data
1. **Medi-Cal Providers** — FFS provider directory
2. **Foster Care** — CFSR4 outcomes data
3. **Census** — ACS 5-Year demographic estimates
4. **ABGAR** — Behavioral health grievances and appeals (DHCS)

### State-Level Data
5. **Depression Prevalence** — BRFSS survey (CDPH)

### Adding More Data
See `CHHS_DATASET_RECOMMENDATIONS.md` for analysis of 407 available CHHS datasets

## Project Structure

```
behavioral_health_etl/
├── run_dashboard.py          # Launch dashboard
├── run_etl.py                # Run ETL pipeline
├── launcher.py               # Interactive menu
├── dashboards.py             # Streamlit dashboard code
├── etl/                       # ETL pipeline
│   ├── main.py              # Entry point
│   ├── config.py            # Data source configuration
│   ├── download.py          # Load data
│   ├── process_clean.py     # Validate and clean
│   ├── export.py            # Export formats
│   ├── logger.py            # Logging
│   └── downloads/           # Input data
├── src/                       # Supporting modules
│   ├── analytics/
│   ├── dashboards/
│   └── utils/
├── output_csv/              # CSV exports
├── output_parquet/          # Parquet exports
└── README.md                # This file
```

## Development

### Running Tests
```bash
# Run Python syntax check
python -m py_compile *.py etl/*.py

# Run data validation tests
python -m pytest tests/
```

### Code Style
- Follow PEP 8
- Use type hints where possible
- Document functions with docstrings

### Adding Datasets
1. Place data in `etl/downloads/dataset_name/`
2. Add to `etl/config.py` DATA_SOURCES dict
3. Add schema to `etl/process_clean.py`
4. Run ETL pipeline: `python run_etl.py`
5. Create dashboard visualization if desired

## Getting Help

1. **Check logs:** Look in `etl.log` for error details
2. **Review code:** Docstrings explain each module
3. **Read README:** [README.md](README.md) has technical details
4. **Check scripts:** All launcher scripts have helpful comments

## Common Tasks

### Export data to different formats
The ETL pipeline automatically exports to:
- CSV (spreadsheets, easy sharing)
- Parquet (big data tools)
- SQLite (databases, queries)
- Excel (Tableau, reporting)

### Create new dashboard page
1. Write function in `dashboards.py`
2. Add to navigation radio buttons
3. Use Streamlit (`st.*`) commands for UI
4. Use Plotly for interactive charts

### Add new dataset
1. Download data to `etl/downloads/my_data/`
2. Update `etl/config.py`
3. Add schema to `etl/process_clean.py`
4. Run ETL: `python run_etl.py`
5. Access via CSV, Parquet, SQLite, or Excel

## Performance Notes

- **CSV exports:** Fast, human-readable, for spreadsheets
- **Parquet exports:** Compressed, efficient, for big data
- **SQLite:** Queryable database, good for analysis
- **Excel:** Good for Tableau, slower for very large datasets

## Security Notes

- Store sensitive URLs in environment variables
- Don't commit API keys to version control
- Use `.gitignore` to exclude output directories
- Keep `etl/downloads/` with git if data is non-sensitive

---

**Happy analyzing! 📊**

For more details, see [README.md](README.md)
