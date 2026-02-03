# CHHS Dataset Catalogue Analysis - Behavioral Health Expansion

## Summary
**Total Behavioral Health Related Datasets Found: 407**

The CHHS catalogue contains extensive behavioral health and healthcare data. Below are recommendations for high-priority datasets to expand the current 6-dataset ETL pipeline for Calaveras County.

---

## 🔴 HIGH PRIORITY - Core Behavioral Health Data

These datasets directly relate to mental health, substance use, and behavioral health services:

### 1. **Annual Beneficiary Grievance and Appeal Report (ABGAR)**
- **Department:** Department of Health Care Services
- **Program:** Medi-Cal Behavioral Health Division
- **Relevance:** Direct Medi-Cal mental health services data
- **County Coverage:** Statewide with county-specific totals
- **Recommendation:** HIGH - Direct mental health services data

### 2. **Adult Population Performance Dashboard**
- **Department:** Department of Health Care Services
- **Program:** Mental Health Management and Performance Outcomes Reporting Branch
- **Relevance:** Mental health outcomes and performance metrics
- **Recommendation:** HIGH - Core behavioral health outcomes

### 3. **Adult Depression (LGHC Indicator)**
- **Department:** California Department of Public Health
- **Program:** Chronic Disease Surveillance and Research Branch (CDSRB)
- **Relevance:** Mental health prevalence data
- **Recommendation:** HIGH - Community mental health prevalence

### 4. **Adult Cigarette and Tobacco Use Prevalence**
- **Department:** California Department of Public Health
- **Program:** California Tobacco Control Program
- **Relevance:** Substance use (tobacco) prevalence
- **Link:** https://www.cdph.ca.gov/Programs/CCDPHP/DCDIC/CTCB/Pages/CaliforniaTobaccoControlBranch.aspx
- **Recommendation:** HIGH - Substance use data

---

## 🟡 MEDIUM PRIORITY - Medi-Cal & Healthcare Access

These support behavioral health by tracking healthcare provider infrastructure and insurance access:

### 5. **ALW Assisted Living Facilities**
- **Department:** Department of Health Care Services
- **Program:** DHCS
- **Relevance:** Medi-Cal-funded facilities (some provide behavioral health)
- **Link:** https://gis.dhcs.ca.gov/datasets/CADHCS::alw-assisted-living-facilities
- **Recommendation:** MEDIUM - Facility capacity planning

### 6. **ALW Care Coordination Agencies**
- **Department:** Department of Health Care Services
- **Program:** DHCS
- **Relevance:** Care coordination for vulnerable Medi-Cal populations
- **Link:** https://gis.dhcs.ca.gov/datasets/CADHCS::alw-care-coordination-agencies
- **Recommendation:** MEDIUM - Integrates with behavioral health services

### 7. **Workforce & Quality Incentive Program Performance**
- **Department:** Department of Health Care Services
- **Relevance:** Healthcare provider workforce and quality metrics
- **Frequency:** Quarterly
- **Recommendation:** MEDIUM - Provider quality and capacity data

### 8. **Medi-Cal Managed Care Organization (MCO) Data**
- **Relevance:** Tracks insurance access for populations served
- **Recommendation:** MEDIUM - Insurance enrollment and access

---

## 🟢 LOWER PRIORITY - Supporting Health Data

These provide broader context for behavioral health analysis:

### 9. **AHRQ Pediatric Quality Indicators for California Hospitals**
- **Department:** Department of Health Care Access and Information
- **Link:** https://hcai.ca.gov/data/healthcare-quality/ahrq-quality-indicators/#imi
- **Recommendation:** LOW - Hospital quality (relevance depends on pediatric focus)

### 10. **Asthma Prevalence / ED Visit Rates**
- **Department:** California Department of Public Health
- **Relevance:** Chronic disease prevalence as health outcomes context
- **Recommendation:** LOW - Contextual health data

### 11. **Insurance Affordability Programs (Covered California)**
- **Department:** Department of Health Care Services
- **Program:** Covered California
- **Relevance:** Insurance access (prerequisite for healthcare)
- **Recommendation:** LOW-MEDIUM - Insurance access context

---

## 📊 Action Plan

### Phase 1: Immediate Acquisition (Next Sprint)
1. **Annual Beneficiary Grievance and Appeal Report (ABGAR)**
   - Download URL: Search CHHS data portal for direct download link
   - Expected Format: CSV or Excel
   - County Granularity: County-specific data available

2. **Adult Depression (LGHC Indicator)**
   - Download URL: https://letsgethealthy.ca.gov/
   - Expected Format: CSV
   - County Granularity: County-level data

3. **Adult Cigarette and Tobacco Use Prevalence**
   - Download URL: CDPH website
   - Expected Format: CSV or Excel
   - County Granularity: County-level data

### Phase 2: Secondary Acquisition (Following Sprint)
4. **Workforce & Quality Incentive Program Performance**
   - Frequency: Quarterly updates
   - Format: Likely Excel or CSV
   - County Granularity: Statewide (verify county availability)

5. **Mental Health Services and Outcomes Data**
   - Search for "Medi-Cal behavioral health" datasets
   - Look for substance use treatment data
   - Crisis services and emergency mental health utilization

### Phase 3: Integration & Enhancement
- Add schema definitions for new datasets in `etl/process_clean.py`
- Create dataset-specific cleaning and filtering logic
- Extend dashboard with new behavioral health metrics pages
- Implement cross-dataset analysis (e.g., correlate depression with SUD facility access)

---

## 🔗 Data Portal Access

All CHHS datasets are available through:
1. **CHHS Open Data Portal:** https://data.chhs.ca.gov/
2. **California Health Dashboard:** https://www.cdph.ca.gov/
3. **DHCS Data Portal:** https://gis.dhcs.ca.gov/
4. **Healthcare Analytics:** https://hcai.ca.gov/data/

---

## 📝 Next Steps

1. **Verify Download URLs:** Search CHHS portal for exact download links for Phase 1 datasets
2. **Assess Data Quality:** Confirm county-level data availability for Calaveras County
3. **Check Update Frequency:** Determine how often each dataset is refreshed
4. **Map Column Names:** Document expected column names and data types for new datasets
5. **Update config.py:** Add new data sources with download URLs
6. **Extend Schemas:** Add pandera schemas for validation
7. **Test ETL:** Run pipeline with new datasets

---

## 📌 Notes

- The CHHS catalogue contains **407 behavioral health-related datasets** across 23+ departments
- Most relevant data comes from: **DHCS**, **CDPH**, **HCAI**
- Data granularity varies: statewide, regional, county, facility, and provider levels
- Update frequencies range from: quarterly to annually to "other"
- All data should be available at county level (verify for Calaveras)
- Consider linking to Census ACS data for demographic context

---

*Generated from CHHS dataset-catalog analysis*
*Last updated: 2026-01*
