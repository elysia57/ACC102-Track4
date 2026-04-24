# ==========================================================
# ACC102 Track 4: Interactive Financial Analysis Dashboard
# Comparison: Apple vs Microsoft (2020–2024)
# Data Source: Public annual financial reports
# No WRDS required
# ==========================================================

import streamlit as st
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="AAPL vs MSFT Interactive Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Main title and introduction
st.title("Interactive Financial Analysis Dashboard: Apple vs Microsoft")
st.subheader("ACC102 Track 4 – Interactive Data Product")
st.markdown("""
This interactive application supports financial performance comparison between Apple and Microsoft 
using historical annual data from 2020 to 2024. Users may filter data, select metrics, and 
visualize trends through dynamic charts.
""")

# Dataset construction from public financial reports
data = {
    "tic": ["AAPL"] * 5 + ["MSFT"] * 5,
    "year": [2020, 2021, 2022, 2023, 2024] * 2,
    "revenue": [274515, 365817, 394328, 383285, 381652,
                143015, 168088, 198270, 211915, 245123],
    "net_income": [57413, 94680, 99803, 96995, 112238,
                   44281, 72738, 72361, 78032, 88136],
    "total_equity": [65337, 71932, 50672, 62122, 73860,
                     119462, 141988, 166542, 205678, 234686]
}

df = pd.DataFrame(data)

# Financial ratio calculation
df["ROE"] = df["net_income"] / df["total_equity"]
df["profit_margin"] = df["net_income"] / df["revenue"]

# Interactive control panel
st.sidebar.header("Control Panel")

# Selection for companies
selected_companies = st.sidebar.multiselect(
    "Select Companies",
    options=["AAPL", "MSFT"],
    default=["AAPL", "MSFT"]
)

# Slider for year range
year_min, year_max = st.sidebar.slider(
    "Select Year Range",
    min_value=2020,
    max_value=2024,
    value=(2020, 2024)
)

# Selection for financial metric
selected_metric = st.sidebar.selectbox(
    "Select Metric to Display",
    options=["ROE", "profit_margin", "revenue", "net_income"]
)

# Selection for chart type
chart_type = st.sidebar.radio(
    "Select Chart Type",
    options=["Line Chart", "Bar Chart"]
)

# Data filtering based on user inputs
filtered_df = df[
    (df["tic"].isin(selected_companies)) &
    (df["year"] >= year_min) &
    (df["year"] <= year_max)
]

# Display filtered data table
st.markdown("## Filtered Financial Data")
st.dataframe(filtered_df, use_container_width=True)

# Dynamic chart rendering
st.markdown("## Dynamic Visualization")
if chart_type == "Line Chart":
    fig = px.line(
        filtered_df,
        x="year",
        y=selected_metric,
        color="tic",
        markers=True
    )
else:
    fig = px.bar(
        filtered_df,
        x="year",
        y=selected_metric,
        color="tic",
        barmode="group"
    )
st.plotly_chart(fig, use_container_width=True)

# Interactive summary output
st.markdown("## Analysis Summary")
avg_value = filtered_df[selected_metric].mean()
st.markdown(f"""
- Companies selected: {', '.join(selected_companies)}
- Year range: {year_min} to {year_max}
- Displayed metric: {selected_metric}
- Chart type: {chart_type}
- Average value across period: {avg_value:.4f}
""")

# Data export function
st.markdown("## Export Data")
csv_data = filtered_df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="Download Filtered Data as CSV",
    data=csv_data,
    file_name="filtered_financial_data.csv",
    mime="text/csv"
)

# Footer note
st.markdown("---")
st.caption("ACC102 Track 4 | Interactive Data Product | All data from public financial reports")