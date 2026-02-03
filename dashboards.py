"""
Interactive Behavioral Health Dashboard for Calaveras County
Uses Streamlit to display visualizations from cleaned ETL data
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from pathlib import Path
import os

# Page configuration
st.set_page_config(
    page_title="Calaveras County Behavioral Health Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main { padding: 2rem; }
    h1 { color: #1f77b4; }
    .metric-card { background-color: #f0f2f6; padding: 1.5rem; border-radius: 0.5rem; }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load cleaned datasets from CSV exports"""
    data_dir = Path("output_csv")
    
    dfs = {}
    last_updated = None
    
    # Load FFS Providers
    ffs_path = data_dir / "ffs_providers_profile.csv"
    if ffs_path.exists():
        dfs['ffs_providers'] = pd.read_csv(ffs_path)
        if last_updated is None or ffs_path.stat().st_mtime > last_updated:
            last_updated = ffs_path.stat().st_mtime
    
    # Load Foster Care
    fc_path = data_dir / "foster_care_entries_exits.csv"
    if fc_path.exists():
        dfs['foster_care'] = pd.read_csv(fc_path)
        if last_updated is None or fc_path.stat().st_mtime > last_updated:
            last_updated = fc_path.stat().st_mtime
    
    # Load ACS Census Data
    acs_path = data_dir / "acs_5yr_estimates.csv"
    if acs_path.exists():
        dfs['census'] = pd.read_csv(acs_path)
        if last_updated is None or acs_path.stat().st_mtime > last_updated:
            last_updated = acs_path.stat().st_mtime

    # Load Core Set Mental Health Measures
    core_set_path = data_dir / "core_set_mental_health.csv"
    if core_set_path.exists():
        dfs['core_set_mental_health'] = pd.read_csv(core_set_path)
        if last_updated is None or core_set_path.stat().st_mtime > last_updated:
            last_updated = core_set_path.stat().st_mtime

    # Load MAT Annual
    mat_annual_path = data_dir / "mat_annual.csv"
    if mat_annual_path.exists():
        dfs['mat_annual'] = pd.read_csv(mat_annual_path)
        if last_updated is None or mat_annual_path.stat().st_mtime > last_updated:
            last_updated = mat_annual_path.stat().st_mtime

    # Load MAT Quarterly
    mat_quarterly_path = data_dir / "mat_quarterly.csv"
    if mat_quarterly_path.exists():
        dfs['mat_quarterly'] = pd.read_csv(mat_quarterly_path)
        if last_updated is None or mat_quarterly_path.stat().st_mtime > last_updated:
            last_updated = mat_quarterly_path.stat().st_mtime
    
    # Load Cigarette Use Prevalence
    cigarette_path = data_dir / "cigarette_use_prevalence.csv"
    if cigarette_path.exists():
        dfs['cigarette_use'] = pd.read_csv(cigarette_path)
        if last_updated is None or cigarette_path.stat().st_mtime > last_updated:
            last_updated = cigarette_path.stat().st_mtime
    
    # Load Tobacco Use Prevalence
    tobacco_path = data_dir / "tobacco_use_prevalence.csv"
    if tobacco_path.exists():
        dfs['tobacco_use'] = pd.read_csv(tobacco_path)
        if last_updated is None or tobacco_path.stat().st_mtime > last_updated:
            last_updated = tobacco_path.stat().st_mtime
    
    # Load Lanterman-Petris-Short Act Data
    lanterman_path = data_dir / "lanterman_petris_short_data.csv"
    if lanterman_path.exists():
        dfs['lanterman'] = pd.read_csv(lanterman_path)
        if last_updated is None or lanterman_path.stat().st_mtime > last_updated:
            last_updated = lanterman_path.stat().st_mtime
    
    # Load Crisis Service Utilization (OCW)
    crisis_path = data_dir / "crisis_service_utilization_ocw.csv"
    if crisis_path.exists():
        dfs['crisis_services'] = pd.read_csv(crisis_path)
        if last_updated is None or crisis_path.stat().st_mtime > last_updated:
            last_updated = crisis_path.stat().st_mtime
    
    # Load Medi-Cal Managed Care Enrollment
    managed_care_path = data_dir / "managed_care_enrollment_report.csv"
    if managed_care_path.exists():
        dfs['managed_care'] = pd.read_csv(managed_care_path)
        if last_updated is None or managed_care_path.stat().st_mtime > last_updated:
            last_updated = managed_care_path.stat().st_mtime
    
    # Store last updated timestamp
    if last_updated:
        from datetime import datetime
        dfs['_last_updated'] = datetime.fromtimestamp(last_updated).strftime('%Y-%m-%d')
    
    return dfs

def show_ffs_providers_dashboard(df):
    """Visualize Medi-Cal FFS Providers"""
    st.header("🏥 Medi-Cal FFS Providers in Calaveras County")
    
    st.info("**Data Source:** California Department of Health Care Services (DHCS) - Medi-Cal Fee-for-Service Provider Directory")
    st.markdown("""
    This dashboard shows behavioral health and medical providers accepting Medi-Cal Fee-for-Service (FFS) in Calaveras County.
    Use this to understand provider capacity, specialties, and geographic distribution.
    """)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Providers", len(df))
    
    with col2:
        if 'Service_Area' in df.columns:
            st.metric("Service Areas", df['Service_Area'].nunique())
        else:
            st.metric("Counties", df['County'].nunique() if 'County' in df.columns else 0)
    
    provider_type_col = None
    for col in ['FI_Provider_Type', 'Provider_Taxonomy', 'FI_Provider_Specialty', 'ANC_Provider_Type', 'NEMT_NMT_Provider_Type']:
        if col in df.columns:
            provider_type_col = col
            break

    with col3:
        if 'FI_Provider_Specialty' in df.columns:
            spec_count = df['FI_Provider_Specialty'].nunique()
            st.metric("Specialties", spec_count)
        elif provider_type_col:
            type_count = df[provider_type_col].nunique()
            st.metric("Provider Types", type_count)
        else:
            st.metric("Provider Categories", len(df))
    
    with col4:
        if 'Phone_Number' in df.columns:
            st.metric("With Contact Info", df['Phone_Number'].notna().sum())
        else:
            st.metric("Records", len(df))
    
    # Provider Type Distribution
    st.subheader("Provider Distribution by Type")
    st.caption("Shows the top 10 provider types/specialties by count. This helps identify which services have the most available providers in Calaveras County.")
    if provider_type_col:
        provider_counts = df[provider_type_col].value_counts().head(10)
        fig = px.bar(
            x=provider_counts.values,
            y=provider_counts.index,
            orientation='h',
            labels={'x': 'Number of Providers', 'y': 'Provider Type'},
            color=provider_counts.values,
            color_continuous_scale='Viridis'
        )
        st.plotly_chart(fig, width='stretch')
    else:
        st.info("Provider type information not available in dataset")
    
    # Geographic Distribution
    st.subheader("Geographic Coverage")
    st.caption("Map showing physical locations of providers. Concentrations indicate service availability in different areas of the county.")
    if 'Latitude' in df.columns and 'Longitude' in df.columns:
        # Filter out invalid coordinates
        df_map = df.dropna(subset=['Latitude', 'Longitude'])
        df_map = df_map[(df_map['Latitude'] != 0) & (df_map['Longitude'] != 0)]
        
        if len(df_map) > 0:
            # Get hover text from available columns
            if 'Legal_Name' in df_map.columns:
                hover_text = df_map['Legal_Name'].astype(str)
            elif 'Provider_Number' in df_map.columns:
                hover_text = df_map['Provider_Number'].astype(str)
            else:
                hover_text = [f"Provider {i}" for i in range(len(df_map))]
            
            fig = go.Figure(data=go.Scattergeo(
                lon=df_map['Longitude'],
                lat=df_map['Latitude'],
                mode='markers',
                marker=dict(size=8, color='blue', opacity=0.6),
                text=hover_text,
                hoverinfo='text'
            ))
            fig.update_layout(
                title='Provider Locations',
                geo=dict(
                    scope='usa',
                    projection_type='albers usa',
                    showland=True,
                    landcolor='lightgray'
                ),
                height=500
            )
            st.plotly_chart(fig, width='stretch')
    
    # Data Table
    st.subheader("Provider Details")
    st.caption("First 20 providers with contact information for outreach and referrals.")
    # Define display columns based on what's available
    display_cols = ['Legal_Name', 'Address', 'City', 'Phone_Number']
    if provider_type_col:
        display_cols.insert(1, provider_type_col)
    display_cols = [col for col in display_cols if col in df.columns]
    if display_cols:
        st.dataframe(df[display_cols].head(20), width='stretch')
    else:
        st.dataframe(df.head(20), width='stretch')

