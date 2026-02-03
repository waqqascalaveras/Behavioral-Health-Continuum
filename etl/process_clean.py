# etl/process_clean.py
"""
Clean processing, cleaning, and validation functions for ETL pipeline.
"""

from typing import Dict

import pandas as pd
import pandera.pandas as pa
from pandera.pandas import DataFrameSchema, Column
from rich.console import Console
from rich.table import Table

from .datasets import DATASET_PROCESSING
from .logger import get_logger

logger = get_logger('etl.process')
console = Console()


def validate_and_summarize(dfs: Dict[str, pd.DataFrame]) -> None:
    """
    Print/log summary stats and show pretty tables for each DataFrame.
    """
    for key, df in dfs.items():
        logger.info(f"--- {key} ---")
        logger.info(f"Rows: {len(df)} | Columns: {list(df.columns)}")
        table = Table(title=f"{key} (first 5 rows)")
        if not df.empty:
            for col in df.columns:
                table.add_column(str(col))
            for _, row in df.head(5).iterrows():
                table.add_row(*[str(x) for x in row.values])
            missing = df.isnull().sum()
            logger.info(f"Missing values:\n{missing}")
            try:
                logger.info(f"Describe:\n{df.describe(include='all')}")
            except (KeyboardInterrupt, Exception) as e:
                logger.info(f"Describe skipped: {type(e).__name__}")
        else:
            logger.warning(f"{key} is empty!")
            table.add_column("No data")
            table.add_row("")
        console.print(table)


