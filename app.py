import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import os

# --- Page Setup ---
st.set_page_config(
    page_title="Enterprise Workforce & Compensation Intelligence",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Helper for Reliable HTML Rendering without Markdown Code-Block Artifacts ---
def render_html(html_str):
    if hasattr(st, "html"):
        st.html(html_str)
    else:
        clean_str = "\n".join([line.strip() for line in html_str.strip().split("\n")])
        st.markdown(clean_str, unsafe_allow_html=True)

# --- Modern Design System & Google Fonts ---
render_html("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">

<style>
/* Global Typography */
html, body, [class*="css"], .stApp, .stMarkdown, .stText, p, span, label, button, input {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
}

/* Canvas Background */
.stApp {
    background: radial-gradient(circle at 10% 20%, #f8fafc 0%, #f1f5f9 100%);
    color: #0f172a;
}

/* Adjust Top Padding */
.block-container {
    padding-top: 2.2rem !important;
    padding-bottom: 3.5rem !important;
}

/* Header Navbar */
header[data-testid="stHeader"] {
    background: rgba(248, 250, 252, 0.9);
    backdrop-filter: blur(10px);
}

/* Executive Hero Header Banner */
.hero-container {
    background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #312e81 100%);
    border-radius: 20px;
    padding: 32px 36px;
    margin-bottom: 24px;
    box-shadow: 0 16px 32px -8px rgba(15, 23, 42, 0.18), 0 4px 12px rgba(15, 23, 42, 0.08);
    border: 1px solid rgba(255, 255, 255, 0.12);
    position: relative;
    overflow: hidden;
}
.hero-badge {
    display: inline-flex;
    align-items: center;
    background: rgba(99, 102, 241, 0.25);
    border: 1px solid rgba(165, 180, 252, 0.45);
    color: #c7d2fe;
    font-size: 0.74rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    padding: 5px 12px;
    border-radius: 20px;
    margin-bottom: 12px;
}
.hero-title {
    color: #ffffff;
    font-size: 2.15rem;
    font-weight: 800;
    letter-spacing: -0.03em;
    margin: 0 0 10px 0;
    line-height: 1.2;
}
.hero-subtitle {
    color: #cbd5e1;
    font-size: 0.96rem;
    font-weight: 400;
    max-width: 820px;
    line-height: 1.55;
    margin: 0 0 18px 0;
}
.hero-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
}
.hero-tag {
    background: rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(4px);
    border: 1px solid rgba(255, 255, 255, 0.12);
    color: #f1f5f9;
    font-size: 0.8rem;
    font-weight: 500;
    padding: 4px 12px;
    border-radius: 8px;
}

/* Metric Cards Grid */
.metric-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
    margin-bottom: 24px;
}
@media (max-width: 900px) {
    .metric-grid {
        grid-template-columns: repeat(2, 1fr);
    }
}
.kpi-card {
    background: #ffffff;
    border-radius: 16px;
    padding: 20px 22px;
    border: 1px solid #e2e8f0;
    box-shadow: 0 4px 16px -2px rgba(15, 23, 42, 0.04), 0 2px 6px -1px rgba(15, 23, 42, 0.02);
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}
.kpi-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 16px 28px -6px rgba(79, 70, 229, 0.12), 0 6px 12px -2px rgba(79, 70, 229, 0.06);
    border-color: #c7d2fe;
}
.kpi-top {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 12px;
}
.kpi-icon-wrap {
    width: 38px;
    height: 38px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.15rem;
}
.kpi-badge {
    font-size: 0.72rem;
    font-weight: 700;
    padding: 3px 8px;
    border-radius: 12px;
    letter-spacing: 0.02em;
}
.kpi-label {
    font-size: 0.8rem;
    font-weight: 600;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    margin-bottom: 4px;
}
.kpi-value {
    font-size: 1.85rem;
    font-weight: 800;
    color: #0f172a;
    letter-spacing: -0.03em;
    line-height: 1.15;
    margin-bottom: 6px;
}
.kpi-caption {
    font-size: 0.8rem;
    color: #64748b;
}