def show_foster_care_dashboard(df):
    """Visualize Foster Care Data"""
    st.header("👨‍👩‍👧 Foster Care & Family Services")
    
    st.info("**Data Source:** Child and Family Services Reviews (CFSR4) - Performance Measures for Calaveras County")
    st.markdown("""
    This dashboard tracks foster care performance metrics including entries, exits, placement stability, and permanency outcomes.
    Federal measures assess how well the county child welfare system serves children and families.
    """)
    
    st.subheader("Key Metrics")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Records", len(df))
    
    with col2:
        if 'Most recent numerator' in df.columns:
            numerator = df['Most recent numerator'].sum()
            st.metric("Most Recent Numerator", f"{numerator:,.0f}")
    
    with col3:
        if 'Most recent denominator' in df.columns:
            denominator = df['Most recent denominator'].sum()
            st.metric("Most Recent Denominator", f"{denominator:,.0f}")
    
    # Performance Metrics
    st.subheader("Performance Rates")
    st.caption("Current performance on key child welfare measures. Higher percentages generally indicate better outcomes (e.g., permanency achieved, stability maintained).")
    if 'Most recent performance' in df.columns:
        perf_data = df[['Measure description', 'Most recent performance']].dropna()
        if len(perf_data) > 0:
            fig = px.bar(
                perf_data.head(10),
                x='Most recent performance',
                y='Measure description',
                orientation='h',
                labels={'Most recent performance': 'Performance Rate', 'Measure description': 'Measure'},
                color='Most recent performance',
                color_continuous_scale='RdYlGn'
            )
            st.plotly_chart(fig, width='stretch')
    
    # Year-over-Year Change
    st.subheader("Trend Analysis (One-Year Change)")
    st.caption("Year-over-year percentage changes show performance trends. Positive changes may indicate improvement, but interpretation depends on the specific measure.")
    if 'One-year percent change' in df.columns:
        change_data = df[['Measure description', 'One-year percent change']].dropna()
        if len(change_data) > 0:
            fig = px.bar(
                change_data.head(10),
                x='One-year percent change',
                y='Measure description',
                orientation='h',
                labels={'One-year percent change': 'Percent Change (%)', 'Measure description': 'Measure'},
                color='One-year percent change',
                color_continuous_scale='RdBu'
            )
            st.plotly_chart(fig, width='stretch')
    
    # Data Table
    st.subheader("Detailed Measures")
    st.caption("Complete performance data with numerators, denominators, and year-over-year changes for all tracked measures.")
    display_cols = [col for col in ['Measure description', 'Most recent numerator', 
                                     'Most recent denominator', 'Most recent performance',
                                     'One-year percent change'] if col in df.columns]
    if display_cols:
        st.dataframe(df[display_cols], width='stretch')

def show_census_dashboard(df):
    """Visualize Census Data"""
    st.header("📈 Census & Demographic Data")
    
    st.info("**Data Source:** U.S. Census Bureau - American Community Survey (ACS) 5-Year Estimates")
    st.markdown("""
    Demographic and socioeconomic characteristics of Calaveras County from the ACS.
    These data provide context for behavioral health needs, service planning, and health equity analysis.
    """)
    
    st.subheader("Key Statistics")
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Data Points", len(df))
    
    with col2:
        if 'County' in df.columns:
            st.metric("Counties", df['County'].nunique())
    
    # Value Distribution
    st.subheader("Data Values Distribution")
    st.caption("Distribution of demographic data values across all variables. Shows the range and frequency of population characteristics.")
    if 'Value' in df.columns and 'Label' in df.columns:
        # Get numeric values
        df_numeric = df[df['Value'].notna()].copy()
        if len(df_numeric) > 0:
            fig = px.histogram(
                df_numeric,
                x='Value',
                nbins=30,
                labels={'Value': 'Value', 'count': 'Frequency'},
                color_discrete_sequence=['steelblue']
            )
            st.plotly_chart(fig, width='stretch')
    
    # Top Metrics
    st.subheader("Top Data Points")
    st.caption("Highest-value demographic indicators. Useful for identifying major population characteristics and service needs.")
    if 'Label' in df.columns and 'Value' in df.columns:
        top_data = df.nlargest(15, 'Value')[['Label', 'Value', 'County']]
        st.dataframe(top_data, width='stretch')