def _schemas() -> Dict[str, DataFrameSchema]:
    return {
        'behavioral_health_performance': DataFrameSchema({
            'county': Column(str, nullable=True),
        }, coerce=True),
        'mhs_dashboard_adult': DataFrameSchema({
            'county': Column(str, nullable=True),
        }, coerce=True),
        'mhs_dashboard_youth': DataFrameSchema({
            'county': Column(str, nullable=True),
        }, coerce=True),
        'katie_a_specialty_mh': DataFrameSchema({
            'county': Column(str, nullable=True),
        }, coerce=True),
        'mat_opioid_use_disorder': DataFrameSchema({
            'county': Column(str, nullable=True),
        }, coerce=True),
        'narcotic_treatment_programs': DataFrameSchema({
            'county': Column(str, nullable=True),
        }, coerce=True),
        'dui_provider_directory': DataFrameSchema({
            'county': Column(str, nullable=True),
        }, coerce=True),
        'lanterman_petris_short': DataFrameSchema({
            'county': Column(str, nullable=True),
        }, coerce=True),
        'crisis_service_utilization': DataFrameSchema({
            'county': Column(str, nullable=True),
        }, coerce=True),
        'managed_care_enrollment': DataFrameSchema({
            'county': Column(str, nullable=True),
        }, coerce=True),
        'certified_eligible_by_zip_sex': DataFrameSchema({
            'zip_code': Column(str, nullable=True),
        }, coerce=True),
        'annual_renewals_by_county': DataFrameSchema({
            'county': Column(str, nullable=True),
        }, coerce=True),
        'former_foster_youth_enrolled': DataFrameSchema({
            'county': Column(str, nullable=True),
        }, coerce=True),
        'eligible_under_21': DataFrameSchema({
            'county': Column(str, nullable=True),
        }, coerce=True),
        'abgar_grievances': DataFrameSchema({
            'Report Year': Column(str, nullable=True),
            'Geography': Column(str, nullable=True),
            'Grievance Category': Column(str, nullable=True),
            'Grievance Type': Column(str, nullable=True),
            'Grievance Count': Column(float, nullable=True),
            'Exempt Grievance Count': Column(float, nullable=True),
            'Unresolved as of June 30': Column(float, nullable=True),
            'Resolved': Column(float, nullable=True),
            'Referred': Column(float, nullable=True),
        }, coerce=True),
        'abgar_appeals': DataFrameSchema({
            'Report Year': Column(str, nullable=True),
            'Geography': Column(str, nullable=True),
            'Notice of Adverse Benefit Determination Category': Column(str, nullable=True),
            'Appeal Count': Column(float, nullable=True),
            'Unresolved as of June 30': Column(float, nullable=True),
            'Decision Upheld': Column(float, nullable=True),
            'Decision Overturned': Column(float, nullable=True),
        }, coerce=True),
        'abgar_expedited_appeals': DataFrameSchema({
            'Report Year': Column(str, nullable=True),
            'Geography': Column(str, nullable=True),
            'Notice of Adverse Benefit Determination Category': Column(str, nullable=True),
            'Expedited Appeal Count': Column(float, nullable=True),
            'Unresolved as of June 30': Column(float, nullable=True),
            'Decision Upheld': Column(float, nullable=True),
            'Decision Overturned': Column(float, nullable=True),
        }, coerce=True),
        'abgar_noabd': DataFrameSchema({
            'Report Year': Column(str, nullable=True),
            'Geography': Column(str, nullable=True),
            'Notice of Adverse Benefit Determination (NOABD) Category': Column(str, nullable=True),
            'Notice of Adverse Benefit Determination (NOABD) Issued': Column(float, nullable=True),
        }, coerce=True),
        'adult_depression_lghc': DataFrameSchema({
            'Year': Column(str, nullable=True),
            'Strata': Column(str, nullable=True),
            'Strata Name': Column(str, nullable=True),
            'Frequency': Column(float, nullable=True),
            'Weighted Frequency': Column(float, nullable=True),
            'Percent': Column(float, nullable=True),
            'Lower 95% CL': Column(float, nullable=True),
            'Upper 95% CL': Column(float, nullable=True),
        }, coerce=True),
        'core_set_mental_health': DataFrameSchema({
            'Measure_Year': Column(str, nullable=True),
            'Type': Column(str, nullable=True),
            'Measure': Column(str, nullable=True),
            'Category': Column(str, nullable=True),
            'Population': Column(str, nullable=True),
            'Numerator': Column(str, nullable=True),
            'Numerator_ANNOT': Column(str, nullable=True),
            'Denominator': Column(str, nullable=True),
            'Denominator_ANNOT': Column(str, nullable=True),
            'Rate': Column(str, nullable=True),
            'Rate_ANNOT': Column(str, nullable=True),
        }, coerce=True),
        'mat_annual': DataFrameSchema({
            'County': Column(str, nullable=True),
            'Year': Column(str, nullable=True),
            'Medication_Assisted_Treatment': Column(str, nullable=True),
            'members': Column(str, nullable=True),
            'status': Column(str, nullable=True),
            'annotation': Column(str, nullable=True),
            'annotation_description': Column(str, nullable=True),
        }, coerce=True),
        'mat_quarterly': DataFrameSchema({
            'County': Column(str, nullable=True),
            'Year': Column(str, nullable=True),
            'Quarter': Column(str, nullable=True),
            'Medication_Assisted_Treatment': Column(str, nullable=True),
            'members': Column(str, nullable=True),
            'status': Column(str, nullable=True),
            'annotation': Column(str, nullable=True),
            'annotation_description': Column(str, nullable=True),
        }, coerce=True),
        'ffs_providers_profile': DataFrameSchema({
            'OBJECTID': Column(int, nullable=True),
            'Provider_Source': Column(str, nullable=True),
            'Provider_Number': Column(str, nullable=True),
            'NPI': Column(str, nullable=True),
            'Owner_Number': Column(str, nullable=True),
            'Service_Location_Number': Column(str, nullable=True),
            'Legal_Name': Column(str, nullable=True),
            'Enroll_Status_Eff_DT': Column(str, nullable=True),
            'Provider_Taxonomy': Column(str, nullable=True),
            'NEMT_NMT_Provider_Type': Column(str, nullable=True),
            'ANC_Provider_Type': Column(str, nullable=True),
            'FI_Provider_Type_CD': Column(str, nullable=True),
            'FI_Provider_Type': Column(str, nullable=True),
            'Provider_License': Column(str, nullable=True),
            'FI_Provider_Specialty_CD': Column(str, nullable=True),
            'FI_Provider_Specialty': Column(str, nullable=True),
            'Out_of_State_Indicator': Column(str, nullable=True),
            'In_Out_State': Column(str, nullable=True),
            'Address_Attention': Column(str, nullable=True),
            'Address': Column(str, nullable=True),
            'Address2': Column(str, nullable=True),
            'City': Column(str, nullable=True),
            'State': Column(str, nullable=True),
            'ZIP': Column(str, nullable=True),
            'ZIP_4': Column(str, nullable=True),
            'DHCS_County_CD': Column(str, nullable=True),
            'FIPS_County_CD': Column(str, nullable=True),
            'County': Column(str, nullable=True),
            'Phone_Number': Column(str, nullable=True),
            'Medicaid_Patients': Column(str, nullable=True),
            'CHIP_Patients': Column(str, nullable=True),
            'Telehealth_Services': Column(str, nullable=True),
            'Provider_Website': Column(str, nullable=True),
            'Threshold_Languages': Column(str, nullable=True),
            'Other_Languages': Column(str, nullable=True),
            'Acc_Exam_Room': Column(str, nullable=True),
            'Acc_Exterior_Building': Column(str, nullable=True),
            'Acc_Interior_Building': Column(str, nullable=True),
            'Acc_Parking': Column(str, nullable=True),
            'Acc_Restroom': Column(str, nullable=True),
            'Acc_Medical_Equipment': Column(str, nullable=True),
            'Acc_Patient_Areas': Column(str, nullable=True),
            'Acc_Patient_Diagnostic': Column(str, nullable=True),
            'Latitude': Column(float, nullable=True),
            'Longitude': Column(float, nullable=True),
            'CountyName': Column(str, nullable=True),
        }, coerce=True),
        'acs_5yr_estimates': DataFrameSchema({
            'Label': Column(str, nullable=True),
            'Value': Column(float, nullable=True),
            'County': Column(str, nullable=True),
        }, coerce=True),
        'sud_recovery_facilities': DataFrameSchema({
            'OBJECTID': Column(int, nullable=True),
            'County_Code': Column(str, nullable=True),
            'Legal_Entity_Name': Column(str, nullable=True),
            'Facility_Name': Column(str, nullable=True),
            'Facility_City': Column(str, nullable=True),
            'Facility_State': Column(str, nullable=True),
            'Facility_Zip': Column(str, nullable=True),
            'Type_of_Application': Column(str, nullable=True),
            'Program_Code': Column(str, nullable=True),
            'Treatment_Capacity': Column(int, nullable=True),
            'Total_Capacity': Column(int, nullable=True),
            'Expiration_Date': Column(str, nullable=True),
            'Target_Population': Column(str, nullable=True),
            'Incident_Medical_Services': Column(str, nullable=True),
            'Adolescent_Waiver': Column(str, nullable=True),
            'Latitude': Column(float, nullable=True),
            'Longitude': Column(float, nullable=True),
            'CountyName': Column(str, nullable=True),
        }, coerce=True),
        'sud_recovery_facilities_geojson': DataFrameSchema({
            'OBJECTID': Column(int, nullable=True),
            'County_Code': Column(str, nullable=True),
            'Legal_Entity_Name': Column(str, nullable=True),
            'Facility_Name': Column(str, nullable=True),
            'Facility_City': Column(str, nullable=True),
            'Facility_State': Column(str, nullable=True),
            'Facility_Zip': Column(str, nullable=True),
            'Type_of_Application': Column(str, nullable=True),
            'Program_Code': Column(str, nullable=True),
            'Treatment_Capacity': Column(int, nullable=True),
            'Total_Capacity': Column(int, nullable=True),
            'Expiration_Date': Column(str, nullable=True),
            'Target_Population': Column(str, nullable=True),
            'Incident_Medical_Services': Column(str, nullable=True),
            'Adolescent_Waiver': Column(str, nullable=True),
            'Latitude': Column(float, nullable=True),
            'Longitude': Column(float, nullable=True),
            'CountyName': Column(str, nullable=True),
        }, coerce=True),
        'foster_care_entries_exits': DataFrameSchema({
            'Measure number': Column(str, nullable=True),
            'Measure description': Column(str, nullable=True),
            'Most recent start date': Column(str, nullable=True),
            'Most recent end date': Column(str, nullable=True),
            'Most recent numerator': Column(float, nullable=True),  # Changed to float to handle NaN
            'Most recent denominator': Column(float, nullable=True),  # Changed to float to handle NaN
            'Most recent performance': Column(float, nullable=True),
            'National performance or goal': Column(str, nullable=True),
            'Desired direction': Column(str, nullable=True),
            'Actual \none-year direction': Column(str, nullable=True),
            'One-year percent change': Column(float, nullable=True),
            'External Links to CCWIP Online Reports': Column(str, nullable=True),
        }, coerce=True),
        'nsduh': DataFrameSchema({
            # RData: schema not implemented, recommend pyreadr
        }),
        'cigarette_use_prevalence': DataFrameSchema({
            'YEAR': Column(int, nullable=True),
            'COMPARISON': Column(str, nullable=True),
            'GENDER': Column(str, nullable=True),
            'PERCENT': Column(float, nullable=True),
            'LOWER95': Column(float, nullable=True),
            'UPPER95': Column(float, nullable=True),
        }, coerce=True),
        'tobacco_use_prevalence': DataFrameSchema({
            'YEAR': Column(int, nullable=True),
            'DEMOGRAPHIC': Column(str, nullable=True),
            'PERCENT': Column(str, nullable=True),  # Can be numeric or '*' (suppressed)
            'SE': Column(str, nullable=True),       # Can be numeric or '*' (suppressed)
            'LOWER95': Column(str, nullable=True),  # Can be numeric or '*' (suppressed)
            'UPPER95': Column(str, nullable=True),  # Can be numeric or '*' (suppressed)
        }, coerce=True),
        'lanterman_petris_short_data': DataFrameSchema({
            'RPT_YEAR': Column(int, nullable=True),
            'COUNTY': Column(str, nullable=True),
            'CATEGORY': Column(str, nullable=True),
            'AMOUNT_TYPE': Column(str, nullable=True),
            'AMOUNT_DESC': Column(str, nullable=True),
            'AMOUNT': Column(float, nullable=True),
            'AMOUNT_ANNOT': Column(str, nullable=True),
        }, coerce=True),
        'crisis_service_utilization_ocw': DataFrameSchema({
            'Health Care Delivery System': Column(str, nullable=True),
            'Health Care Delivery System Id': Column(str, nullable=True),
            'Fiscal Year': Column(int, nullable=True),
            'Demographic Group': Column(str, nullable=True),
            'MH Service Description': Column(str, nullable=True),
            'Units': Column(str, nullable=True),
            'Amount MH Service Received': Column(float, nullable=True),
            'Amount MH Service Received Suppression Identifier': Column(str, nullable=True),
            'Medi-Cal Delivery System': Column(str, nullable=True),
            'Population Category': Column(str, nullable=True),
            'Demographic Category': Column(str, nullable=True),
        }, coerce=True),
        'managed_care_enrollment_report': DataFrameSchema({
            'Enrollment Month': Column(str, nullable=True),
            'Plan Type': Column(str, nullable=True),
            'County': Column(str, nullable=True),
            'Plan Name': Column(str, nullable=True),
            ' Count of Enrollees ': Column(float, nullable=True),
            'Count of Enrollees Annotation Code': Column(str, nullable=True),
            'Count of Enrollees Annotation Description': Column(str, nullable=True),
        }, coerce=True),
        'nsumhss_2024': DataFrameSchema({
            # RData: schema not implemented, recommend pyreadr
        }),
    }


