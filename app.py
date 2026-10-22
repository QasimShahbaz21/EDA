import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import os

# --- Page Setup ---
st.set_page_config(
    page_title="Employee Workforce Dashboard",
    page_icon="💼",
    layout="wide"
)

# Custom Styling
st.markdown("""
    <style>
    .main {
        background-color: #f8fafc;
    }
    .metric-card {
        background-color: white;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    </style>
""", unsafe_allow_html=True)

# --- Data Loading & Preprocessing ---
@st.cache_data
def load_data():
    # Supports both local workspace and Streamlit Cloud repo structure
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
        st.error("Dataset not found. Please ensure 'data/Messy_Employee_dataset.csv' is present.")
        st.stop()
        
    df = pd.read_csv(file_path)

    # Impute missing values with median (as done in Lab 6)
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

# --- Title Header ---
st.title("💼 Employee Workforce & Compensation Dashboard")
st.caption("Interactive analysis of employee demographics, compensation, performance, and remote work trends.")

# --- Sidebar Filters ---
st.sidebar.header("🔍 Filter Employees")

# Filter 1: Department
all_departments = sorted(df['Department'].dropna().unique().tolist())
selected_departments = st.sidebar.multiselect(
    "Select Department(s):",
    options=all_departments,
    default=all_departments
)

# Filter 2: Remote Work
remote_options = ["All", "Remote Only", "In-Office Only"]
selected_remote = st.sidebar.radio("Remote Work Status:", remote_options)

# Filter 3: Performance Score
perf_order = ['Poor', 'Average', 'Good', 'Excellent']
selected_performance = st.sidebar.multiselect(
    "Select Performance Level:",
    options=perf_order,
    default=perf_order
)

# Apply Filters
filtered_df = df[df['Department'].isin(selected_departments)]
filtered_df = filtered_df[filtered_df['Performance_Score'].isin(selected_performance)]

if selected_remote == "Remote Only":
    filtered_df = filtered_df[filtered_df['Remote_Work'] == True]
elif selected_remote == "In-Office Only":
    filtered_df = filtered_df[filtered_df['Remote_Work'] == False]

# Safety check for empty filter result
if filtered_df.empty:
    st.warning("No employees match the selected filter criteria. Please broaden your filters in the sidebar.")
    st.stop()

# --- Key Metrics (st.metric) ---
st.markdown("### 📊 Key Workforce Numbers")
col1, col2, col3, col4 = st.columns(4)

total_emp = len(filtered_df)
avg_salary = filtered_df['Salary'].mean()
median_age = filtered_df['Age'].median()
remote_pct = (filtered_df['Remote_Work'].sum() / total_emp) * 100

col1.metric("Total Headcount", f"{total_emp:,} employees")
col2.metric("Average Salary", f"${avg_salary:,.2f}")
col3.metric("Median Age", f"{median_age:.0f} years")
col4.metric("Remote Employees", f"{remote_pct:.1f}%")

st.divider()

# --- Visualizations ---
st.markdown("### 📈 Visual Analysis")

tab1, tab2, tab3 = st.tabs([
    "1. Salary by Performance (Boxplot)",
    "2. Salary Spread (Histogram)",
    "3. Age vs Salary by Remote Work (Scatterplot)"
])

# --- Chart 1: Improved Boxplot ---
with tab1:
    st.subheader("Salary Distribution Across Performance Tiers")
    st.markdown("Shows whether performance ratings impact employee salary bands.")
    
    fig1, ax1 = plt.subplots(figsize=(8, 4.5))
    sns.boxplot(
        data=filtered_df,
        x='Performance_Score',
        y='Salary',
        order=[p for p in perf_order if p in filtered_df['Performance_Score'].unique()],
        palette='Blues',
        showmeans=True,
        meanprops={"marker": "D", "markeredgecolor": "black", "markerfacecolor": "gold", "markersize": "7"},
        ax=ax1
    )
    
    ax1.set_title("Employee Salary Distribution by Performance Rating", fontsize=13, fontweight='bold', pad=12)
    ax1.set_xlabel("Performance Rating", fontsize=11, fontweight='semibold')
    ax1.set_ylabel("Annual Salary ($)", fontsize=11, fontweight='semibold')
    ax1.yaxis.set_major_formatter(ticker.StrMethodFormatter('${x:,.0f}'))
    ax1.grid(axis='y', linestyle='--', alpha=0.5)
    
    st.pyplot(fig1)

# --- Chart 2: Histogram with KDE ---
with tab2:
    st.subheader("Workforce Salary Spread & Bell Curve")
    st.markdown("Displays the distribution of salaries across the selected workforce slice.")
    
    fig2, ax2 = plt.subplots(figsize=(8, 4.5))
    sns.histplot(
        filtered_df['Salary'],
        kde=True,
        color='#1d4ed8',
        bins=20,
        ax=ax2
    )
    
    ax2.set_title("Workforce Salary Distribution", fontsize=13, fontweight='bold', pad=12)
    ax2.set_xlabel("Annual Salary ($)", fontsize=11, fontweight='semibold')
    ax2.set_ylabel("Number of Employees", fontsize=11, fontweight='semibold')
    ax2.xaxis.set_major_formatter(ticker.StrMethodFormatter('${x:,.0f}'))
    ax2.grid(axis='y', linestyle='--', alpha=0.5)
    
    st.pyplot(fig2)

# --- Chart 3: Scatter Plot ---
with tab3:
    st.subheader("Age vs Salary Relationship (Colored by Remote Work)")
    st.markdown("Examines if older workers or remote workers enjoy higher compensation.")
    
    fig3, ax3 = plt.subplots(figsize=(8, 4.5))
    sns.scatterplot(
        data=filtered_df,
        x='Age',
        y='Salary',
        hue='Remote_Work',
        palette={True: '#2563eb', False: '#ef4444'},
        alpha=0.7,
        s=50,
        ax=ax3
    )
    
    ax3.set_title("Age vs Salary by Remote Work Status", fontsize=13, fontweight='bold', pad=12)
    ax3.set_xlabel("Age (Years)", fontsize=11, fontweight='semibold')
    ax3.set_ylabel("Annual Salary ($)", fontsize=11, fontweight='semibold')
    ax3.yaxis.set_major_formatter(ticker.StrMethodFormatter('${x:,.0f}'))
    ax3.legend(title="Remote Work", labels=["Remote (True)", "In-Office (False)"])
    ax3.grid(True, linestyle='--', alpha=0.4)
    
    st.pyplot(fig3)

# --- Findings Summary ---
st.divider()
st.markdown("### 💡 Key Data-Backed Findings")
st.markdown("""
1. **Performance Pay Equity:** Employees across all four performance ratings earn almost identical median salaries (~**$85,548**). Performance ratings do not dictate compensation tiers.
2. **Even Remote Split:** **50.3%** of employees work remotely, and their average pay (**$85,468**) is on par with in-office peers (**$85,584**).
3. **Department Pay Band:** Average salaries stay closely clustered between **$83,912** (HR) and **$87,143** (Sales), showing tight organizational wage standardization.
""")