def show_abgar_dashboard():
    """Visualize ABGAR (Beneficiary Grievance and Appeal) Data"""
    st.header("⚖️ Mental Health Services - Grievances & Appeals")
    
    st.info("**Data Source:** California Department of Health Care Services (DHCS) - Annual Beneficiary Grievance and Appeal Report (ABGAR)")
    st.markdown("""
    This dashboard tracks beneficiary grievances, appeals, and notices of adverse benefit determinations (NOABD) for mental health services in Calaveras County.
    These data help identify service quality issues, access barriers, and areas needing improvement in the mental health delivery system.
    
    **County vs. State Comparison:** Charts show Calaveras County data compared to California state totals for context.
    """)
    
    # Load ABGAR data
    data = {}
    csv_dir = "output_csv"
    abgar_files = ['abgar_grievances', 'abgar_appeals', 'abgar_expedited_appeals', 'abgar_noabd']
    
    for fname in abgar_files:
        fpath = os.path.join(csv_dir, f"{fname}.csv")
        if os.path.exists(fpath):
            data[fname] = pd.read_csv(fpath)
    
    if not data:
        st.error("No ABGAR data available")
        return
    
    # Key Metrics - County vs State
    st.subheader("Overview - Calaveras County vs. California State")
    county_griev = None
    state_griev = None
    county_app = None
    state_app = None
    
    # Create comparison metrics
    if 'abgar_grievances' in data:
        df_griev = data['abgar_grievances']
        county_griev = df_griev[df_griev['Geography'] == 'Calaveras']['Grievance Count'].sum()
        state_griev = df_griev[df_griev['Geography'] == 'State']['Grievance Count'].sum()
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Calaveras - Total Grievances", f"{county_griev:,.0f}")
        with col2:
            st.metric("California State - Total Grievances", f"{state_griev:,.0f}")
    
    if 'abgar_appeals' in data:
        df_app = data['abgar_appeals']
        county_app = df_app[df_app['Geography'] == 'Calaveras']['Appeal Count'].sum()
        state_app = df_app[df_app['Geography'] == 'State']['Appeal Count'].sum()
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Calaveras - Appeals", f"{county_app:,.0f}")
        with col2:
            st.metric("California State - Appeals", f"{state_app:,.0f}")

    # Cross-comparison: Grievances per Provider
    st.subheader("Service Load - Grievances per Provider")
    st.caption("Cross-comparison of grievance volume and provider capacity in Calaveras County. Shows how many grievances occur per 100 providers.")
    providers_path = os.path.join(csv_dir, "ffs_providers_profile.csv")
    if os.path.exists(providers_path) and county_griev is not None:
        providers_df = pd.read_csv(providers_path)
        provider_count = len(providers_df)
        if provider_count > 0:
            grievances_per_100 = (county_griev / provider_count) * 100
            st.metric("Grievances per 100 Providers", f"{grievances_per_100:.1f}")
        else:
            st.info("Provider count is zero; cannot compute grievances per provider.")
    else:
        st.info("Provider data not available to compute grievances per provider.")

    # Cross-comparison: Calaveras share of statewide totals
    st.subheader("Calaveras Share of Statewide Totals")
    st.caption("Percentage of California total grievances and appeals attributed to Calaveras County. Percentages enable direct comparison to statewide totals.")

    if 'abgar_grievances' in data:
        share_df = df_griev[df_griev['Geography'].isin(['Calaveras', 'State'])].groupby(['Report Year', 'Geography'])['Grievance Count'].sum().reset_index()
        share_pivot = share_df.pivot(index='Report Year', columns='Geography', values='Grievance Count').fillna(0)
        if 'State' in share_pivot.columns and 'Calaveras' in share_pivot.columns:
            share_pivot['Percent'] = share_pivot['Calaveras'] / share_pivot['State'].replace(0, pd.NA) * 100
            share_plot = share_pivot.reset_index().dropna(subset=['Percent'])
            if len(share_plot) > 0:
                fig = px.line(
                    share_plot,
                    x='Report Year',
                    y='Percent',
                    markers=True,
                    labels={'Percent': 'Percent of State (%)', 'Report Year': 'Fiscal Year'},
                    title='Calaveras Share of Statewide Grievances'
                )
                st.plotly_chart(fig, width='stretch')

    if 'abgar_appeals' in data:
        share_df = df_app[df_app['Geography'].isin(['Calaveras', 'State'])].groupby(['Report Year', 'Geography'])['Appeal Count'].sum().reset_index()
        share_pivot = share_df.pivot(index='Report Year', columns='Geography', values='Appeal Count').fillna(0)
        if 'State' in share_pivot.columns and 'Calaveras' in share_pivot.columns:
            share_pivot['Percent'] = share_pivot['Calaveras'] / share_pivot['State'].replace(0, pd.NA) * 100
            share_plot = share_pivot.reset_index().dropna(subset=['Percent'])
            if len(share_plot) > 0:
                fig = px.line(
                    share_plot,
                    x='Report Year',
                    y='Percent',
                    markers=True,
                    labels={'Percent': 'Percent of State (%)', 'Report Year': 'Fiscal Year'},
                    title='Calaveras Share of Statewide Appeals'
                )
                st.plotly_chart(fig, width='stretch')
    
    # Grievance Analysis - Comparison
    if 'abgar_grievances' in data:
        st.subheader("Grievances by Category - County vs. State")
        st.caption("Distribution of grievances across categories. Compare Calaveras County patterns to statewide trends to identify local vs. systemic issues. Excludes summary totals ('All').")
        grievance_df = data['abgar_grievances'].copy()
        
        # Filter out summary rows (where Category or Type = 'All')
        grievance_df = grievance_df[
            (grievance_df['Grievance Category'] != 'All') & 
            (grievance_df['Grievance Type'] != 'All')
        ]
        
        # Separate county and state data, group by category
        county_data = grievance_df[grievance_df['Geography'] == 'Calaveras'].groupby('Grievance Category')['Grievance Count'].sum().reset_index()
        state_data = grievance_df[grievance_df['Geography'] == 'State'].groupby('Grievance Category')['Grievance Count'].sum().reset_index()
        
        # Remove zero-count categories for cleaner visualization
        county_data = county_data[county_data['Grievance Count'] > 0]
        state_data = state_data[state_data['Grievance Count'] > 0]
        
        # Side-by-side comparison using percentages (grouped bar chart)
        if len(county_data) > 0 and len(state_data) > 0:
            county_total = county_data['Grievance Count'].sum()
            state_total = state_data['Grievance Count'].sum()
            county_data['Percent'] = (county_data['Grievance Count'] / county_total) * 100 if county_total else 0
            state_data['Percent'] = (state_data['Grievance Count'] / state_total) * 100 if state_total else 0

            county_data['Geography'] = 'Calaveras'
            state_data['Geography'] = 'State'
            combined = pd.concat([county_data, state_data])

            # Grouped bar chart (horizontal for easier category reading)
            fig = px.bar(
                combined,
                x='Percent',
                y='Grievance Category',
                color='Geography',
                barmode='group',
                orientation='h',
                labels={'Percent': 'Percent of Total Grievances (%)'},
                color_discrete_map={'Calaveras': '#1f77b4', 'State': '#ff7f0e'},
                title='Grievance Category Distribution - Percentage Comparison'
            )
            fig.update_layout(yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig, width='stretch')
    
    # Detailed County Grievance Table
    if 'abgar_grievances' in data:
        st.subheader("Calaveras County - Grievance Details by Type")
        st.caption("Top 20 grievance types ranked by count for Calaveras County. Shows specific issues beneficiaries reported and how many were resolved or referred.")
        county_grievances = data['abgar_grievances'][data['abgar_grievances']['Geography'] == 'Calaveras']
        grievance_detail = county_grievances[['Report Year', 'Grievance Category', 'Grievance Type', 
                                                       'Grievance Count', 'Resolved', 'Referred']].copy()
        grievance_detail = grievance_detail.dropna(subset=['Grievance Count'])
        st.dataframe(grievance_detail.sort_values('Grievance Count', ascending=False).head(20), width='stretch')
    
    # Grievance and Appeal Trends Over Time
    if 'abgar_grievances' in data and 'abgar_appeals' in data:
        st.subheader("Grievances and Appeals Trends - Calaveras vs. State")
        st.caption("Year-over-year trends in grievances and appeals. Track how complaint volumes have changed. Note: Calaveras has zero appeals on record.")
        
        # Grievances over time
        griev_trend = df_griev.groupby(['Report Year', 'Geography'])['Grievance Count'].sum().reset_index()
        griev_cal = griev_trend[griev_trend['Geography'] == 'Calaveras']
        griev_state = griev_trend[griev_trend['Geography'] == 'State']
        
        # Use dual y-axis to show both on same chart
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        if len(griev_cal) > 0:
            fig.add_trace(
                go.Scatter(
                    x=griev_cal['Report Year'],
                    y=griev_cal['Grievance Count'],
                    mode='lines+markers',
                    name='Calaveras Grievances',
                    line=dict(color='#1f77b4')
                ),
                secondary_y=False
            )
        
        if len(griev_state) > 0:
            fig.add_trace(
                go.Scatter(
                    x=griev_state['Report Year'],
                    y=griev_state['Grievance Count'],
                    mode='lines+markers',
                    name='State Grievances',
                    line=dict(color='#ff7f0e', dash='dash')
                ),
                secondary_y=True
            )
        
        fig.update_layout(
            title='Grievance Trends Over Time',
            xaxis_title='Fiscal Year',
            height=450
        )
        fig.update_yaxes(title_text='Calaveras Count', secondary_y=False)
        fig.update_yaxes(title_text='State Count', secondary_y=True)
        st.plotly_chart(fig, width='stretch')
    


