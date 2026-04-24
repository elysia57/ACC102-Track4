# ACC102 Track 4: Interactive Financial Analysis Tool
# Data Source: WRDS Compustat
# Analysis Period: 2020 - 2024
# Companies: Apple (AAPL) vs Microsoft (MSFT)

import streamlit as st
import pandas as pd
import wrds

# Page configuration
st.set_page_config(page_title="AAPL vs MSFT 2020-2024", layout="wide")
st.title("Apple vs Microsoft Financial Analysis (2020–2024)")
st.subheader("ACC102 Track 4 | WRDS Data Product")

# Sidebar for user input
st.sidebar.header("User Input")
st.sidebar.info("Fixed: AAPL, MSFT | Period: 2020–2024")

wrds_username = st.sidebar.text_input("WRDS Username")
wrds_password = st.sidebar.text_input("WRDS Password", type="password")

# Run analysis button
if st.sidebar.button("Run Analysis"):
    # Validate input
    if not wrds_username or not wrds_password:
        st.error("Please enter your WRDS credentials.")
        st.stop()

    with st.spinner("Connecting to WRDS..."):
        try:
            # Connect to WRDS database
            conn = wrds.Connection(wrds_username=wrds_username, wrds_password=wrds_password)
        except Exception as e:
            st.error(f"Connection failed: {str(e)}")
            st.stop()

    # SQL query to get data from Compustat
    query = """
        SELECT tic, fyear, ni, sale, ceq
        FROM comp.funda
        WHERE tic IN ('AAPL', 'MSFT')
        AND fyear BETWEEN 2020 AND 2024
        AND indfmt = 'INDL'
        AND datafmt = 'STD'
        AND consol = 'C'
        ORDER BY tic, fyear;
    """

    # Retrieve data
    df = conn.raw_sql(query)
    conn.close()

    # Check if data exists
    if df.empty:
        st.warning("No data retrieved. Please check credentials or data availability.")
        st.stop()

    # Calculate financial ratios
    df["ROE"] = df["ni"] / df["ceq"]
    df["Profit_Margin"] = df["ni"] / df["sale"]
    df = df.round(4)

    # Display cleaned data
    st.subheader("Cleaned Financial Data")
    st.dataframe(df)

    # Plot ROE trend
    st.subheader("ROE Trend (2020–2024)")
    for ticker in ["AAPL", "MSFT"]:
        company_data = df[df["tic"] == ticker]
        st.line_chart(company_data, x="fyear", y="ROE")

    # Plot profit margin comparison
    st.subheader("Profit Margin Comparison")
    st.bar_chart(df, x="tic", y="Profit_Margin")

    # Download data as CSV
    csv_data = df.to_csv(index=False).encode("utf-8")
    st.download_button("Download CSV", csv_data, "aapl_msft_2020_2024.csv", "text/csv")