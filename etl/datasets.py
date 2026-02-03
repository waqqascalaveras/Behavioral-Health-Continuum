# Dataset-specific processing and requirements for Calaveras Health Dashboard ETL
# This file documents custom cleaning, transformation, and validation logic for each dataset.
# Add notes for manual/restricted/local sources as needed.

DATASET_PROCESSING = {
    # Tobacco & Substance Use Prevention
    'cigarette_use_prevalence': {
        'processing': 'California adult cigarette use prevalence 1984-present. Standardize gender categories.',
        'notes': 'Source: CDPH. Historical trends with confidence intervals. Not county-specific.'
    },
    'tobacco_use_prevalence': {
        'processing': 'California adult tobacco use prevalence by demographic groups. Standardize demographic labels.',
        'notes': 'Source: CDPH. More recent data (2016+) with demographic breakdowns by race/ethnicity and gender.'
    },
    # Mental Health Crisis/Involuntary Holds
    'lanterman_petris_short_data': {
        'processing': 'LPS Act involuntary psychiatric holds by county. Standardize county names, categorize by hold type (5150/5250/5270/etc).',
        'notes': 'Source: DHCS. Annual data on emergency psychiatric commitments. County-level data available for Calaveras.'
    },
    # Crisis Services & Mental Health Utilization
    'crisis_service_utilization_ocw': {
        'processing': 'OCW crisis service utilization by county and demographic group. Parse fiscal year, aggregate by delivery system.',
        'notes': 'Source: DHCS SMHS. County-level mental health crisis service usage (phone, walk-in, etc). Includes Calaveras data.'
    },
    'managed_care_enrollment_report': {
        'processing': 'Medi-Cal managed care enrollment by county and plan type. Parse enrollment month (YYYY-MM), clean enrollee counts.',
        'notes': 'Source: DHCS. Monthly enrollment data 2007-present. Shows insurance access by county (includes Calaveras).'
    },
    'nsumhss_2024': {
        'processing': 'NSUMHSS RData file requires pyreadr. Extract individual-level substance use and mental health service data.',
        'notes': 'Source: SAMHSA. National survey data with state/substate indicators. RData format requires specialized parsing.'
    },
}



# Fill in each dataset as you implement custom logic in etl/process.py.