def show_depression_dashboard():
    """Visualize Adult Depression (LGHC) Data"""
    st.header("🧠 Mental Health - Adult Depression Prevalence")
    
    # Load depression data
    fpath = "output_csv/adult_depression_lghc.csv"
    if not os.path.exists(fpath):
        st.error("Adult Depression (LGHC) data not available")
        return
    
    df = pd.read_csv(fpath)
    
    # Key Metrics
    st.subheader("California State Summary (BRFSS)")
    st.caption("Statewide depression prevalence provides context for Calaveras County behavioral health needs. California data helps benchmark local trends.")
    col1, col2, col3 = st.columns(3)
    
    total_data = df[df['Strata Name'] == 'Total']
    
    with col1:
        if len(total_data) > 0:
            avg_prevalence = total_data['Percent'].mean()
            st.metric("Average Depression Prevalence", f"{avg_prevalence:.1f}%")
    
    with col2:
        st.metric("Data Years", f"{int(df['Year'].min())}-{int(df['Year'].max())}")
    
    with col3:
        st.metric("Data Points", len(df))
    
    # Trend Analysis Over Time
    st.subheader("Depression Prevalence Trend (Overall)")
    st.caption("Percentage of California adults ever diagnosed with depression over time. Shaded area shows 95% confidence interval. Upward trends may reflect both increased prevalence and improved screening/diagnosis.")
    trend_data = df[df['Strata Name'] == 'Total'].sort_values('Year')
    if len(trend_data) > 0:
        fig = px.line(
            trend_data,
            x='Year',
            y='Percent',
            markers=True,
            labels={'Percent': 'Prevalence (%)', 'Year': 'Year'},
            title='Adult Depression Prevalence Over Time',
            color_discrete_sequence=['#1f77b4']
        )
        fig.add_scatter(
            x=trend_data['Year'],
            y=trend_data['Lower 95% CL'],
            mode='lines',
            line=dict(width=0),
            name='Lower CI'
        )
        fig.add_scatter(
            x=trend_data['Year'],
            y=trend_data['Upper 95% CL'],
            mode='lines',
            line=dict(width=0),
            fillcolor='rgba(31, 119, 180, 0.2)',
            fill='tonexty',
            name='Upper CI'
        )
        fig.update_traces(showlegend=False, selector=dict(name='Lower CI'))
        fig.update_traces(showlegend=False, selector=dict(name='Upper CI'))
        st.plotly_chart(fig, width='stretch')
    
    # Demographics Comparison
    st.subheader("Depression Prevalence by Demographics")
    st.caption("Compare depression rates across demographic groups. Higher bars indicate populations with elevated depression prevalence who may need targeted services.")
    
    col1, col2 = st.columns(2)
    
    # Sex comparison
    with col1:
        sex_data = df[df['Strata'] == 'Sex'].drop_duplicates(subset=['Strata Name']).sort_values('Percent', ascending=False)
        if len(sex_data) > 0:
            fig = px.bar(
                sex_data,
                x='Strata Name',
                y='Percent',
                color='Strata Name',
                labels={'Percent': 'Prevalence (%)', 'Strata Name': 'Sex'},
                title='Depression by Sex',
                color_discrete_map={'Male': '#3498db', 'Female': '#e74c3c'}
            )
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, width='stretch')
    
    # Age comparison
    with col2:
        age_data = df[df['Strata'] == 'Age'].drop_duplicates(subset=['Strata Name']).sort_values('Percent', ascending=False)
        if len(age_data) > 0:
            fig = px.bar(
                age_data,
                x='Strata Name',
                y='Percent',
                labels={'Percent': 'Prevalence (%)', 'Strata Name': 'Age Group'},
                title='Depression by Age Group',
                color='Percent',
                color_continuous_scale='Reds'
            )
            st.plotly_chart(fig, width='stretch')
    
    # Race-Ethnicity comparison
    st.subheader("Depression Prevalence by Race/Ethnicity")
    st.caption("Disparities in depression prevalence by racial/ethnic group. Differences may reflect access to care, cultural factors, and health inequities.")
    race_data = df[df['Strata'] == 'Race-Ethnicity'].drop_duplicates(subset=['Strata Name']).sort_values('Percent', ascending=False)
    if len(race_data) > 0:
        fig = px.bar(
            race_data,
            x='Percent',
            y='Strata Name',
            orientation='h',
            labels={'Percent': 'Prevalence (%)', 'Strata Name': 'Race/Ethnicity'},
            color='Percent',
            color_continuous_scale='Purples'
        )
        st.plotly_chart(fig, width='stretch')
    
    # Education & Income
    st.subheader("Depression by Socioeconomic Status")
    st.caption("Depression prevalence by education and income levels. Lower socioeconomic status often correlates with higher depression rates due to stress, access barriers, and social determinants of health.")
    col1, col2 = st.columns(2)
    
    with col1:
        edu_data = df[df['Strata'] == 'Education'].drop_duplicates(subset=['Strata Name']).sort_values('Percent', ascending=False)
        if len(edu_data) > 0:
            fig = px.bar(
                edu_data,
                x='Strata Name',
                y='Percent',
                labels={'Percent': 'Prevalence (%)', 'Strata Name': 'Education'},
                title='Depression by Education Level',
                color='Percent',
                color_continuous_scale='Blues'
            )
            st.plotly_chart(fig, width='stretch')
    
    with col2:
        income_data = df[df['Strata'] == 'Income'].drop_duplicates(subset=['Strata Name']).sort_values('Percent', ascending=False)
        if len(income_data) > 0:
            fig = px.bar(
                income_data,
                x='Strata Name',
                y='Percent',
                labels={'Percent': 'Prevalence (%)', 'Strata Name': 'Income Level'},
                title='Depression by Income Level',
                color='Percent',
                color_continuous_scale='Greens'
            )
            st.plotly_chart(fig, width='stretch')
    
    # Detailed Data Table
    st.subheader("Detailed Prevalence Data")
    st.caption("Top 30 data points ranked by prevalence percentage. Includes confidence intervals and weighted frequency estimates.")
    display_cols = ['Year', 'Strata', 'Strata Name', 'Percent', 'Lower 95% CL', 'Upper 95% CL', 'Frequency']
    display_cols = [col for col in display_cols if col in df.columns]
    st.dataframe(
        df[display_cols].sort_values('Percent', ascending=False).head(30),
        width='stretch'
    )
    
    # Data Source Info
    st.info("""
    **Data Source:** California Behavioral Risk Factor Surveillance Survey (BRFSS)
    
    **Indicator:** Proportion of adults ever told they had a depressive disorder (depression, major depression, dysthymia, or minor depression)
    
    **Geography:** California statewide (state-level data, not county-specific)
    
    **Reference:** Let's Get Healthy California (LGHC) - https://letsgethealthy.ca.gov/
    """)
    