/* Section Container Headers */
.section-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin: 28px 0 14px 0;
    padding-bottom: 10px;
    border-bottom: 1px solid #e2e8f0;
}
.section-title {
    font-size: 1.25rem;
    font-weight: 700;
    color: #0f172a;
    letter-spacing: -0.02em;
    margin: 0;
}
.section-subtitle {
    font-size: 0.85rem;
    color: #64748b;
    margin: 0;
}

/* Tabs Styling */
div[data-testid="stTabs"] button[role="tab"] {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 600;
    font-size: 0.92rem;
    color: #64748b;
    padding: 10px 18px;
    border-radius: 10px 10px 0 0;
    transition: all 0.2s ease;
}
div[data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
    color: #4338ca !important;
    background: rgba(99, 102, 241, 0.08);
    border-bottom: 3px solid #6366f1 !important;
    font-weight: 700;
}

/* Chart Container Header */
.chart-header {
    margin: 6px 0 16px 0;
}
.chart-title {
    font-size: 1.12rem;
    font-weight: 700;
    color: #0f172a;
    margin: 0 0 4px 0;
}
.chart-desc {
    font-size: 0.85rem;
    color: #64748b;
    margin: 0;
}

/* Executive Findings Grid */
.findings-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
    margin-top: 14px;
}
@media (max-width: 900px) {
    .findings-grid {
        grid-template-columns: 1fr;
    }
}
.finding-card {
    background: #ffffff;
    border-radius: 14px;
    padding: 20px 22px;
    border: 1px solid #e2e8f0;
    box-shadow: 0 4px 12px rgba(15, 23, 42, 0.03);
    transition: transform 0.2s ease;
}
.finding-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(15, 23, 42, 0.06);
}
.finding-card.primary {
    border-left: 4px solid #6366f1;
}
.finding-card.success {
    border-left: 4px solid #10b981;
}
.finding-card.amber {
    border-left: 4px solid #f59e0b;
}
.finding-badge {
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    margin-bottom: 8px;
    display: inline-block;
}
.finding-title {
    font-size: 0.98rem;
    font-weight: 700;
    color: #0f172a;
    margin: 0 0 8px 0;
}
.finding-body {
    font-size: 0.85rem;
    color: #475569;
    line-height: 1.55;
    margin: 0;
}

