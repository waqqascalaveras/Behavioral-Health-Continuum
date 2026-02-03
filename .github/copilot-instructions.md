# Copilot Instructions for Behavioral Health ETL Project

## Project Overview
- This project is a modular ETL pipeline for preparing data for Tableau dashboards.
- The ETL process is organized under the `etl/` directory, with each step (config, download, process, export, logging) as a separate module.
- The main entry point for the ETL pipeline is `etl/main.py`.
- The pipeline is designed for maintainability, error reporting, and extensibility.

## Key Components
- `etl/config.py`: Defines data sources and output configuration. Update this file to add or change data sources.
- `etl/logger.py`: Sets up logging to both file and console. All modules use this for consistent logging.
- `etl/download.py`: Handles downloading or loading data from URLs or local files.
- `etl/process.py`: Contains data cleaning, validation, and transformation logic. Extend this for new processing steps.
- `etl/export.py`: Exports processed data to Excel for Tableau.
- `etl/main.py`: Orchestrates the ETL workflow.

## Usage & Workflows
- To run the pipeline, use:
  ```
  python -m etl.main
  ```
  or
  ```
  py -m etl.main
  ```
- Edit `etl/config.py` to configure data sources.
- Check `etl.log` for detailed logs and error reports after running the pipeline.

## Project Conventions
- Each ETL step is a separate module for clarity and testability.
- Logging is centralized via `etl/logger.py`.
- Add new data sources in `config.py` and new processing logic in `process.py`.
- All exports are handled in `export.py` for consistency.

## Extending the Pipeline

## ETL & Analysis Next Steps (2026)
- Add schema and cleaning logic for all new files using discovery_report.md
- Implement automated data quality checks and reporting (`etl/data_quality.py`)
- Integrate datasets for cross-source analysis (`etl/integrate.py`)
- Add feature engineering for derived columns and time-based analysis
- Build summary statistics and visualizations in `src/analytics` and `src/visualization`
- Ensure exports are clean and documented for Tableau/Power BI
- Update documentation and automate ETL runs (scheduled tasks, CLI options)

## References
- See `etl/README.md` for more details and examples.
- The `src/` directory appears to contain additional analytics, dashboards, and utility code, but the primary ETL workflow is in `etl/`.

---
For questions or unclear patterns, review `etl/README.md` or consult the main ETL modules for examples.