def show_core_set_dashboard(df):
    """Visualize Core Set Mental Health Measures"""
    st.header("🧾 Core Set Mental Health Measures")

    st.info("**Data Source:** DHCS - Core Set Measures for Mental Health (1915b STCs)")
    st.markdown("""
    These measures track quality and performance of mental health services across California.
    Use this dashboard to monitor statewide trends and benchmark local performance initiatives.
    """)

    if df.empty:
        st.warning("No Core Set measures data available.")
        return

    df_clean = df.copy()
    if 'Measure_Year' in df_clean.columns:
        df_clean['Measure_Year'] = pd.to_numeric(df_clean['Measure_Year'], errors='coerce')
    if 'Rate' in df_clean.columns:
        df_clean['Rate'] = pd.to_numeric(df_clean['Rate'].astype(str).str.rstrip('%'), errors='coerce')

    latest_year = int(df_clean['Measure_Year'].max()) if 'Measure_Year' in df_clean.columns else None

    st.subheader("Key Metrics")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Records", len(df_clean))
    with col2:
        st.metric("Measures", df_clean['Measure'].nunique() if 'Measure' in df_clean.columns else 0)
    with col3:
        st.metric("Latest Year", latest_year if latest_year else "Unknown")

    st.subheader("Top Measures by Rate (Latest Year)")
    st.caption("Highest-performing measures in the most recent year. Rates are percentages and reflect statewide performance.")
    if latest_year and 'Rate' in df_clean.columns:
        top_measures = df_clean[df_clean['Measure_Year'] == latest_year].dropna(subset=['Rate'])
        top_measures = top_measures.sort_values('Rate', ascending=False).head(10)
        if len(top_measures) > 0:
            fig = px.bar(
                top_measures,
                x='Rate',
                y='Measure',
                orientation='h',
                labels={'Rate': 'Rate (%)', 'Measure': 'Measure'},
                color='Rate',
                color_continuous_scale='Blues'
            )
            st.plotly_chart(fig, width='stretch')

    st.subheader("Trend by Measure")
    st.caption("Select a measure to see how performance has changed over time. Rates are averaged across categories and populations.")
    if 'Measure' in df_clean.columns:
        measure_options = sorted([m for m in df_clean['Measure'].dropna().unique()])
        if measure_options:
            selected_measure = st.selectbox("Select Measure", measure_options)
            trend_df = df_clean[df_clean['Measure'] == selected_measure].dropna(subset=['Rate'])
            if len(trend_df) > 0:
                # Aggregate by year and type (average rates across categories/populations)
                trend_agg = trend_df.groupby(['Measure_Year', 'Type'])['Rate'].mean().reset_index()
                trend_agg = trend_agg.sort_values('Measure_Year')
                fig = px.line(
                    trend_agg,
                    x='Measure_Year',
                    y='Rate',
                    color='Type',
                    markers=True,
                    labels={'Measure_Year': 'Year', 'Rate': 'Rate (%)'},
                    title=f"{selected_measure} Performance Trend"
                )
                st.plotly_chart(fig, width='stretch')

    st.subheader("Detailed Measure Data")
    st.caption("Complete Core Set measures data for review and quality monitoring.")
    display_cols = [
        'Measure_Year', 'Type', 'Measure', 'Category', 'Population',
        'Numerator', 'Denominator', 'Rate'
    ]
    display_cols = [col for col in display_cols if col in df_clean.columns]
    if display_cols:
        st.dataframe(df_clean[display_cols].head(50), width='stretch')