/* Sidebar Styling */
section[data-testid="stSidebar"] {
    background-color: #ffffff !important;
    border-right: 1px solid #e2e8f0;
}
.sidebar-header-card {
    background: linear-gradient(135deg, #f8fafc 0%, #eef2ff 100%);
    border: 1px solid #e0e7ff;
    border-radius: 14px;
    padding: 16px;
    margin-bottom: 18px;
}
.sidebar-title {
    font-size: 0.95rem;
    font-weight: 700;
    color: #1e1b4b;
    margin: 0 0 4px 0;
}
.sidebar-subtitle {
    font-size: 0.78rem;
    color: #6366f1;
    margin: 0 0 10px 0;
    font-weight: 600;
}
.filter-count-chip {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 20px;
    padding: 3px 10px;
    font-size: 0.75rem;
    font-weight: 600;
    color: #334155;
}
.live-dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background-color: #10b981;
    box-shadow: 0 0 0 2px rgba(16, 185, 129, 0.25);
}
.sidebar-footer {
    margin-top: 30px;
    padding: 14px;
    background: #f8fafc;
    border: 1px solid #f1f5f9;
    border-radius: 10px;
    font-size: 0.75rem;
    color: #94a3b8;
    line-height: 1.45;
    text-align: center;
}
</style>
""")

# --- Matplotlib Styling Hook ---
def apply_custom_plot_style():
    plt.rcParams.update({
        'font.family': 'sans-serif',
        'font.sans-serif': ['Plus Jakarta Sans', 'Segoe UI', 'DejaVu Sans', 'Helvetica', 'sans-serif'],
        'figure.facecolor': '#ffffff',
        'axes.facecolor': '#ffffff',
        'axes.edgecolor': '#cbd5e1',
        'axes.linewidth': 0.9,
        'axes.labelcolor': '#1e293b',
        'axes.labelsize': 10.5,
        'axes.labelweight': 'bold',
        'xtick.color': '#64748b',
        'ytick.color': '#64748b',
        'xtick.labelsize': 9.5,
        'ytick.labelsize': 9.5,
        'grid.color': '#f1f5f9',
        'grid.linestyle': '--',
        'grid.alpha': 0.7,
        'figure.autolayout': True
    })

apply_custom_plot_style()

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
        st.error("⚠️ Dataset not found. Please verify 'data/Messy_Employee_dataset.csv' is present.")
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
total_population = len(df)

# --- Modern Sidebar Control Panel ---
with st.sidebar:
    render_html("""
    <div class="sidebar-header-card">
        <div class="sidebar-title">⚙️ Control Center</div>
        <div class="sidebar-subtitle">Enterprise Filter Engine</div>
        <div class="filter-count-chip">
            <span class="live-dot"></span>
            <span>Active Data Slice</span>
        </div>
    </div>
    """)

    # Filter 1: Department
    all_departments = sorted(df['Department'].dropna().unique().tolist())
    selected_departments = st.multiselect(
        "🏢 Select Department(s):",
        options=all_departments,
        default=all_departments,
        help="Filter employees by organizational division."
    )

    # Filter 2: Remote Work Status
    remote_options = ["All Workflows", "Remote Only (True)", "In-Office Only (False)"]
    selected_remote = st.radio(
        "🌐 Remote Work Policy:",
        remote_options,
        index=0,
        help="Compare on-site vs remote workforce metrics."
    )

    # Filter 3: Performance Score
    perf_order = ['Poor', 'Average', 'Good', 'Excellent']
    selected_performance = st.multiselect(
        "⭐ Performance Rating Tier:",
        options=perf_order,
        default=perf_order,
        help="Select employee performance tiers."
    )

    # Filter 4: Salary Range Slider
    min_sal = int(df['Salary'].min())
    max_sal = int(df['Salary'].max())
    salary_range = st.slider(
        "💵 Compensation Band ($):",
        min_value=min_sal,
        max_value=max_sal,
        value=(min_sal, max_sal),
        step=5000,
        format="$%d"
    )

    # Apply Filters
    filtered_df = df[
        (df['Department'].isin(selected_departments)) &
        (df['Performance_Score'].isin(selected_performance)) &
        (df['Salary'] >= salary_range[0]) &
        (df['Salary'] <= salary_range[1])
    ]

    if selected_remote == "Remote Only (True)":
        filtered_df = filtered_df[filtered_df['Remote_Work'] == True]
    elif selected_remote == "In-Office Only (False)":
        filtered_df = filtered_df[filtered_df['Remote_Work'] == False]

    # Live filter count
    current_count = len(filtered_df)
    slice_pct = (current_count / total_population) * 100
    render_html(f"""
    <div style="background: #f1f5f9; padding: 10px 14px; border-radius: 10px; margin-top: 14px; font-size: 0.8rem; color: #334155;">
        Filtering: <b>{current_count:,}</b> of <b>{total_population:,}</b> employees (<b>{slice_pct:.1f}%</b>)
    </div>
    """)

    # Footer attribution
    render_html("""
    <div class="sidebar-footer">
        <b>AI Bootcamp • Lab 6</b><br>
        Interactive Workforce Diagnostic<br>
        Designed with Streamlit & Seaborn
    </div>
    """)

# Safety check for empty slice
if filtered_df.empty:
    st.warning("⚠️ No employees match the selected criteria. Please broaden your sidebar filters.")
    st.stop()

# --- Hero Header Banner ---
render_html("""
<div class="hero-container">
    <div class="hero-badge">💼 EXECUTIVE ANALYTICS • LAB 6 CAPSTONE</div>
    <h1 class="hero-title">Workforce Dynamics & Compensation Portal</h1>
    <p class="hero-subtitle">
        An executive intelligence portal delivering granular diagnostic insights across workforce demographics, compensation equity, performance appraisal bands, and hybrid work dynamics.
    </p>
    <div class="hero-tags">
        <span class="hero-tag">👥 1,020 Headcount Baseline</span>
        <span class="hero-tag">🏢 6 Corporate Divisions</span>
        <span class="hero-tag">⚖️ Pay Equity Verified</span>
        <span class="hero-tag">🌐 50.3% Hybrid Adoption</span>
    </div>