def process_all(dfs: Dict[str, pd.DataFrame]) -> Dict[str, pd.DataFrame]:
    """
    Standardize, clean, and validate datasets.
    """
    schemas = _schemas()

    for key, df in dfs.items():
        if 'county' in df.columns:
            df['county'] = df['county'].astype(str).str.title()
        if 'CountyName' in df.columns:
            df['CountyName'] = df['CountyName'].astype(str).str.title()

        if 'zip_code' in df.columns:
            df['zip_code'] = df['zip_code'].astype(str).str.zfill(5)
        if 'Facility_Zip' in df.columns:
            df['Facility_Zip'] = pd.to_numeric(df['Facility_Zip'], errors='coerce').apply(
                lambda x: str(int(x)).zfill(5) if pd.notna(x) else None
            )
        if 'ZIP' in df.columns:
            df['ZIP'] = pd.to_numeric(df['ZIP'], errors='coerce').apply(
                lambda x: str(int(x)).zfill(5) if pd.notna(x) else None
            )

        if 'Latitude' in df.columns:
            df['Latitude'] = pd.to_numeric(df['Latitude'], errors='coerce')
        if 'Longitude' in df.columns:
            df['Longitude'] = pd.to_numeric(df['Longitude'], errors='coerce')

        if key == 'ffs_providers_profile':
            if 'County' in df.columns:
                df['County'] = df['County'].astype(str).str.title()
            if 'CountyName' in df.columns:
                df['CountyName'] = df['CountyName'].astype(str).str.title()
            if 'City' in df.columns:
                df['City'] = df['City'].astype(str).str.title()
            if 'ZIP_4' in df.columns:
                df['ZIP_4'] = pd.to_numeric(df['ZIP_4'], errors='coerce').apply(
                    lambda x: str(int(x)).zfill(4) if pd.notna(x) else None
                )
            if 'Phone_Number' in df.columns:
                df['Phone_Number'] = pd.to_numeric(df['Phone_Number'], errors='coerce').apply(
                    lambda x: str(int(x)) if pd.notna(x) else None
                )
            if 'Enroll_Status_Eff_DT' in df.columns:
                df['Enroll_Status_Eff_DT'] = pd.to_datetime(df['Enroll_Status_Eff_DT'], errors='coerce')

        if key == 'acs_5yr_estimates':
            if len(df.columns) >= 2:
                label_col = df.columns[0]
                value_col = df.columns[1]
                county_name = str(value_col).split(',')[0].strip()
                df = df.rename(columns={label_col: 'Label', value_col: 'Value'})
                df['Value'] = df['Value'].astype(str).str.replace(',', '', regex=False)
                df['Value'] = pd.to_numeric(df['Value'], errors='coerce')
                df['County'] = county_name
                df = df[df['Label'].notna()]

        if key == 'foster_care_entries_exits':
            if 'Measure number' not in df.columns:
                header_row = None
                for idx, row in df.iterrows():
                    if row.astype(str).str.contains('Measure number', case=False, na=False).any():
                        header_row = idx
                        break
                if header_row is not None:
                    df.columns = df.loc[header_row]
                    df = df.loc[header_row + 1:].reset_index(drop=True)
            if 'Most recent numerator' in df.columns:
                df['Most recent numerator'] = pd.to_numeric(df['Most recent numerator'], errors='coerce')
            if 'Most recent denominator' in df.columns:
                df['Most recent denominator'] = pd.to_numeric(df['Most recent denominator'], errors='coerce')
            if 'Most recent performance' in df.columns:
                df['Most recent performance'] = pd.to_numeric(df['Most recent performance'], errors='coerce')

        if key in ('sud_recovery_facilities', 'sud_recovery_facilities_geojson'):
            if 'County_Code' in df.columns:
                df['County_Code'] = pd.to_numeric(df['County_Code'], errors='coerce').apply(
                    lambda x: str(int(x)).zfill(2) if pd.notna(x) else None
                )
            if 'Expiration_Date' in df.columns:
                df['Expiration_Date'] = pd.to_datetime(df['Expiration_Date'], errors='coerce')
            if 'Facility_City' in df.columns:
                df['Facility_City'] = df['Facility_City'].astype(str).str.title()
            if 'CountyName' in df.columns:
                df['CountyName'] = df['CountyName'].astype(str).str.title()

        if key == 'sud_recovery_facilities':
            if 'Treatment_Capacity' in df.columns and 'Total_Capacity' in df.columns:
                df['Capacity_Utilization'] = (df['Treatment_Capacity'] / df['Total_Capacity']).round(2)
            if 'Expiration_Date' in df.columns:
                df['Expiration_Year'] = df['Expiration_Date'].dt.year
            if 'Total_Capacity' in df.columns:
                df['Large_Facility'] = df['Total_Capacity'] > 50

        if key == 'foster_care_entries_exits':
            if 'Most recent numerator' in df.columns and 'Most recent denominator' in df.columns:
                df['Rate'] = (df['Most recent numerator'] / df['Most recent denominator']).round(4)
            if 'One-year percent change' in df.columns:
                # Convert percentage strings to numeric (e.g., "5.2%" -> 0.052)
                def parse_percentage(val):
                    if pd.isna(val):
                        return None
                    if isinstance(val, (int, float)):
                        return val
                    # Remove % and convert to decimal
                    try:
                        return float(str(val).strip().rstrip('%')) / 100
                    except (ValueError, AttributeError):
                        return None
                
                df['One-year percent change'] = df['One-year percent change'].apply(parse_percentage)
                df['OneYearChangeFlag'] = df['One-year percent change'].apply(lambda x: abs(x) > 0.05 if pd.notna(x) else False)
        # Core Set Mental Health - skip first title row
        if key == 'core_set_mental_health':
            # Remove % signs and convert to float
            if 'Rate' in df.columns:
                df['Rate'] = df['Rate'].astype(str).str.rstrip('%')
            # Remove commas from numbers
            for col in ['Numerator', 'Denominator']:
                if col in df.columns:
                    df[col] = df[col].astype(str).str.replace(',', '')

        # MAT datasets - convert members to numeric, handle suppressed values
        if key in ['mat_annual', 'mat_quarterly']:
            if 'members' in df.columns:
                # Convert to numeric, suppressed values become NaN
                df['members'] = pd.to_numeric(df['members'], errors='coerce')
            if 'Year' in df.columns:
                df['Year'] = df['Year'].astype(str)


        # Only validate schemas for non-empty datasets
        if key in schemas and len(df) > 0:
            try:
                df = schemas[key].validate(df, lazy=True)
            except pa.errors.SchemaErrors as e:
                logger.error(f"Schema validation failed for {key}: {e.failure_cases}")

        if key in DATASET_PROCESSING:
            notes = DATASET_PROCESSING[key].get('notes', '')
            logger.info(f"Processing notes for {key}: {notes}")

        # Filter to Calaveras County only
        df = _filter_by_county(df, key)
        
        dfs[key] = df

    return dfs