def show_mat_dashboard(df_annual, df_quarterly):
    """Visualize Medication-Assisted Treatment (MAT) Data"""
    st.header("💊 Medication-Assisted Treatment (MAT) for Opioid Use Disorders")

    st.info("**Data Source:** DHCS - Medication-Assisted Treatment in Medi-Cal for Opioid Use Disorders")
    st.markdown("""
    MAT data shows how many Medi-Cal members received opioid use disorder treatment (e.g., Buprenorphine, Methadone).
    Compare Calaveras County to statewide trends to understand local treatment access and gaps.
    """)

    if df_annual.empty and df_quarterly.empty:
        st.warning("No MAT data available.")
        return

    # Annual Trends
    st.subheader("Annual MAT Utilization - County vs. State")
    st.caption("Annual member counts receiving MAT. Dual y-axes scale county and statewide values separately.")

    if not df_annual.empty:
        annual = df_annual.copy()
        annual['Year'] = pd.to_numeric(annual['Year'], errors='coerce')
        annual['members'] = pd.to_numeric(annual['members'], errors='coerce')
        annual = annual.dropna(subset=['Year'])

        meds = sorted([m for m in annual['Medication_Assisted_Treatment'].dropna().unique()])
        selected_med = st.selectbox("Select MAT Medication", meds) if meds else None

        if selected_med:
            filtered = annual[
                (annual['Medication_Assisted_Treatment'] == selected_med)
                & (annual['County'].isin(['Calaveras', 'Statewide']))
            ]
            filtered = filtered.dropna(subset=['members'])

            if len(filtered) > 0:
                cal = filtered[filtered['County'] == 'Calaveras'].sort_values('Year')
                state = filtered[filtered['County'] == 'Statewide'].sort_values('Year')

                fig = make_subplots(specs=[[{"secondary_y": True}]])
                fig.add_trace(
                    go.Scatter(
                        x=cal['Year'],
                        y=cal['members'],
                        mode='lines+markers',
                        name='Calaveras'
                    ),
                    secondary_y=False
                )
                fig.add_trace(
                    go.Scatter(
                        x=state['Year'],
                        y=state['members'],
                        mode='lines+markers',
                        name='Statewide'
                    ),
                    secondary_y=True
                )
                fig.update_layout(
                    title=f"{selected_med} - Annual MAT Utilization",
                    xaxis_title='Year'
                )
                fig.update_yaxes(title_text='Calaveras Members', secondary_y=False)
                fig.update_yaxes(title_text='Statewide Members', secondary_y=True)
                st.plotly_chart(fig, width='stretch')

                # Share of statewide totals (percentage)
                share_df = filtered.pivot_table(index='Year', columns='County', values='members', aggfunc='sum').fillna(0)
                if 'Calaveras' in share_df.columns and 'Statewide' in share_df.columns:
                    share_df['Percent'] = share_df['Calaveras'] / share_df['Statewide'].replace(0, pd.NA) * 100
                    share_plot = share_df.reset_index().dropna(subset=['Percent'])
                    if len(share_plot) > 0:
                        st.subheader("Calaveras Share of Statewide MAT")
                        st.caption("Percent of statewide MAT utilization attributed to Calaveras County. Percentages allow direct comparison across years.")
                        fig = px.line(
                            share_plot,
                            x='Year',
                            y='Percent',
                            markers=True,
                            labels={'Percent': 'Percent of State (%)', 'Year': 'Year'},
                            title=f"{selected_med} - Calaveras Share of Statewide MAT"
                        )
                        st.plotly_chart(fig, width='stretch')

                latest_year = int(filtered['Year'].max())
                latest = filtered[filtered['Year'] == latest_year]
                col1, col2 = st.columns(2)
                with col1:
                    cal_val = latest[latest['County'] == 'Calaveras']['members'].sum()
                    st.metric("Calaveras (Latest Year)", f"{cal_val:,.0f}")
                with col2:
                    state_val = latest[latest['County'] == 'Statewide']['members'].sum()
                    st.metric("Statewide (Latest Year)", f"{state_val:,.0f}")

    # Quarterly Trends
    st.subheader("Quarterly MAT Trends Over Time")
    st.caption("Seasonal patterns and long-term quarterly trends. Shows how each quarter's utilization has changed year-over-year.")

    if not df_quarterly.empty:
        quarterly = df_quarterly.copy()
        quarterly['Year'] = pd.to_numeric(quarterly['Year'], errors='coerce')
        quarterly['members'] = pd.to_numeric(quarterly['members'], errors='coerce')
        quarterly = quarterly.dropna(subset=['Year'])

        q_filtered = quarterly[
            quarterly['County'].isin(['Calaveras', 'Statewide'])
        ].dropna(subset=['members'])

        if len(q_filtered) > 0:
            # Create Year-Quarter combo for x-axis
            q_filtered['YearQuarter'] = q_filtered['Year'].astype(str) + '-' + q_filtered['Quarter'].astype(str)
            
            # Aggregate by year and quarter (average across MAT types)
            q_agg = q_filtered.groupby(['Year', 'Quarter', 'County'])['members'].mean().reset_index()
            q_agg['YearQuarter'] = q_agg['Year'].astype(str) + '-' + q_agg['Quarter'].astype(str)
            
            # Separate Calaveras and Statewide
            cal_q = q_agg[q_agg['County'] == 'Calaveras'].sort_values(['Year', 'Quarter'])
            state_q = q_agg[q_agg['County'] == 'Statewide'].sort_values(['Year', 'Quarter'])

            # Show trend over time with dual y-axes
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            fig.add_trace(
                go.Scatter(
                    x=cal_q['YearQuarter'],
                    y=cal_q['members'],
                    mode='lines+markers',
                    name='Calaveras',
                    line=dict(dash='solid')
                ),
                secondary_y=False
            )
            fig.add_trace(
                go.Scatter(
                    x=state_q['YearQuarter'],
                    y=state_q['members'],
                    mode='lines+markers',
                    name='Statewide',
                    line=dict(dash='dash')
                ),
                secondary_y=True
            )
            fig.update_layout(
                title="MAT Utilization by Quarter - Time Series",
                xaxis_title='Year-Quarter',
                height=500
            )
            fig.update_xaxes(tickangle=45)
            fig.update_yaxes(title_text='Calaveras Members (Avg)', secondary_y=False)
            fig.update_yaxes(title_text='Statewide Members (Avg)', secondary_y=True)
            st.plotly_chart(fig, width='stretch')

    # Detailed Data Tables
    st.subheader("Detailed MAT Data")
    st.caption("Annual and quarterly MAT records for Calaveras County and statewide comparison.")
    if not df_annual.empty:
        st.markdown("**Annual Data (Sample)**")
        st.dataframe(df_annual.head(30), width='stretch')
    if not df_quarterly.empty:
        st.markdown("**Quarterly Data (Sample)**")
        st.dataframe(df_quarterly.head(30), width='stretch')


def show_tobacco_dashboard(df_cigarette, df_tobacco):
    """Visualize Tobacco & Cigarette Use Prevalence"""
    st.header("🚬 Tobacco & Cigarette Use Prevalence")
    
    st.info("**Data Source:** California Department of Public Health (CDPH) - California Tobacco Control Program")
    st.markdown("""
    Historical trends in cigarette and tobacco use among California adults (1984-2019).
    These data provide context for substance use patterns and prevention efforts.
    
    **Note:** Data is statewide, not specific to Calaveras County.
    """)
    
    # Cigarette Use Trends
    if df_cigarette is not None and not df_cigarette.empty:
        st.subheader("Cigarette Use Trends (1984-2019)")
        st.caption("Historical California adult cigarette use prevalence by gender with 95% confidence intervals.")
        
        # Line chart by gender
        fig = px.line(
            df_cigarette,
            x='YEAR',
            y='PERCENT',
            color='GENDER',
            labels={'PERCENT': 'Prevalence (%)', 'YEAR': 'Year', 'GENDER': 'Gender'},
            title='Adult Cigarette Use by Gender'
        )
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
        
        # Key metrics
        col1, col2, col3 = st.columns(3)
        latest_year = df_cigarette['YEAR'].max()
        latest_data = df_cigarette[df_cigarette['YEAR'] == latest_year]
        
        with col1:
            overall = latest_data[latest_data['GENDER'] == 'Total']['PERCENT'].values
            if len(overall) > 0:
                st.metric(f"Overall ({latest_year})", f"{overall[0]:.1f}%")
        
        with col2:
            male = latest_data[latest_data['GENDER'] == 'Male']['PERCENT'].values
            if len(male) > 0:
                st.metric(f"Male ({latest_year})", f"{male[0]:.1f}%")
        
        with col3:
            female = latest_data[latest_data['GENDER'] == 'Female']['PERCENT'].values
            if len(female) > 0:
                st.metric(f"Female ({latest_year})", f"{female[0]:.1f}%")
    
    # Tobacco Use by Demographics
    if df_tobacco is not None and not df_tobacco.empty:
        st.subheader("Tobacco Use by Demographics (2016-2019)")
        st.caption("Recent tobacco use prevalence by demographic groups. Asterisks (*) indicate suppressed values.")
        
        # Filter numeric data
        df_tobacco_numeric = df_tobacco[df_tobacco['PERCENT'] != '*'].copy()
        df_tobacco_numeric['PERCENT'] = pd.to_numeric(df_tobacco_numeric['PERCENT'], errors='coerce')
        df_tobacco_numeric = df_tobacco_numeric.dropna(subset=['PERCENT'])
        
        if not df_tobacco_numeric.empty:
            # Bar chart by demographic
            latest_tobacco = df_tobacco_numeric[df_tobacco_numeric['YEAR'] == df_tobacco_numeric['YEAR'].max()]
            fig = px.bar(
                latest_tobacco.sort_values('PERCENT', ascending=False),
                x='PERCENT',
                y='DEMOGRAPHIC',
                orientation='h',
                labels={'PERCENT': 'Prevalence (%)', 'DEMOGRAPHIC': 'Demographic Group'},
                title='Tobacco Use by Demographic Group',
                color='PERCENT',
                color_continuous_scale='Reds'
            )
            fig.update_layout(height=600)
            st.plotly_chart(fig, use_container_width=True)