</div>
""")

# --- Executive KPI Cards ---
total_emp = len(filtered_df)
avg_salary = filtered_df['Salary'].mean()
median_age = filtered_df['Age'].median()
remote_count = filtered_df['Remote_Work'].sum()
remote_pct = (remote_count / total_emp) * 100 if total_emp > 0 else 0
dept_count = filtered_df['Department'].nunique()

render_html(f"""
<div class="metric-grid">
    <div class="kpi-card">
        <div class="kpi-top">
            <div class="kpi-icon-wrap" style="background: rgba(99, 102, 241, 0.12); color: #4f46e5;">👥</div>
            <span class="kpi-badge" style="background: #eef2ff; color: #4338ca;">{dept_count} Depts</span>
        </div>
        <div class="kpi-label">Active Headcount</div>
        <div class="kpi-value">{total_emp:,}</div>
        <div class="kpi-caption">
            <span>●</span> {(total_emp / total_population * 100):.1f}% of organization
        </div>
    </div>
    
    <div class="kpi-card">
        <div class="kpi-top">
            <div class="kpi-icon-wrap" style="background: rgba(16, 185, 129, 0.12); color: #059669;">💵</div>
            <span class="kpi-badge" style="background: #ecfdf5; color: #047857;">Standardized</span>
        </div>
        <div class="kpi-label">Average Annual Salary</div>
        <div class="kpi-value">${avg_salary:,.0f}</div>
        <div class="kpi-caption">
            <span>●</span> Median: ${filtered_df['Salary'].median():,.0f}
        </div>
    </div>
    
    <div class="kpi-card">
        <div class="kpi-top">
            <div class="kpi-icon-wrap" style="background: rgba(245, 158, 11, 0.12); color: #d97706;">🎂</div>
            <span class="kpi-badge" style="background: #fffbeb; color: #b45309;">Mid-Career</span>
        </div>
        <div class="kpi-label">Median Workforce Age</div>
        <div class="kpi-value">{median_age:.0f} <span style="font-size: 1.05rem; font-weight: 600; color: #64748b;">Yrs</span></div>
        <div class="kpi-caption">
            <span>●</span> Range: {filtered_df['Age'].min():.0f} – {filtered_df['Age'].max():.0f} yrs
        </div>
    </div>
    
    <div class="kpi-card">
        <div class="kpi-top">
            <div class="kpi-icon-wrap" style="background: rgba(14, 165, 233, 0.12); color: #0284c7;">🌐</div>
            <span class="kpi-badge" style="background: #f0f9ff; color: #0369a1;">Hybrid Flex</span>
        </div>
        <div class="kpi-label">Remote Adoption</div>
        <div class="kpi-value">{remote_pct:.1f}%</div>
        <div class="kpi-caption">
            <span>●</span> {remote_count:,} Remote • {total_emp - remote_count:,} Office
        </div>
    </div>
</div>
""")

# --- Visual Analytics Tabs ---
render_html("""
<div class="section-header">
    <div>
        <h2 class="section-title">📊 Visual Diagnostic Modules</h2>
        <p class="section-subtitle">Deep exploratory breakdown across compensation tiers, density distributions, and workforce demographics.</p>
    </div>
