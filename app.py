# ACC102 Track 4: Apple vs Microsoft Financial Analysis (2020-2024)
# No WRDS required
# Data source: Public financial statements

import streamlit as st
import pandas as pd

# Page setup
st.set_page_config(page_title="AAPL vs MSFT", layout="wide")
st.title("Apple vs Microsoft Financial Analysis (2020–2024)")
st.subheader("ACC102 Track 4 | Interactive Data Product")

# Remove the WRDS login section entirely
st.info("This tool uses preloaded public financial data. No WRDS credentials needed.")

# Preloaded data (AAPL & MSFT 2020-2024 key figures)
data = {
    "tic": ["AAPL","AAPL","AAPL","AAPL","AAPL",
            "MSFT","MSFT","MSFT","MSFT","MSFT"],
    "fyear": [2020,2021,2022,2023,2024,
              2020,2021,2022,2023,2024],
    "ni": [57413,94680,99803,96995,112238,
           44281,72738,72361,78032,88136],
    "sale": [274515,365817,394328,383285,381652,
             143015,168088,198270,211915,245123],
    "ceq": [65337,71932,50672,62122,73860,
            119462,141988,166542,205678,234686]
}

df = pd.DataFrame(data)

# Calculate financial ratios
df["ROE"] = df["ni"] / df["ceq"]
df["Profit_Margin"] = df["ni"] / df["sale"]
df = df.round(4)

# Show data
st.subheader("Financial Data (2020–2024)")
st.dataframe(df)

# Show charts
st.subheader("ROE Trend Comparison")
for ticker in ["AAPL", "MSFT"]:
    sub = df[df["tic"] == ticker]
    st.line_chart(sub, x="fyear", y="ROE")

st.subheader("Profit Margin Comparison")
st.bar_chart(df, x="tic", y="Profit_Margin")

# Download button
csv = df.to_csv(index=False).encode()
st.download_button("Download CSV", csv, "aapl_msft_2020_2024.csv")