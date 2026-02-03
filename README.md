# Behavioral Health ETL Pipeline

## Introduction

This project automates the acquisition, processing, validation, and export of behavioral health and Medi-Cal datasets for Calaveras County and California, and visualizes them in a Streamlit dashboard for analysis.

## How the Pipeline Works (End-to-End)

1. **Configure Data Sources**
   - `etl/config.py` defines all inputs and local file paths.
   - This pipeline does not download remote data automatically.

2. **Download / Load Data**
   - `etl/download.py` loads local files from `etl/downloads/` only.
   - Specialized logic handles Excel sheets, GeoJSON, RData, and special headers.

3. **Clean & Validate**
   - `etl/process_clean.py` applies dataset-specific cleaning rules.
   - Pandera schemas validate columns, data types, and missing values.
   - County filtering keeps Calaveras data and state totals when available.

4. **Quality Summaries**
   - Each dataset logs row counts, column lists, missing values, and samples.
   - This supports auditability and troubleshooting.

5. **Export Outputs**
   - `etl/export.py` writes clean datasets to:
     - CSV (`output_csv/`)
     - Parquet (`output_parquet/`)
     - SQLite (`output_data.sqlite`)
     - Excel (`behavioral_health_dashboard_data.xlsx`)

6. **Dashboard & Analytics**
   - `dashboards.py` reads exported CSVs and renders interactive visuals.
   - Pages include county vs. state comparisons when available.
   - Additional analytics can be built under `src/analytics/` and `src/visualization/`.

## Data Sources Integrated

The pipeline currently processes 11 non-empty datasets:

1. **Medi-Cal Fee-for-Service Providers** (146 providers) - Calaveras County
   - Complete provider directory with contact info, specialties, accessibility features
   - Geographic coordinates for mapping

2. **Foster Care & Family Services** (56 records) - Calaveras County
   - CFSR4 (Child and Family Services Review) data
   - Performance outcomes and metrics

3. **Census & Demographic Data** (71 data points) - Calaveras County
   - ACS 5-Year estimates for population characteristics

4. **ABGAR - Behavioral Health Grievances & Appeals** (162 records total) - Calaveras County
   - **Grievances** (72 records): Service quality complaints by category
   - **Appeals** (30 records): Beneficiary appeals and decisions
   - **Expedited Appeals** (30 records): Urgent appeal status
   - **NOABD** (30 records): Notices of Adverse Benefit Determination
   - Source: California Department of Health Care Services (DHCS)
   - Coverage: Specialty Mental Health Services (SMHS) for Medi-Cal
   - Fiscal years: FY1819, FY1920, FY2021

5. **Adult Depression Prevalence (LGHC)** (161 records) - California Statewide
   - Depression prevalence rates by demographics (age, sex, race/ethnicity, education, income)
   - Source: California Behavioral Risk Factor Surveillance Survey (BRFSS)
   - Years: 2012-2018
   - Stratified by demographics and socioeconomic factors

6. **Core Set Measures for Mental Health** (5,206 records) - California Statewide
   - Federal quality measures for mental health services
   - Includes numerator/denominator counts and performance rates
   - Years: 2020-2023

7. **Medication-Assisted Treatment (MAT) - Annual** (120 records) - Calaveras + Statewide
   - Annual MAT utilization for opioid use disorders
   - Treatments include Buprenorphine and Methadone
   - Years: 2010-2024

8. **Medication-Assisted Treatment (MAT) - Quarterly** (496 records) - Calaveras + Statewide
   - Quarterly MAT utilization for opioid use disorders
   - Treatments include Buprenorphine and Methadone
   - Years: 2010-2025

## Dashboard Pages

Interactive Streamlit dashboard with 7 pages:
  - 🏥 Providers: Medi-Cal Fee-for-Service providers
  - 👨‍👩‍👧 Foster Care: Family services and outcomes
  - 📈 Census Data: Demographic statistics
  - ⚖️ Grievances & Appeals: Behavioral health services complaints
  - 🧠 Depression Prevalence: Adult mental health trends
  - 🧾 Core Set Measures: Mental health quality measures (statewide)
  - 💊 MAT Utilization: Medication-assisted treatment (county vs state)

