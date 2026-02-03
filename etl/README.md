# Behavioral Health ETL Pipeline

This modular ETL pipeline downloads, processes, validates, and exports data for Tableau dashboards. It uses best practices for maintainability, error reporting, and extensibility.

## Structure
- `config.py`: Data source and output configuration
- `logger.py`: Logging setup (file + console)
- `download.py`: Download/load data from URLs or local files
- `process.py`: Data cleaning, validation, and transformation
- `export.py`: Export to Excel for Tableau
- `main.py`: Pipeline entry point

## Usage
1. Edit `etl/config.py` to set your data sources (URLs or local paths).
2. Run the pipeline:
   ```powershell
   py -m etl.main
   ```
   or
   ```powershell
   python -m etl.main
   ```
3. Check `etl.log` for detailed logs and error reports.
4. Import the generated Excel file into Tableau.

## Features
- Modular, testable code
- Handles both local and remote data
- Logs all steps and errors to file and console
- Validates and summarizes each dataset
- Easy to extend for new features or data sources

## Customization
- Add your data processing logic in `process.py`
- Add new data sources in `config.py`
- Improve validation or add new exports as needed
