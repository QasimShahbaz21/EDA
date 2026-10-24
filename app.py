import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import os

# --- Page Configuration ---
st.set_page_config(
    page_title="Employee Compensation & Performance Analysis",
    page_icon="https://cdn-icons-png.flaticon.com/512/3135/3135715.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Helper for Reliable Clean HTML Rendering ---
def render_html(html_str):
    if hasattr(st, "html"):
        st.html(html_str)
    else:
        clean_str = "\n".join([line.strip() for line in html_str.strip().split("\n")])
        st.markdown(clean_str, unsafe_allow_html=True)

# --- Professional Design System (Google Fonts, Clean Enterprise CSS, Zero Emojis) ---
render_html("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">

<style>
/* Global Clean Typography */
html, body, .stApp {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

h1, h2, h3, h4, h5, h6, p, label, .stMarkdown, .stSelectbox, .stMultiSelect, .stRadio, .stSlider {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

/* Preserve Streamlit Material Icons for sidebar collapse/expand controls */
[data-testid="stIconMaterial"], 
[data-testid="stSidebarCollapseButton"] span, 
[data-testid="collapsedControl"] span,
button[kind="header"] span,
.material-symbols-rounded, 
.material-symbols-outlined, 
.material-icons {
    font-family: 'Material Symbols Rounded', 'Material Symbols Outlined', 'Material Icons' !important;
    font-size: 1.25rem !important;
    letter-spacing: normal !important;
}

/* Base Canvas */
.stApp {
    background-color: #f8fafc;
    color: #0f172a;
}

/* Adjust Streamlit Main Container Spacing */
.block-container {
    padding-top: 1.8rem !important;
    padding-bottom: 3.5rem !important;
    max-width: 1320px;
}

/* Header Navbar */
header[data-testid="stHeader"] {
    background: rgba(248, 250, 252, 0.95);
    backdrop-filter: blur(8px);
}

/* Enterprise Header Card (Clean, Minimalist, No Glow) */
.dashboard-header {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 24px 28px;
    margin-bottom: 20px;
    box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.04);
}
.header-breadcrumb {
    font-size: 0.78rem;
    font-weight: 600;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 6px;
    display: flex;
    align-items: center;
    gap: 6px;
}
.header-title {
    font-size: 1.65rem;
    font-weight: 700;
    color: #0f172a;
    letter-spacing: -0.025em;
    margin: 0 0 8px 0;
    line-height: 1.25;
}
.header-subtitle {
    font-size: 0.9rem;
    color: #475569;
    max-width: 900px;
    line-height: 1.5;
    margin: 0 0 16px 0;
}
.header-meta-row {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 16px;
    padding-top: 12px;
    border-top: 1px solid #f1f5f9;
}
.meta-item {
    font-size: 0.8rem;
    color: #64748b;
    display: inline-flex;
    align-items: center;
    gap: 6px;
}
.meta-dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background-color: #10b981;
}

/* Professional Metric Cards */
.metrics-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
    margin-bottom: 24px;
}
@media (max-width: 900px) {
    .metrics-row {
        grid-template-columns: repeat(2, 1fr);
    }
}
.stat-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 18px 20px;
    box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.03);
    transition: border-color 0.15s ease, box-shadow 0.15s ease;
}
.stat-card:hover {
    border-color: #cbd5e1;
    box-shadow: 0 4px 12px -2px rgba(15, 23, 42, 0.06);
}
.stat-card-top {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 8px;
}
.stat-card-label {
    font-size: 0.75rem;
    font-weight: 600;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
.stat-card-icon {
    color: #64748b;
    display: flex;
    align-items: center;
    justify-content: center;
}
.stat-card-value {
    font-size: 1.75rem;
    font-weight: 700;
    color: #0f172a;
    letter-spacing: -0.03em;
    line-height: 1.2;
    margin-bottom: 6px;
}
.stat-card-sub {
    font-size: 0.8rem;
    color: #64748b;
}

/* Section Dividers and Subheadings */
.module-header {
    margin: 16px 0 14px 0;
}
.module-title {
    font-size: 1.15rem;
    font-weight: 700;
    color: #0f172a;
    letter-spacing: -0.015em;
    margin: 0 0 4px 0;
}
.module-desc {
    font-size: 0.84rem;
    color: #64748b;
    margin: 0;
}

/* Tabs Styling */
div[data-testid="stTabs"] button[role="tab"] {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 600;
    font-size: 0.88rem;
    color: #64748b;
    padding: 10px 18px;
    border-radius: 8px 8px 0 0;
    transition: all 0.15s ease;
}
div[data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
    color: #1e40af !important;
    background: #ffffff;
    border-bottom: 2.5px solid #2563eb !important;
    font-weight: 700;
}

/* Insights Grid */
.insights-container {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 24px;
    margin-top: 24px;
    box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.03);
}
.insights-title {
    font-size: 1.05rem;
    font-weight: 700;
    color: #0f172a;
    margin: 0 0 16px 0;
    display: flex;
    align-items: center;
    gap: 8px;
}
.insights-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
}
@media (max-width: 900px) {
    .insights-grid {
        grid-template-columns: 1fr;
    }
}
.insight-item {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 16px 18px;
}
.insight-header {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 8px;
}
.insight-tag {
    font-size: 0.72rem;
    font-weight: 700;
    color: #2563eb;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
.insight-heading {
    font-size: 0.92rem;
    font-weight: 700;
    color: #0f172a;
    margin: 0 0 6px 0;
}
.insight-text {
    font-size: 0.83rem;
    color: #475569;
    line-height: 1.5;
    margin: 0;
}

/* Sidebar Clean Styling */
section[data-testid="stSidebar"] {
    background-color: #ffffff !important;
    border-right: 1px solid #e2e8f0;
}
.sidebar-panel-header {
    padding-bottom: 12px;
    margin-bottom: 16px;
    border-bottom: 1px solid #e2e8f0;
}
.sidebar-panel-title {
    font-size: 0.95rem;
    font-weight: 700;
    color: #0f172a;
    display: flex;
    align-items: center;
    gap: 8px;
    margin: 0 0 4px 0;
}
.sidebar-panel-desc {
    font-size: 0.78rem;
    color: #64748b;
    margin: 0;
}
.filter-summary-box {
    background: #f1f5f9;
    border: 1px solid #e2e8f0;
    border-radius: 6px;
    padding: 8px 12px;
    font-size: 0.78rem;
    color: #334155;
    margin-top: 14px;
}
.sidebar-note {
    margin-top: 28px;
    padding: 12px;
    border-top: 1px solid #f1f5f9;
    font-size: 0.74rem;
    color: #94a3b8;
    line-height: 1.4;
}
</style>
""")

# --- Matplotlib Custom Theme (Minimalist, Corporate Standard) ---
def set_plot_theme():
    plt.rcParams.update({
        'font.family': 'sans-serif',
        'font.sans-serif': ['Plus Jakarta Sans', 'Segoe UI', 'DejaVu Sans', 'Arial', 'sans-serif'],
        'figure.facecolor': '#ffffff',
        'axes.facecolor': '#ffffff',
        'axes.edgecolor': '#cbd5e1',
        'axes.linewidth': 0.8,
        'axes.labelcolor': '#334155',
        'axes.labelsize': 10,
        'axes.labelweight': 'bold',
        'xtick.color': '#64748b',
        'ytick.color': '#64748b',
        'xtick.labelsize': 9,
        'ytick.labelsize': 9,
        'grid.color': '#f1f5f9',
        'grid.linestyle': '--',
        'grid.alpha': 0.7,
        'figure.autolayout': True
    })

set_plot_theme()

# --- Data Loading & Preprocessing ---
@st.cache_data
def load_data():
    possible_paths = [
        os.path.join(os.path.dirname(__file__), "data", "Messy_Employee_dataset.csv"),
        "data/Messy_Employee_dataset.csv",
        "E:/self/AI_Bootcamp/data/Messy_Employee_dataset.csv"
    ]
    file_path = None
    for p in possible_paths:
        if os.path.exists(p):
            file_path = p
            break
            
    if file_path is None:
        st.error("Dataset not found. Please verify 'data/Messy_Employee_dataset.csv' is present.")
        st.stop()
        
    df = pd.read_csv(file_path)

    # Impute missing values with median (as verified in Lab 6)
    df['Age'] = df['Age'].fillna(df['Age'].median())
    df['Salary'] = df['Salary'].fillna(df['Salary'].median())

    # Fix negative phone numbers
    df['Phone'] = df['Phone'].abs()

    # Split Department and Region
    if 'Department_Region' in df.columns:
        split_dept = df['Department_Region'].str.split('-', n=1, expand=True)
        df['Department'] = split_dept[0]
        df['Region'] = split_dept[1] if split_dept.shape[1] > 1 else 'Unknown'

    # Extract Join Year
    if 'Join_Date' in df.columns:
        df['Join_Year'] = pd.to_datetime(df['Join_Date'], errors='coerce').dt.year

    return df

df = load_data()
total_records = len(df)

# --- Sidebar Controls ---
with st.sidebar:
    render_html("""
    <div class="sidebar-panel-header">
        <div class="sidebar-panel-title">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#2563eb" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><line x1="4" y1="21" x2="4" y2="14"/><line x1="4" y1="10" x2="4" y2="3"/><line x1="12" y1="21" x2="12" y2="12"/><line x1="12" y1="8" x2="12" y2="3"/><line x1="20" y1="21" x2="20" y2="16"/><line x1="20" y1="12" x2="20" y2="3"/><line x1="1" y1="14" x2="7" y2="14"/><line x1="9" y1="8" x2="15" y2="8"/><line x1="17" y1="16" x2="23" y2="16"/></svg>
            Dataset Filters
        </div>
        <p class="sidebar-panel-desc">Slice employee records across dimensions.</p>
    </div>
    """)

    # Department filter
    dept_options = sorted(df['Department'].dropna().unique().tolist())
    selected_depts = st.multiselect(
        "Department:",
        options=dept_options,
        default=dept_options,
        help="Select organizational units."
    )

    # Remote work filter
    work_modes = ["All Workflows", "Remote Only", "In-Office Only"]
    selected_work_mode = st.radio(
        "Work Arrangement:",
        work_modes,
        index=0,
        help="Filter by remote vs in-office status."
    )

    # Performance filter
    performance_ranks = ['Poor', 'Average', 'Good', 'Excellent']
    selected_perf = st.multiselect(
        "Performance Tier:",
        options=performance_ranks,
        default=performance_ranks,
        help="Filter by annual appraisal scores."
    )

    # Salary slider
    min_salary = int(df['Salary'].min())
    max_salary = int(df['Salary'].max())
    salary_range = st.slider(
        "Annual Salary Band ($):",
        min_value=min_salary,
        max_value=max_salary,
        value=(min_salary, max_salary),
        step=5000,
        format="$%d"
    )

    # Apply filters
    filtered_df = df[
        (df['Department'].isin(selected_depts)) &
        (df['Performance_Score'].isin(selected_perf)) &
        (df['Salary'] >= salary_range[0]) &
        (df['Salary'] <= salary_range[1])
    ]

    if selected_work_mode == "Remote Only":
        filtered_df = filtered_df[filtered_df['Remote_Work'] == True]
    elif selected_work_mode == "In-Office Only":
        filtered_df = filtered_df[filtered_df['Remote_Work'] == False]

    matched_count = len(filtered_df)
    coverage_pct = (matched_count / total_records) * 100 if total_records > 0 else 0

    render_html(f"""
    <div class="filter-summary-box">
        Displaying <b>{matched_count:,}</b> of <b>{total_records:,}</b> records ({coverage_pct:.1f}%).
    </div>
    """)

    render_html("""
    <div class="sidebar-note">
        <b>HR Analytics Lab 6</b><br>
        Exploratory Data Analysis Dashboard<br>
        Streamlit & Seaborn
    </div>
    """)

# Empty slice warning
if filtered_df.empty:
    st.warning("No records match your selected filter criteria. Please broaden your sidebar filters.")
    st.stop()

# --- Executive Header Card ---
render_html("""
<div class="dashboard-header">
    <div class="header-breadcrumb">
        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>
        Human Resources / Workforce Analytics / Lab 6
    </div>
    <h1 class="header-title">Employee Compensation & Performance Analysis</h1>
    <p class="header-subtitle">
        An interactive diagnostic dashboard analyzing compensation distribution, performance rating equity, demographic spread, and remote work parity across company records.
    </p>
    <div class="header-meta-row">
        <span class="meta-item">
            <span class="meta-dot"></span>
            Dataset Status: Verified & Cleaned
        </span>
        <span class="meta-item">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
            1,020 Total Records
        </span>
        <span class="meta-item">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="7" width="20" height="14" rx="2" ry="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/></svg>
            6 Departments
        </span>
        <span class="meta-item">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 14 14"/></svg>
            Updated: Q4 2024
        </span>
    </div>
</div>
""")

# --- Summary KPI Metrics Row (With Clean SVG Icons) ---
headcount = len(filtered_df)
mean_sal = filtered_df['Salary'].mean()
med_sal = filtered_df['Salary'].median()
med_age = filtered_df['Age'].median()
remote_tot = filtered_df['Remote_Work'].sum()
remote_ratio = (remote_tot / headcount * 100) if headcount > 0 else 0

render_html(f"""
<div class="metrics-row">
    <div class="stat-card">
        <div class="stat-card-top">
            <span class="stat-card-label">Active Headcount</span>
            <span class="stat-card-icon">
                <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="#475569" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
            </span>
        </div>
        <div class="stat-card-value">{headcount:,}</div>
        <div class="stat-card-sub">{(headcount / total_records * 100):.1f}% of organization</div>
    </div>

    <div class="stat-card">
        <div class="stat-card-top">
            <span class="stat-card-label">Average Annual Salary</span>
            <span class="stat-card-icon">
                <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="#475569" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>
            </span>
        </div>
        <div class="stat-card-value">${mean_sal:,.0f}</div>
        <div class="stat-card-sub">Median: ${med_sal:,.0f}</div>
    </div>

    <div class="stat-card">
        <div class="stat-card-top">
            <span class="stat-card-label">Median Age</span>
            <span class="stat-card-icon">
                <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="#475569" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
            </span>
        </div>
        <div class="stat-card-value">{med_age:.0f} <span style="font-size: 1rem; font-weight: 500; color: #64748b;">years</span></div>
        <div class="stat-card-sub">Range: {filtered_df['Age'].min():.0f} to {filtered_df['Age'].max():.0f} years</div>
    </div>

    <div class="stat-card">
        <div class="stat-card-top">
            <span class="stat-card-label">Remote Work Ratio</span>
            <span class="stat-card-icon">
                <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="#475569" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg>
            </span>
        </div>
        <div class="stat-card-value">{remote_ratio:.1f}%</div>
        <div class="stat-card-sub">{remote_tot:,} remote / {headcount - remote_tot:,} in-office</div>
    </div>
</div>
""")

# --- Visual Analysis Tabs (Clean, Professional Labels, No Emojis) ---
render_html("""
<div class="module-header">
    <h2 class="module-title">Visual Analysis Modules</h2>
    <p class="module-desc">Select a module to view exploratory distributions, correlations, and departmental metrics.</p>
</div>
""")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Salary by Performance",
    "Salary Distribution",
    "Age vs Salary",
    "Department Summary",
    "Data Explorer"
])

# --- Tab 1: Boxplot ---
with tab1:
    render_html("""
    <div style="margin-bottom: 12px;">
        <h3 style="font-size: 1rem; font-weight: 700; color: #0f172a; margin: 0 0 4px 0;">Salary Distribution Across Performance Tiers</h3>
        <p style="font-size: 0.83rem; color: #64748b; margin: 0;">Evaluation of whether higher appraisal scores correspond to elevated salary bands.</p>
    </div>
    """)

    fig1, ax1 = plt.subplots(figsize=(8.5, 4.3), dpi=140)
    perf_present = [p for p in performance_ranks if p in filtered_df['Performance_Score'].unique()]
    
    # Classic professional monochromatic blue palette
    palette_box = ['#cbd5e1', '#93c5fd', '#60a5fa', '#2563eb'][:len(perf_present)]
    
    sns.boxplot(
        data=filtered_df,
        x='Performance_Score',
        y='Salary',
        order=perf_present,
        palette=palette_box,
        showmeans=True,
        meanprops={
            "marker": "D", 
            "markeredgecolor": "#0f172a", 
            "markerfacecolor": "#f59e0b", 
            "markersize": "6.5"
        },
        boxprops=dict(alpha=0.85, edgecolor='#1e293b', linewidth=1.1),
        medianprops=dict(color="#b91c1c", linewidth=2),
        whiskerprops=dict(color="#475569", linewidth=1.1),
        capprops=dict(color="#475569", linewidth=1.1),
        ax=ax1
    )

    ax1.set_title("Salary Distribution by Performance Score (Gold Diamond = Mean, Red Line = Median)", 
                  fontsize=10.5, fontweight='bold', pad=12, color='#0f172a')
    ax1.set_xlabel("Performance Rating", fontsize=9.5, fontweight='bold', labelpad=6)
    ax1.set_ylabel("Annual Salary ($)", fontsize=9.5, fontweight='bold', labelpad=6)
    ax1.yaxis.set_major_formatter(ticker.StrMethodFormatter('${x:,.0f}'))
    ax1.grid(axis='y', linestyle='--', alpha=0.5)
    sns.despine(top=True, right=True)
    
    st.pyplot(fig1)

    st.markdown("""
    **Observation:** Across all four performance tiers, median salaries remain constant at approximately **$85,548**. In this organization, performance appraisal ratings do not dictate base salary bands.
    """)

# --- Tab 2: Histogram with KDE ---
with tab2:
    render_html("""
    <div style="margin-bottom: 12px;">
        <h3 style="font-size: 1rem; font-weight: 700; color: #0f172a; margin: 0 0 4px 0;">Workforce Salary Distribution</h3>
        <p style="font-size: 0.83rem; color: #64748b; margin: 0;">Frequency distribution and continuous density curve across the selected employee cohort.</p>
    </div>
    """)

    fig2, ax2 = plt.subplots(figsize=(8.5, 4.3), dpi=140)
    
    sns.histplot(
        filtered_df['Salary'],
        kde=True,
        color='#2563eb',
        bins=22,
        line_kws={'linewidth': 2, 'color': '#1e3a8a'},
        edgecolor='#cbd5e1',
        alpha=0.45,
        ax=ax2
    )
    
    cur_mean = filtered_df['Salary'].mean()
    cur_median = filtered_df['Salary'].median()
    
    ax2.axvline(cur_mean, color='#b91c1c', linestyle='--', linewidth=1.8, label=f"Mean: ${cur_mean:,.0f}")
    ax2.axvline(cur_median, color='#15803d', linestyle=':', linewidth=2, label=f"Median: ${cur_median:,.0f}")
    
    ax2.set_title("Salary Frequency Histogram with Kernel Density Estimate", 
                  fontsize=10.5, fontweight='bold', pad=12, color='#0f172a')
    ax2.set_xlabel("Annual Salary ($)", fontsize=9.5, fontweight='bold', labelpad=6)
    ax2.set_ylabel("Employee Count", fontsize=9.5, fontweight='bold', labelpad=6)
    ax2.xaxis.set_major_formatter(ticker.StrMethodFormatter('${x:,.0f}'))
    ax2.grid(axis='y', linestyle='--', alpha=0.5)
    ax2.legend(frameon=True, facecolor='#ffffff', edgecolor='#cbd5e1', fontsize=8.5)
    sns.despine(top=True, right=True)
    
    st.pyplot(fig2)

    st.markdown("""
    **Observation:** Salaries form a symmetrical bell curve bounded between **$30,000** and **$140,000**. The near-perfect alignment of the mean ($85,548) and median ($85,548) indicates negligible skewness.
    """)

# --- Tab 3: Scatter Plot ---
with tab3:
    render_html("""
    <div style="margin-bottom: 12px;">
        <h3 style="font-size: 1rem; font-weight: 700; color: #0f172a; margin: 0 0 4px 0;">Age vs Salary by Remote Work Arrangement</h3>
        <p style="font-size: 0.83rem; color: #64748b; margin: 0;">Evaluation of correlation between employee age, remote work status, and compensation.</p>
    </div>
    """)

    fig3, ax3 = plt.subplots(figsize=(8.5, 4.3), dpi=140)
    
    palette_scatter = {True: '#2563eb', False: '#64748b'}
    
    sns.scatterplot(
        data=filtered_df,
        x='Age',
        y='Salary',
        hue='Remote_Work',
        palette=palette_scatter,
        alpha=0.7,
        s=48,
        edgecolor='#ffffff',
        linewidth=0.5,
        ax=ax3
    )
    
    # Regression trendline
    sns.regplot(
        data=filtered_df,
        x='Age',
        y='Salary',
        scatter=False,
        color='#0f172a',
        line_kws={'linestyle': '--', 'linewidth': 1.5, 'alpha': 0.6, 'label': 'Trend Line'},
        ax=ax3
    )
    
    ax3.set_title("Age vs Salary Correlation (Colored by Remote Work Policy)", 
                  fontsize=10.5, fontweight='bold', pad=12, color='#0f172a')
    ax3.set_xlabel("Age (Years)", fontsize=9.5, fontweight='bold', labelpad=6)
    ax3.set_ylabel("Annual Salary ($)", fontsize=9.5, fontweight='bold', labelpad=6)
    ax3.yaxis.set_major_formatter(ticker.StrMethodFormatter('${x:,.0f}'))
    ax3.legend(title="Work Mode", labels=["Remote", "In-Office", "Trend"], 
               frameon=True, facecolor='#ffffff', edgecolor='#cbd5e1', fontsize=8.5)
    ax3.grid(True, linestyle='--', alpha=0.4)
    sns.despine(top=True, right=True)
    
    st.pyplot(fig3)

    st.markdown("""
    **Observation:** The flat regression line confirms zero correlation between worker age and compensation. Remote employees and in-office staff display identical salary distributions across all age ranges.
    """)

# --- Tab 4: Department Summary ---
with tab4:
    render_html("""
    <div style="margin-bottom: 12px;">
        <h3 style="font-size: 1rem; font-weight: 700; color: #0f172a; margin: 0 0 4px 0;">Departmental Compensation Comparison</h3>
        <p style="font-size: 0.83rem; color: #64748b; margin: 0;">Ranked comparison of average compensation and headcount by business unit.</p>
    </div>
    """)

    dept_metrics = filtered_df.groupby('Department').agg(
        Avg_Salary=('Salary', 'mean'),
        Median_Salary=('Salary', 'median'),
        Headcount=('Employee_ID', 'count')
    ).reset_index().sort_values(by='Avg_Salary', ascending=True)

    fig4, ax4 = plt.subplots(figsize=(8.5, 4.0), dpi=140)
    bars = ax4.barh(dept_metrics['Department'], dept_metrics['Avg_Salary'], color='#3b82f6', alpha=0.85, edgecolor='#1e3a8a', height=0.52)
    
    for bar, (_, row) in zip(bars, dept_metrics.iterrows()):
        ax4.text(bar.get_width() + 1000, bar.get_y() + bar.get_height()/2, 
                 f"${row['Avg_Salary']:,.0f} (n={row['Headcount']})", 
                 va='center', fontsize=8.5, fontweight='bold', color='#1e293b')

    ax4.set_xlim(0, max(dept_metrics['Avg_Salary']) * 1.22)
    ax4.set_title("Average Annual Salary by Department (Ranked)", fontsize=10.5, fontweight='bold', pad=12)
    ax4.set_xlabel("Average Salary ($)", fontsize=9.5, fontweight='bold', labelpad=6)
    ax4.xaxis.set_major_formatter(ticker.StrMethodFormatter('${x:,.0f}'))
    ax4.grid(axis='x', linestyle='--', alpha=0.5)
    sns.despine(top=True, right=True)
    
    st.pyplot(fig4)

    st.markdown("""
    **Observation:** Organizational pay bands are tightly standardized. Across all 6 divisions, average salaries range narrowly between **$83,912** (HR) and **$87,143** (Sales) — a variance of under 3.9%.
    """)

# --- Tab 5: Data Explorer ---
with tab5:
    render_html("""
    <div style="margin-bottom: 12px;">
        <h3 style="font-size: 1rem; font-weight: 700; color: #0f172a; margin: 0 0 4px 0;">Filtered Dataset Explorer</h3>
        <p style="font-size: 0.83rem; color: #64748b; margin: 0;">Review raw records and export filtered tables for reporting.</p>
    </div>
    """)

    col_btn1, col_btn2 = st.columns([3, 1])
    with col_btn1:
        st.caption(f"Showing {len(filtered_df):,} matching employee records.")
    with col_btn2:
        csv_export = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Filtered CSV",
            data=csv_export,
            file_name="workforce_data_filtered.csv",
            mime="text/csv",
            use_container_width=True
        )

    st.dataframe(
        filtered_df[['Employee_ID', 'First_Name', 'Last_Name', 'Department', 'Region', 'Age', 'Salary', 'Performance_Score', 'Remote_Work']],
        use_container_width=True,
        hide_index=True
    )

    st.markdown("#### Summary Statistics")
    st.dataframe(filtered_df[['Age', 'Salary']].describe().T.style.format("{:,.2f}"), use_container_width=True)

# --- Executive Summary Card (Professional, No Emojis) ---
render_html("""
<div class="insights-container">
    <div class="insights-title">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#2563eb" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>
        Executive Findings & Strategic Summary
    </div>
    
    <div class="insights-grid">
        <div class="insight-item">
            <div class="insight-header">
                <span class="insight-tag">Compensation Equity</span>
            </div>
            <h4 class="insight-heading">Performance Ratings Decoupled from Pay</h4>
            <p class="insight-text">
                Median compensation across all four appraisal tiers (Poor to Excellent) is identical at <b>$85,548</b>. Performance evaluations do not influence base salary distributions.
            </p>
        </div>

        <div class="insight-item">
            <div class="insight-header">
                <span class="insight-tag">Workplace Policy</span>
            </div>
            <h4 class="insight-heading">Full Hybrid Compensation Parity</h4>
            <p class="insight-text">
                <b>50.3%</b> of the workforce operates remotely. Average pay for remote employees (<b>$85,468</b>) is on exact parity with in-office staff (<b>$85,584</b>), showing zero location penalty.
            </p>
        </div>

        <div class="insight-item">
            <div class="insight-header">
                <span class="insight-tag">Organizational Structure</span>
            </div>
            <h4 class="insight-heading">Tight Departmental Banding</h4>
            <p class="insight-text">
                Average departmental wages are rigidly standardized between <b>$83,912</b> (HR) and <b>$87,143</b> (Sales) — a variance of less than 3.9% across all six divisions.
            </p>
        </div>
    </div>
</div>
""")
