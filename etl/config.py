# etl/config.py
"""
Configuration for ETL pipeline: data sources, output paths, and validation rules.
"""
import os
from typing import Dict

BASE_DIR = os.path.dirname(__file__)
DOWNLOADS_DIR = os.path.join(BASE_DIR, "downloads")


DATA_SOURCES: Dict[str, str] = {
        # 16. Profile of Enrolled Medi-Cal Fee-for-Service Providers
        'ffs_providers_profile': os.path.join(DOWNLOADS_DIR, 'medi-cal-ffs-provider-listing_1_26_26.csv'),
        # 17. Medi-Cal Managed Care Provider Listing
        'managed_care_provider_listing': 'manual:https://data.chhs.ca.gov/dataset/medi-cal-managed-care-provider-listing/resource/xxxx-xxxx.csv',
        # 18. Licensed Mental Health Rehabilitation Centers (MHRC) and Psychiatric Health Facilities (PHF)
        'mhrc_phf_facilities': 'manual:https://data.chhs.ca.gov/dataset/licensed-mental-health-rehabilitation-centers-mhrc-and-psychiatric-health-facilities-phf/resource/xxxx-xxxx.csv',
        # 19. ACEs Aware Clinician Listing
        'aces_aware_clinicians': 'manual:https://data.chhs.ca.gov/dataset/aces-aware-clinician-listing/resource/xxxx-xxxx.csv',
        # 20. Dental Utilization Measures by County
        'dental_utilization_by_county': 'manual:https://data.chhs.ca.gov/dataset/dental-utilization-measures-and-sealant-data-by-county-ethnicity-age/resource/xxxx-xxxx.csv',
        # 21. Core Set Measures for Mental Health
        'core_set_measures_mental_health': 'manual:https://data.chhs.ca.gov/dataset/core-set-measures-for-mental-health/resource/xxxx-xxxx.csv',
        # 22. Homeless Student Enrollment by Dwelling Type
        'homeless_student_enrollment': 'manual:https://www.cde.ca.gov/ds/ad/filessp.asp',
        # 23. Student Enrollment by Demographics
        'student_enrollment_demographics': 'manual:https://dq.cde.ca.gov/dataquest/',
        # 24. Chronic Absenteeism Data
        'chronic_absenteeism': 'manual:https://www.cde.ca.gov/ds/ad/filesabd.asp',
        # 25. HUD PIT Count by CoC
        'hud_pit_count': 'manual:https://www.hudexchange.info/resource/3031/pit-and-hic-data-since-2007/',
        # 26. Housing Inventory Count (HIC)
        'hud_hic': 'manual:https://www.hudexchange.info/resource/3031/pit-and-hic-data-since-2007/',
        # 27. Arrest Statistics (OpenJustice Portal)
        'arrest_statistics': 'manual:https://openjustice.doj.ca.gov/exploration/crime-statistics',
        # 28. Criminal Justice Profiles
        'criminal_justice_profiles': 'manual:https://openjustice.doj.ca.gov/',
        # 29. Recidivism Rates (CDCR)
        'cdcr_recidivism_rates': 'manual:https://www.cdcr.ca.gov/research/recidivism/',
        # 30. Incompetent to Stand Trial (IST) Data
        'incompetent_to_stand_trial': 'manual:https://www.courts.ca.gov/',
        # 31. Child Maltreatment Rates (CCWIP)
        'child_maltreatment_rates': 'manual:https://ccwip.berkeley.edu/',
        # 32. Foster Care Entries/Exits (CCWIP)
        'foster_care_entries_exits': os.path.join(DOWNLOADS_DIR, 'CFSR4_R04-Northern Region_Oct2025_25Q2.xlsx'),
        # 33. ACS 5-Year Estimates
        'acs_5yr_estimates': os.path.join(DOWNLOADS_DIR, 'DECENNIALPL2020.P1-2026-01-31T003932.xlsx'),
        # 34. Emergency Department Data (OSHPD)
        'oshpd_ed_data': 'manual:https://data.chhs.ca.gov/dataset/ed-visit-data',
        # 35. Hospital Discharge Data (OSHPD)
        'oshpd_hospital_discharge': 'manual:https://data.chhs.ca.gov/',
        # 36. CalEnviroScreen 4.0
        'calenviroscreen_4': 'manual:https://oehha.ca.gov/calenviroscreen/report/calenviroscreen-40',
        # 37. CHIS Public Use Files
        'chis_public_use': 'manual:https://healthpolicy.ucla.edu/chis/data/Pages/overview.aspx',
        # 38. NSDUH (SAMHSA)
        'nsduh': os.path.join(DOWNLOADS_DIR, 'NSDUH_2024.RData'),
        # 39. TEDS (SAMHSA)
        'teds': 'manual:https://www.samhsa.gov/data/data-we-collect/teds',
        # 40. Behavioral Health Quality Measures (CMS)
        'cms_bh_quality_measures': 'manual:https://www.medicaid.gov/medicaid/quality-of-care/',
        # 41. Vital Statistics (CDPH)
        'cdph_vital_statistics': 'manual:https://www.cdph.ca.gov/Programs/CHSI/Pages/Data-and-Statistics.aspx',
        # 42. Communicable Disease Surveillance (CDPH)
        'cdph_communicable_disease': 'manual:https://www.cdph.ca.gov/Programs/CID/DCDC/Pages/IDB.aspx',
    # 1. Behavioral Health Program Performance Data
    'behavioral_health_performance': 'manual:https://behavioralhealth-data.dhcs.ca.gov/api/views/xxxx-xxxx/rows.csv?accessType=DOWNLOAD',
    # 2. Mental Health Services Dashboard - Adult Demographics
    'mhs_dashboard_adult': 'manual:https://behavioralhealth-data.dhcs.ca.gov/api/views/xxxx-xxxx/rows.csv?accessType=DOWNLOAD',
    # 3. Mental Health Services Dashboard - Children & Youth Demographics
    'mhs_dashboard_youth': 'manual:https://behavioralhealth-data.dhcs.ca.gov/api/views/xxxx-xxxx/rows.csv?accessType=DOWNLOAD',
    # 4. Katie A. Specialty Mental Health Services
    'katie_a_specialty_mh': 'manual:https://data.chhs.ca.gov/dataset/katie-a-specialty-mental-health-datasets/resource/xxxx-xxxx.csv',
    # 5. Medication-Assisted Treatment for Opioid Use Disorders
    'mat_opioid_use_disorder': 'manual:https://data.chhs.ca.gov/dataset/medication-assisted-treatment-mat-in-medi-cal-for-opioid-use-disorders-county/resource/xxxx-xxxx.csv',
    # 6. Licensed Narcotic Treatment Programs
    'narcotic_treatment_programs': 'manual:https://data.chhs.ca.gov/dataset/licensed-narcotic-treatment-programs/resource/xxxx-xxxx.csv',
    # 7. SUD Recovery Treatment Facilities
    'sud_recovery_facilities': os.path.join(DOWNLOADS_DIR, 'SUD_Recovery_Treatment_Facilities.csv'),
    'sud_recovery_facilities_geojson': os.path.join(DOWNLOADS_DIR, 'SUD_Recovery_Treatment_Facilities.geojson'),
    'sud_recovery_facilities_geojson': 'etl/downloads/SUD_Recovery_Treatment_Facilities.geojson',
    # 8. Licensed DUI Provider Directory
    'dui_provider_directory': 'manual:https://data.chhs.ca.gov/dataset/licensed-driving-under-the-influence-dui-provider-directory/resource/xxxx-xxxx.csv',
    # 9. Lanterman-Petris-Short (LPS) Act Data
    'lanterman_petris_short': 'manual:https://data.chhs.ca.gov/dataset/lps-act-data/resource/xxxx-xxxx.csv',
    # 10. Crisis Service Utilization (SMHS)
    'crisis_service_utilization': 'manual:https://behavioralhealth-data.dhcs.ca.gov/api/views/xxxx-xxxx/rows.csv?accessType=DOWNLOAD',
    # 11. Medi-Cal Managed Care Enrollment Report
    'managed_care_enrollment': 'manual:https://data.chhs.ca.gov/dataset/medi-cal-managed-care-enrollment-report/resource/xxxx-xxxx.csv',
    # 12. Medi-Cal Certified Eligible Counts by Zip Code and Sex
    'certified_eligible_by_zip_sex': 'manual:https://data.chhs.ca.gov/dataset/medi-cal-certified-eligible-counts-by-month-of-eligibility-zip-code-and-sex/resource/xxxx-xxxx.csv',
    # 13. Medi-Cal Annual Renewals by County
    'annual_renewals_by_county': 'manual:https://data.chhs.ca.gov/dataset/medi-cal-annual-renewals-by-county/resource/xxxx-xxxx.csv',
    # 14. Former Foster Youth Enrolled in Medi-Cal
    'former_foster_youth_enrolled': 'manual:https://data.chhs.ca.gov/dataset/former-foster-youth-enrolled-in-medi-cal-by-month/resource/xxxx-xxxx.csv',
    # 15. Eligible Individuals Under Age 21
    'eligible_under_21': 'manual:https://data.chhs.ca.gov/dataset/eligible-individuals-under-age-21-enrolled-in-medi-cal/resource/xxxx-xxxx.csv',
    # 43. Annual Beneficiary Grievance and Appeal Report (ABGAR)
    'abgar_grievances': os.path.join(DOWNLOADS_DIR, 'abgar', 'grievance-type-county-and-statewide.csv'),
    'abgar_appeals': os.path.join(DOWNLOADS_DIR, 'abgar', 'appeal-type-county-and-statewide.csv'),
    'abgar_expedited_appeals': os.path.join(DOWNLOADS_DIR, 'abgar', 'expedited-appeal-type-county-and-statewide.csv'),
    'abgar_noabd': os.path.join(DOWNLOADS_DIR, 'abgar', 'notice-of-adverse-benefit-determination-noabd-type-county-and-statewide.csv'),
    # 44. Adult Depression (LGHC - Let's Get Healthy California)
    'adult_depression_lghc': os.path.join(DOWNLOADS_DIR, 'lghc', 'adult-depression-lghc-indicator-24.csv'),
    # 45. Core Set Measures for Mental Health
    'core_set_mental_health': os.path.join(DOWNLOADS_DIR, 'coresetmeasures', 'mental-health-core-set-measure-rates-by-county.csv'),
    # 46. Medication-Assisted Treatment (MAT) for Opioid Use Disorders
    'mat_annual': os.path.join(DOWNLOADS_DIR, 'mat', 'medication-assisted-treatment-in-medi-cal-for-opioid-use-disorders-annually.csv'),
    'mat_quarterly': os.path.join(DOWNLOADS_DIR, 'mat', 'medication-assisted-treatment-in-medi-cal-for-opioid-use-disorders-quarterly-by-county.csv'),
    # 47. Tobacco & Cigarette Use Prevalence (CDPH)
    'cigarette_use_prevalence': os.path.join(DOWNLOADS_DIR, 'tobacco', 'data-cigarette-use-prevalence-in-adults.csv'),
    'tobacco_use_prevalence': os.path.join(DOWNLOADS_DIR, 'tobacco', 'data-tobacco-use-prevalence-in-adults.csv'),
    # 48. Lanterman-Petris-Short (LPS) Act Data
    'lanterman_petris_short_data': os.path.join(DOWNLOADS_DIR, 'lanterman', 'lanterman-petris-short-act-data.csv'),
    # 49. Crisis Service Utilization (OCW) - SMHS
    'crisis_service_utilization_ocw': os.path.join(DOWNLOADS_DIR, 'ocw_utilization.csv'),
    # 50. Medi-Cal Managed Care Enrollment Report
    'managed_care_enrollment_report': os.path.join(DOWNLOADS_DIR, 'medicalmanaged', 'medi-cal-managed-care-enrollment-report.csv'),
    # 51. NSUMHSS 2024 - National Survey of Substance Use and Mental Health Services Study
    'nsumhss_2024': os.path.join(DOWNLOADS_DIR, 'NSUMHSS', 'NSUMHSS_2024_R.rdata'),
}

OUTPUT_EXCEL = 'behavioral_health_dashboard_data.xlsx'
LOG_FILE = 'etl.log'
