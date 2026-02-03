# Quick Start Guide

## 🚀 Running the Project

### Option 1: Interactive Menu (Recommended)
```powershell
python launcher.py
```
- Choose from menu: ETL, Dashboard, or Both
- Auto-installs missing dependencies
- Best for beginners

### Option 2: Direct Commands
```powershell
# Dashboard only
python run_dashboard.py

# ETL only
python run_etl.py
```

### Option 3: Double-Click (Windows)
- Double-click any `.py` file above
- Runs in terminal automatically

## 📦 Dependencies
**No manual installation needed!** All scripts auto-install:
- pandas
- streamlit
- plotly
- openpyxl
- pandera
- polars

First run will install missing packages automatically.

## 🌐 Dashboard Access
- Opens automatically at: http://localhost:8501
- Press **Ctrl+C** to stop

## 📁 File Organization

**Entry Points (what to run):**
- `launcher.py` — Main menu
- `run_dashboard.py` — Dashboard only
- `run_etl.py` — ETL only

**Core Code:**
- `etl/` — ETL pipeline modules
- `dashboards.py` — Streamlit dashboard
- `etl/config.py` — Data source configuration

**Data Locations:**
- `etl/downloads/` — Input files (place here manually)
- `output_csv/` — Processed CSV exports
- `behavioral_health_dashboard_data.xlsx` — Excel export

## 🔧 Adding New Data

1. Place CSV/Excel file in `etl/downloads/`
2. Edit `etl/config.py` — add file path
3. Run `python run_etl.py`
4. Run `python run_dashboard.py` to view

## 📊 Dashboard Pages
1. 🏥 Providers
2. 👨‍👩‍👧 Foster Care
3. 📈 Census Data
4. ⚖️ Grievances & Appeals
5. 🧠 Depression Prevalence
6. 🧾 Core Set Measures
7. 💊 MAT Utilization

## ❓ Troubleshooting

**Dashboard won't start?**
- Check if port 8501 is in use
- Stop with Ctrl+C and retry

**Missing data in dashboard?**
- Run ETL first: `python run_etl.py`
- Check `etl.log` for errors

**Import errors?**
- Delete and re-run (auto-installs dependencies)
- Or manually: `pip install pandas streamlit plotly openpyxl pandera polars`

---
For full documentation, see [README.md](README.md)