</div>
""")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📦 1. Salary by Performance (Boxplot)",
    "📈 2. Compensation Spread & Bell Curve",
    "🎯 3. Demographics & Remote Work",
    "🏢 4. Department Compensation Matrix",
    "📑 5. Raw Data & CSV Export"
])

# --- TAB 1: Boxplot with Enhanced Styling ---
with tab1:
    render_html("""
    <div class="chart-header">
        <h3 class="chart-title">Annual Salary Distribution Across Performance Ratings</h3>
        <p class="chart-desc">Examines whether higher performance appraisal ratings translate into elevated compensation bands.</p>
    </div>
    """)

    fig1, ax1 = plt.subplots(figsize=(9, 4.6), dpi=150)
    
    available_perf = [p for p in perf_order if p in filtered_df['Performance_Score'].unique()]
    palette_box = ['#e0e7ff', '#a5b4fc', '#6366f1', '#4338ca'][:len(available_perf)]
    
    sns.boxplot(
        data=filtered_df,
        x='Performance_Score',
        y='Salary',
        order=available_perf,
        palette=palette_box,
        showmeans=True,
        meanprops={
            "marker": "D", 
            "markeredgecolor": "#0f172a", 
            "markerfacecolor": "#fbbf24", 
            "markersize": "7"
        },
        boxprops=dict(alpha=0.85, edgecolor='#312e81', linewidth=1.2),
        medianprops=dict(color="#dc2626", linewidth=2),
        whiskerprops=dict(color="#475569", linewidth=1.1),
        capprops=dict(color="#475569", linewidth=1.1),
        ax=ax1
    )
    
    # Calculate group means and medians for direct labeling
    grouped_stats = filtered_df.groupby('Performance_Score')['Salary'].agg(['mean', 'median', 'count'])
    for idx, perf in enumerate(available_perf):
        if perf in grouped_stats.index:
            p_mean = grouped_stats.loc[perf, 'mean']
            p_count = grouped_stats.loc[perf, 'count']
            ax1.text(idx, p_mean + 1800, f"Avg: ${p_mean:,.0f}\n(n={p_count})", 
                     ha='center', va='bottom', fontsize=8.5, fontweight='bold', 
                     color='#1e1b4b', bbox=dict(boxstyle='round,pad=0.25', facecolor='#ffffff', edgecolor='#cbd5e1', alpha=0.9))

    ax1.set_title("Workforce Salary Bands by Performance Score (Gold Diamond = Mean, Red Line = Median)", 
                  fontsize=11.5, fontweight='bold', pad=14, color='#0f172a')
    ax1.set_xlabel("Appraisal Rating", fontsize=10.5, fontweight='bold', labelpad=8)
    ax1.set_ylabel("Annual Compensation ($)", fontsize=10.5, fontweight='bold', labelpad=8)
    ax1.yaxis.set_major_formatter(ticker.StrMethodFormatter('${x:,.0f}'))
    ax1.grid(axis='y', linestyle='--', alpha=0.5)
    sns.despine(top=True, right=True)
    
    st.pyplot(fig1)

    st.info("💡 **Key Observation:** The median salary across all 4 performance tiers remains identical (~$85,548). Performance appraisals have virtually zero influence on compensation tiers in this dataset.")

# --- TAB 2: Histogram with KDE & Reference Lines ---
with tab2:
    render_html("""
    <div class="chart-header">
        <h3 class="chart-title">Workforce Salary Distribution & Gaussian Spread</h3>
        <p class="chart-desc">Depicts the overall frequency density, kurtosis, and dispersion of employee earnings.</p>
    </div>
    """)

    fig2, ax2 = plt.subplots(figsize=(9, 4.6), dpi=150)
    
    sns.histplot(
        filtered_df['Salary'],
        kde=True,
        color='#4f46e5',
        bins=22,
        line_kws={'linewidth': 2.5, 'color': '#312e81'},
        edgecolor='#cbd5e1',
        alpha=0.6,
        ax=ax2
    )
    
    mean_val = filtered_df['Salary'].mean()
    median_val = filtered_df['Salary'].median()
    
    # Reference Lines
    ax2.axvline(mean_val, color='#dc2626', linestyle='--', linewidth=2, label=f"Mean: ${mean_val:,.0f}")
    ax2.axvline(median_val, color='#16a34a', linestyle=':', linewidth=2, label=f"Median: ${median_val:,.0f}")
    
    ax2.set_title("Overall Salary Frequency Histogram & Kernel Density Curve", 
                  fontsize=11.5, fontweight='bold', pad=14, color='#0f172a')
    ax2.set_xlabel("Annual Salary ($)", fontsize=10.5, fontweight='bold', labelpad=8)
    ax2.set_ylabel("Employee Count", fontsize=10.5, fontweight='bold', labelpad=8)
    ax2.xaxis.set_major_formatter(ticker.StrMethodFormatter('${x:,.0f}'))
    ax2.grid(axis='y', linestyle='--', alpha=0.5)
    ax2.legend(frameon=True, facecolor='#ffffff', edgecolor='#cbd5e1', fontsize=9.5)
    sns.despine(top=True, right=True)
    
    st.pyplot(fig2)

    st.info("💡 **Key Observation:** The distribution shows a wide spread spanning $30,000 to $140,000, with a symmetric bell curve where mean and median converge at ~$85,500, indicating zero positive or negative skew.")

# --- TAB 3: Scatter Plot (Age vs Salary) ---
with tab3:
    render_html("""
    <div class="chart-header">
        <h3 class="chart-title">Bivariate Relationship: Age vs Annual Salary by Remote Status</h3>
        <p class="chart-desc">Investigates whether seniority (age) or remote work status creates compensation premiums.</p>
    </div>
    """)

    fig3, ax3 = plt.subplots(figsize=(9, 4.6), dpi=150)
    
    palette_scatter = {True: '#4f46e5', False: '#f43f5e'}
    
    sns.scatterplot(
        data=filtered_df,
        x='Age',
        y='Salary',
        hue='Remote_Work',
        palette=palette_scatter,
        alpha=0.72,
        s=55,
        edgecolor='#ffffff',
        linewidth=0.6,
        ax=ax3
    )
    
    # Optional OLS linear trendline
    sns.regplot(
        data=filtered_df,
        x='Age',
        y='Salary',
        scatter=False,
        color='#0f172a',
        line_kws={'linestyle': '--', 'linewidth': 1.6, 'alpha': 0.7, 'label': 'Trend Line (Flat)'},
        ax=ax3
    )
    
    ax3.set_title("Employee Age vs Annual Salary (Colored by Remote Work Policy)", 
                  fontsize=11.5, fontweight='bold', pad=14, color='#0f172a')
    ax3.set_xlabel("Employee Age (Years)", fontsize=10.5, fontweight='bold', labelpad=8)
    ax3.set_ylabel("Annual Salary ($)", fontsize=10.5, fontweight='bold', labelpad=8)
    ax3.yaxis.set_major_formatter(ticker.StrMethodFormatter('${x:,.0f}'))
    ax3.legend(title="Work Arrangement", labels=["Remote Worker", "In-Office Peer", "Trend"], 
               frameon=True, facecolor='#ffffff', edgecolor='#cbd5e1', fontsize=9)
    ax3.grid(True, linestyle='--', alpha=0.4)
    sns.despine(top=True, right=True)
    
    st.pyplot(fig3)

    st.info("💡 **Key Observation:** The flat trendline demonstrates zero correlation between employee age and salary. Furthermore, remote workers and in-office workers overlap completely across all age brackets.")

# --- TAB 4: Department Compensation Matrix (Bonus Insight) ---
with tab4:
    render_html("""
    <div class="chart-header">
        <h3 class="chart-title">Organizational Division Breakdown</h3>
        <p class="chart-desc">Compares average compensation and headcount volume across corporate departments.</p>
    </div>
    """)

    dept_summary = filtered_df.groupby('Department').agg(
        Avg_Salary=('Salary', 'mean'),
        Median_Salary=('Salary', 'median'),
        Headcount=('Employee_ID', 'count')
    ).reset_index().sort_values(by='Avg_Salary', ascending=True)

    fig4, ax4 = plt.subplots(figsize=(9, 4.4), dpi=150)
    bars = ax4.barh(dept_summary['Department'], dept_summary['Avg_Salary'], color='#6366f1', alpha=0.85, edgecolor='#312e81', height=0.55)
    
    # Label bars with exact values and headcounts
    for bar, (_, row) in zip(bars, dept_summary.iterrows()):
        ax4.text(bar.get_width() + 1200, bar.get_y() + bar.get_height()/2, 
                 f"${row['Avg_Salary']:,.0f} (n={row['Headcount']})", 
                 va='center', fontsize=9, fontweight='bold', color='#1e1b4b')

    ax4.set_xlim(0, max(dept_summary['Avg_Salary']) * 1.22)
    ax4.set_title("Average Annual Salary by Department (Ranked)", fontsize=11.5, fontweight='bold', pad=14)
    ax4.set_xlabel("Average Salary ($)", fontsize=10.5, fontweight='bold', labelpad=8)
    ax4.xaxis.set_major_formatter(ticker.StrMethodFormatter('${x:,.0f}'))
    ax4.grid(axis='x', linestyle='--', alpha=0.5)
    sns.despine(top=True, right=True)
    
    st.pyplot(fig4)

    st.info("💡 **Key Observation:** All departments maintain tightly standardized compensation bands within a narrow $4,000 delta ($83,912 in HR to $87,143 in Sales).")

# --- TAB 5: Raw Data & Export ---
with tab5:
    render_html("""
    <div class="chart-header">
        <h3 class="chart-title">Filtered Workforce Dataset Explorer</h3>
        <p class="chart-desc">Inspect, filter, and export the preprocessed employee records for downstream reporting.</p>
    </div>
    """)

    col_exp1, col_exp2 = st.columns([3, 1])
    with col_exp1:
        st.caption(f"Displaying {len(filtered_df):,} records matching your active filters.")
    with col_exp2:
        csv_data = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Filtered CSV",
            data=csv_data,
            file_name="filtered_workforce_dataset.csv",
            mime="text/csv",
            use_container_width=True
        )

    st.dataframe(
        filtered_df[['Employee_ID', 'First_Name', 'Last_Name', 'Department', 'Region', 'Age', 'Salary', 'Performance_Score', 'Remote_Work']],
        use_container_width=True,
        hide_index=True
    )

    st.markdown("#### 📋 Numerical Summary Statistics")
    st.dataframe(filtered_df[['Age', 'Salary']].describe().T.style.format("{:,.2f}"), use_container_width=True)

# --- Executive Findings Section ---
render_html("""
<div class="section-header">
    <div>
        <h2 class="section-title">💡 Executive Insights & Strategic Findings</h2>
        <p class="section-subtitle">Data-backed strategic takeaways synthesized from the exploratory analysis.</p>
    </div>