def _filter_by_county(df: pd.DataFrame, dataset_key: str) -> pd.DataFrame:
    """Filter datasets to Calaveras County and State-level comparison data."""
    if len(df) == 0:
        return df
    
    # Map of dataset keys to their county column names and acceptable values
    # Include 'State' to keep state-level comparison data
    county_filters = {
        'ffs_providers_profile': ('County', ['Calaveras']),
        'acs_5yr_estimates': ('County', ['Calaveras', 'Calaveras County']),
        'sud_recovery_facilities': ('CountyName', ['Calaveras']),
        'sud_recovery_facilities_geojson': ('CountyName', ['Calaveras']),
        'abgar_grievances': ('Geography', ['Calaveras', 'State']),
        'abgar_appeals': ('Geography', ['Calaveras', 'State']),
        'abgar_expedited_appeals': ('Geography', ['Calaveras', 'State']),
        'abgar_noabd': ('Geography', ['Calaveras', 'State']),
        'mat_annual': ('County', ['Calaveras', 'Statewide']),
        'mat_quarterly': ('County', ['Calaveras', 'Statewide']),
    }
    
    if dataset_key not in county_filters:
        return df  # No county filter for this dataset
    
    county_col, acceptable_values = county_filters[dataset_key]
    
    if county_col not in df.columns:
        logger.warning(f"County column '{county_col}' not found in {dataset_key}")
        return df
    
    # Filter to acceptable county values
    before_count = len(df)
    df_filtered = df[df[county_col].isin(acceptable_values)].copy()
    after_count = len(df_filtered)
    
    if before_count != after_count:
        logger.info(f"[CALAVERAS FILTER] {dataset_key}: {before_count:,} -> {after_count:,} rows")
    
    return df_filtered