## Setup & Usage

### Prerequisites
- Python 3.8+ installed
- **No manual pip installs required** — All scripts auto-install missing dependencies on first run

### Quick Start

**Recommended: Use Launcher (easiest)**
```powershell
python launcher.py
```
- Interactive menu with numbered options
- Auto-installs dependencies (pandas, streamlit, plotly, etc.)
- Choose: ETL only, Dashboard only, or Both

**Or Run Directly:**
```powershell
# Dashboard only (opens browser automatically)
python run_dashboard.py

# ETL pipeline only (process data)
python run_etl.py
```

**Double-Click Support:**
- Windows: Double-click any `.py` launcher file
- Opens in terminal and runs automatically

### Data Setup & Pipeline Execution

1. **Configure Data Sources**
   - Manually download datasets into `etl/downloads/`.
   - Edit `etl/config.py` to point to local file paths for all datasets.
   - Use `etl/discover_files.py` to auto-summarize new files and update schemas in `etl/process_clean.py`.

2. **Run the Pipeline**
   - Use `launcher.py` (interactive menu) **or**
   - Run `python run_etl.py` directly
   - Exports to: CSV, Parquet, SQLite, Excel

3. **View Dashboard**
   - Use `launcher.py` (interactive menu) **or**
   - Run `python run_dashboard.py` directly
   - Opens browser at http://localhost:8501

### Advanced Usage

**Manual ETL Module Run:**
```powershell
python -m etl.main
```

**Data Quality & Integration:**
- Run `etl/data_quality.py` for automated quality checks
- Run `etl/integrate.py` to join/merge datasets

**Feature Engineering & Analysis:**
- Add derived columns in `etl/process_clean.py`
- Build custom analytics in `src/analytics/` and `src/visualization/`

## Directory Structure

**Main Entry Points:**
- `launcher.py` — **Recommended**: Interactive menu (ETL, Dashboard, or Both)
- `run_dashboard.py` — Launch Streamlit dashboard only
- `run_etl.py` — Run ETL pipeline only

**Core Modules:**
- `etl/` — ETL pipeline (config, download, process_clean, export, main)
- `dashboards.py` — Streamlit dashboard with 7 interactive pages
- `src/` — Analytics, configuration, and utility modules

**Data Directories:**
- `etl/downloads/` — Input files (manually downloaded)
- `output_csv/` — Processed CSV exports
- `output_parquet/` — Parquet format exports
- `output_data.sqlite` — SQLite database
- `behavioral_health_dashboard_data.xlsx` — Excel workbook

## Customization

**Adding New Datasets:**
1. Place file in `etl/downloads/`
2. Add entry to `etl/config.py`
3. Run `etl/discover_files.py` to generate schema
4. Update `etl/process_clean.py` with cleaning rules
5. Add visualization to `dashboards.py`

**Extending the Pipeline:**
- Dataset-specific rules: `etl/datasets.py`
- Cross-dataset integration: `etl/integrate.py`
- Analytics & metrics: `src/analytics/`
- Custom visualizations: `src/visualization/`

## Notes

- All launcher scripts (`launcher.py`, `run_dashboard.py`, `run_etl.py`) automatically install missing Python dependencies
- Dashboard opens at http://localhost:8501 (browser opens automatically)
- Press Ctrl+C to stop dashboard or ETL processes
- See `etl.log` for detailed ETL execution logs

## GitHub Synchronization

This workstation doesn't have Git installed, so we use a Python-based upload script:

```powershell
# Preview changes before uploading
python upload_to_github.py --dry-run

# Upload changes to GitHub
python upload_to_github.py
```

**Repository:** https://github.com/waqqascalaveras/Behavioral-Health-Continuum

See [GITHUB_UPLOAD_GUIDE.md](GITHUB_UPLOAD_GUIDE.md) for complete setup and usage instructions.

---
For detailed technical documentation, see `etl/README.md`