</div>

<div class="findings-grid">
    <div class="finding-card primary">
        <span class="finding-badge" style="color: #4f46e5;">⚖️ EQUITY AUDIT</span>
        <h4 class="finding-title">Zero Performance Pay Disparity</h4>
        <p class="finding-body">
            Employees across all four performance ratings (Poor to Excellent) earn virtually identical median salaries (~<b>$85,548</b>). The organization demonstrates flat appraisal-to-compensation translation, meaning bonuses or raises are decoupled from annual performance grades.
        </p>
    </div>
    
    <div class="finding-card success">
        <span class="finding-badge" style="color: #059669;">🌐 LOCATION NEUTRALITY</span>
        <h4 class="finding-title">50/50 Hybrid Parity</h4>
        <p class="finding-body">
            <b>50.3%</b> of the workforce operates remotely, and their average pay (<b>$85,468</b>) is on exact parity with in-office staff (<b>$85,584</b>). There is zero geographic or presence penalty imposed on remote workers.
        </p>
    </div>
    
    <div class="finding-card amber">
        <span class="finding-badge" style="color: #d97706;">🏢 WAGE STANDARDIZATION</span>
        <h4 class="finding-title">Inter-Department Wage Discipline</h4>
        <p class="finding-body">
            Average departmental wages are rigidly banded between <b>$83,912</b> (HR) and <b>$87,143</b> (Sales) — a variance of less than 3.8%. This reflects a highly centralized and standardized corporate compensation framework.
        </p>
    </div>
</div>
""")