def show_lanterman_dashboard(df):
    """Visualize Lanterman-Petris-Short (LPS) Act Data"""
    st.header("🚨 Lanterman-Petris-Short Act - Emergency Psychiatric Holds")
    
    st.info("**Data Source:** California Department of Health Care Services (DHCS) - LPS Act Data")
    st.markdown("""
    Involuntary psychiatric holds under the Lanterman-Petris-Short (LPS) Act for 2023.
    This data tracks emergency mental health interventions by county, including 72-hour holds (5150), 
    14-day certifications (5250), and extended holds.
    """)
    
    # Filter Calaveras County data
    df_calaveras = df[df['COUNTY'].str.contains('Calaveras', case=False, na=False)]
    df_statewide = df[df['COUNTY'].str.contains('Statewide', case=False, na=False)]
    
    # Key Metrics
    st.subheader("Calaveras County - Emergency Psychiatric Holds (2023)")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_holds = df_calaveras['AMOUNT'].sum()
        st.metric("Total Holds", f"{total_holds:,.0f}")
    
    with col2:
        hold_types = df_calaveras['CATEGORY'].nunique()
        st.metric("Hold Categories", hold_types)
    
    with col3:
        avg_hold = df_calaveras['AMOUNT'].mean()
        st.metric("Avg per Category", f"{avg_hold:,.1f}")
    
    # Holds by Category
    st.subheader("Distribution by Hold Type")
    st.caption("Breakdown of emergency psychiatric holds by category (72h, 14-day, extended) for Calaveras County.")
    if not df_calaveras.empty:
        category_counts = df_calaveras.groupby('CATEGORY')['AMOUNT'].sum().sort_values(ascending=False)
        fig = px.bar(
            x=category_counts.values,
            y=category_counts.index,
            orientation='h',
            labels={'x': 'Number of Holds', 'y': 'Hold Category'},
            color=category_counts.values,
            color_continuous_scale='Reds'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Age Group Distribution
    st.subheader("Age Group Distribution")
    st.caption("Emergency holds by age group. Shows which populations require the most crisis interventions.")
    if 'AMOUNT_DESC' in df_calaveras.columns:
        age_data = df_calaveras[df_calaveras['AMOUNT_DESC'].str.contains('Adult|Child', case=False, na=False)]
        if not age_data.empty:
            age_counts = age_data.groupby('AMOUNT_DESC')['AMOUNT'].sum().sort_values(ascending=False)
            fig = px.pie(
                values=age_counts.values,
                names=age_counts.index,
                title='Holds by Age Group'
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # County Comparison
    st.subheader("Calaveras vs. Statewide Comparison")
    st.caption("Comparison of hold rates and patterns between Calaveras County and California statewide totals.")
    if not df_statewide.empty and not df_calaveras.empty:
        col1, col2 = st.columns(2)
        with col1:
            calaveras_total = df_calaveras['AMOUNT'].sum()
            st.metric("Calaveras Total", f"{calaveras_total:,.0f}")
        with col2:
            state_total = df_statewide['AMOUNT'].sum()
            st.metric("Statewide Total", f"{state_total:,.0f}")
            if state_total > 0:
                pct = (calaveras_total / state_total) * 100
                st.caption(f"Calaveras represents {pct:.2f}% of statewide holds")
    
    # Data Table
    st.subheader("Detailed Data")
    st.dataframe(df_calaveras, use_container_width=True)


def show_crisis_services_dashboard(df):
    """Visualize Crisis Service Utilization (OCW)"""
    st.header("📞 Crisis Service Utilization")
    
    st.info("**Data Source:** California Department of Health Care Services (DHCS) - Specialty Mental Health Services (SMHS)")
    st.markdown("""
    Mental health crisis service utilization by county and demographic groups.
    Tracks crisis hotlines, walk-in crisis centers, mobile crisis teams, and other emergency mental health services.
    """)
    
    # Filter Calaveras data
    df_calaveras = df[df['Health Care Delivery System'].str.contains('Calaveras', case=False, na=False)]
    
    # Key Metrics
    st.subheader("Calaveras County Crisis Services")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_services = df_calaveras['Amount MH Service Received'].sum()
        st.metric("Total Services", f"{total_services:,.0f}")
    
    with col2:
        service_types = df_calaveras['MH Service Description'].nunique()
        st.metric("Service Types", service_types)
    
    with col3:
        fiscal_years = df_calaveras['Fiscal Year'].nunique()
        st.metric("Fiscal Years", fiscal_years)
    
    # Service Type Distribution
    st.subheader("Crisis Services by Type")
    st.caption("Breakdown of crisis service utilization by service type (phone crisis, walk-in, mobile teams, etc.).")
    if not df_calaveras.empty:
        service_counts = df_calaveras.groupby('MH Service Description')['Amount MH Service Received'].sum().sort_values(ascending=False)
        fig = px.bar(
            x=service_counts.values,
            y=service_counts.index,
            orientation='h',
            labels={'x': 'Service Count', 'y': 'Service Type'},
            color=service_counts.values,
            color_continuous_scale='Blues'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Trend Over Time
    st.subheader("Service Trends by Fiscal Year")
    st.caption("Year-over-year trends in crisis service demand. Shows whether crisis services are increasing or decreasing.")
    if 'Fiscal Year' in df_calaveras.columns:
        yearly_data = df_calaveras.groupby('Fiscal Year')['Amount MH Service Received'].sum().reset_index()
        fig = px.line(
            yearly_data,
            x='Fiscal Year',
            y='Amount MH Service Received',
            markers=True,
            labels={'Amount MH Service Received': 'Total Services', 'Fiscal Year': 'Year'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Demographic Breakdown
    st.subheader("Services by Demographic Group")
    if 'Demographic Group' in df_calaveras.columns:
        demo_data = df_calaveras.groupby('Demographic Group')['Amount MH Service Received'].sum().sort_values(ascending=False)
        fig = px.pie(
            values=demo_data.values,
            names=demo_data.index,
            title='Crisis Services by Demographics'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Data Table
    st.subheader("Detailed Crisis Service Data")
    st.dataframe(df_calaveras, use_container_width=True)


def show_managed_care_dashboard(df):
    """Visualize Medi-Cal Managed Care Enrollment"""
    st.header("🏥 Medi-Cal Managed Care Enrollment")
    
    st.info("**Data Source:** California Department of Health Care Services (DHCS) - Managed Care Enrollment Report")
    st.markdown("""
    Monthly Medi-Cal managed care enrollment by county and plan type (2007-present).
    Shows insurance access trends, plan coverage, and enrollment patterns for behavioral health services.
    """)
    
    # Filter Calaveras data
    df_calaveras = df[df['County'].str.contains('Calaveras', case=False, na=False)].copy()
    
    # Convert enrollee count to numeric (remove commas and spaces)
    df_calaveras[' Count of Enrollees '] = pd.to_numeric(
        df_calaveras[' Count of Enrollees '].astype(str).str.replace(',', '').str.strip(),
        errors='coerce'
    )
    
    # Parse enrollment month
    if not df_calaveras.empty:
        df_calaveras['Enrollment Month'] = pd.to_datetime(df_calaveras['Enrollment Month'], errors='coerce')
        df_calaveras = df_calaveras.dropna(subset=['Enrollment Month', ' Count of Enrollees '])
    
    # Key Metrics
    st.subheader("Calaveras County Managed Care Enrollment")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        latest_enrollment = df_calaveras[' Count of Enrollees '].sum()
        st.metric("Total Enrollees (All Time)", f"{latest_enrollment:,.0f}")
    
    with col2:
        plan_types = df_calaveras['Plan Type'].nunique()
        st.metric("Plan Types", plan_types)
    
    with col3:
        plans = df_calaveras['Plan Name'].nunique()
        st.metric("Unique Plans", plans)
    
    # Enrollment Trends
    st.subheader("Enrollment Trends Over Time")
    st.caption("Monthly enrollment totals from 2007 to present. Shows growth or decline in Medi-Cal coverage in Calaveras.")
    if not df_calaveras.empty:
        monthly_data = df_calaveras.groupby('Enrollment Month')[' Count of Enrollees '].sum().reset_index()
        fig = px.line(
            monthly_data,
            x='Enrollment Month',
            y=' Count of Enrollees ',
            markers=True,
            labels={' Count of Enrollees ': 'Total Enrollees', 'Enrollment Month': 'Month'}
        )
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
    
    # Plan Type Distribution
    st.subheader("Enrollment by Plan Type")
    st.caption("Breakdown by HMO, PPO, DHMO, and specialty care plans. Shows which plan types serve most beneficiaries.")
    if 'Plan Type' in df_calaveras.columns:
        plan_data = df_calaveras.groupby('Plan Type')[' Count of Enrollees '].sum().sort_values(ascending=False)
        fig = px.bar(
            x=plan_data.values,
            y=plan_data.index,
            orientation='h',
            labels={'x': 'Total Enrollees', 'y': 'Plan Type'},
            color=plan_data.values,
            color_continuous_scale='Greens'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Top Plans
    st.subheader("Top 10 Plans by Enrollment")
    if 'Plan Name' in df_calaveras.columns:
        top_plans = df_calaveras.groupby('Plan Name')[' Count of Enrollees '].sum().nlargest(10)
        fig = px.bar(
            x=top_plans.values,
            y=top_plans.index,
            orientation='h',
            labels={'x': 'Enrollees', 'y': 'Plan Name'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Recent Data Table
    st.subheader("Recent Enrollment Data")
    if not df_calaveras.empty:
        recent = df_calaveras.sort_values('Enrollment Month', ascending=False).head(50)
        st.dataframe(recent, use_container_width=True)


def show_data_overview(data):
    """Show overview of all available datasets"""
    st.header("📊 Data Overview - All Datasets")
    
    st.markdown("""
    Summary of all available behavioral health datasets for Calaveras County.
    """)
    
    # Create overview table
    overview_data = []
    for key, df in data.items():
        if key != '_last_updated' and isinstance(df, pd.DataFrame):
            overview_data.append({
                'Dataset': key,
                'Rows': len(df),
                'Columns': len(df.columns),
                'Memory (KB)': df.memory_usage(deep=True).sum() / 1024
            })
    
    if overview_data:
        overview_df = pd.DataFrame(overview_data)
        st.dataframe(overview_df, use_container_width=True)
        
        # Visualize dataset sizes
        fig = px.bar(
            overview_df,
            x='Rows',
            y='Dataset',
            orientation='h',
            title='Dataset Sizes by Row Count',
            labels={'Rows': 'Number of Rows', 'Dataset': 'Dataset Name'}
        )
        st.plotly_chart(fig, use_container_width=True)


def main():
    """Main dashboard app"""
    st.title("📊 Calaveras County Behavioral Health Dashboard")
    
    st.markdown("""
    Welcome to the interactive behavioral health dashboard for Calaveras County.
    This dashboard visualizes cleaned and processed data from multiple sources including:
    - Medi-Cal Fee-for-Service Providers
    - Foster Care & Family Services
    - Census & Demographic Data
    """)

    
    # Load data
    try:
        data = load_data()
        
        if not data:
            st.error("❌ No data files found in output_csv/ directory. Please run the ETL pipeline first.")
            return
        
        # Sidebar navigation
        st.sidebar.header("Navigation")
        page = st.sidebar.radio(
            "Select Dashboard",
            list(range(12)),
            format_func=lambda x: {
                0: "🏥 Providers",
                1: "👨‍👩‍👧 Foster Care",
                2: "📈 Census Data",
                3: "⚖️ Grievances & Appeals",
                4: "🧠 Depression Prevalence",
                5: "🧾 Core Set Measures",
                6: "💊 MAT Utilization",
                7: "🚬 Tobacco Use",
                8: "🚨 Psychiatric Holds (LPS)",
                9: "📞 Crisis Services",
                10: "🏥 Managed Care Enrollment",
                11: "📊 Data Overview"
            }.get(x, "Dashboard")
        )
        
        # Display selected dashboard
        if 'ffs_providers' in data and page == 0:
            show_ffs_providers_dashboard(data['ffs_providers'])
        elif 'foster_care' in data and page == 1:
            show_foster_care_dashboard(data['foster_care'])
        elif 'census' in data and page == 2:
            show_census_dashboard(data['census'])
        elif page == 3:
            show_abgar_dashboard()
        elif page == 4:
            show_depression_dashboard()
        elif page == 5 and 'core_set_mental_health' in data:
            show_core_set_dashboard(data['core_set_mental_health'])
        elif page == 5:
            st.error("Core Set measures data not available. Please run the ETL pipeline.")
        elif page == 6 and 'mat_annual' in data and 'mat_quarterly' in data:
            show_mat_dashboard(data['mat_annual'], data['mat_quarterly'])
        elif page == 6:
            st.error("MAT data not available. Please run the ETL pipeline.")
        elif page == 7:
            show_tobacco_dashboard(
                data.get('cigarette_use'),
                data.get('tobacco_use')
            )
        elif page == 8 and 'lanterman' in data:
            show_lanterman_dashboard(data['lanterman'])
        elif page == 8:
            st.error("Lanterman (LPS) data not available. Please run the ETL pipeline.")
        elif page == 9 and 'crisis_services' in data:
            show_crisis_services_dashboard(data['crisis_services'])
        elif page == 9:
            st.error("Crisis services data not available. Please run the ETL pipeline.")
        elif page == 10 and 'managed_care' in data:
            show_managed_care_dashboard(data['managed_care'])
        elif page == 10:
            st.error("Managed care enrollment data not available. Please run the ETL pipeline.")
        elif page == 11:
            show_data_overview(data)
        
        # Footer
        st.sidebar.markdown("---")
        
        # Get last updated date from data
        last_updated = data.get('_last_updated', 'Unknown')
        
        st.sidebar.markdown(f"""
        **Data Last Updated:** {last_updated}
        
        **Data Sources:**
        - Medi-Cal Provider Directory
        - Foster Care Services (CFSR4)
        - Census Bureau (ACS 5-Year)
        - ABGAR (Grievances & Appeals)
        - LGHC (Depression Prevalence)
        - Core Set Measures (Mental Health)
        - MAT (Opioid Use Disorders)
        - Tobacco Use (CDPH)
        - Lanterman-Petris-Short (LPS Act)
        - Crisis Services (SMHS OCW)
        - Managed Care Enrollment
        """)
        
    except Exception as e:
        st.error(f"❌ Error loading dashboard: {str(e)}")
        st.info("Make sure the ETL pipeline has been run and CSV files are in output_csv/")

if __name__ == "__main__":
    main()
