
import streamlit as st
import pandas as pd
import sqlite3
import os

st.set_page_config(page_title="Keysight 6G EDA Prospects", layout="wide")
st.title("📡 Keysight 6G/Wireless EDA Sales Dashboard")

# Load data
conn = sqlite3.connect("keysight_6g_eda_prospects_enhanced.db")
df = pd.read_sql_query("SELECT * FROM eda_6g_prospects", conn)

# Filters
with st.sidebar:
    st.header("🔍 Filter Prospects")
    company = st.multiselect("Company", df["company"].unique())
    location = st.multiselect("Location", df["location"].unique())
    keyword = st.text_input("Keyword in Insight")

filtered_df = df.copy()
if company:
    filtered_df = filtered_df[filtered_df["company"].isin(company)]
if location:
    filtered_df = filtered_df[filtered_df["location"].isin(location)]
if keyword:
    filtered_df = filtered_df[filtered_df["early_targeting_insight"].str.contains(keyword, case=False)]

# Display
st.dataframe(filtered_df[["priority_rank", "company", "location", "eda_fit", "early_targeting_insight"]], use_container_width=True)

# Battlecard Download
st.subheader("📄 View Battlecards")
for i, row in filtered_df.iterrows():
    with st.expander(f"{row['company']} - {row['eda_fit']}"):
        st.markdown(f"**Contact:** {row['sales_contact_name']} ({row['sales_contact_email']})")
        st.markdown(f"**Insight:** {row['early_targeting_insight']}")
        file_path = f"battlecards/{row['company'].replace('/', '_')}_battlecard.txt"
        if os.path.exists(file_path):
            with open(file_path, "rb") as f:
                st.download_button(
                    label="📥 Download Battlecard",
                    data=f,
                    file_name=os.path.basename(file_path),
                    mime="text/plain"
                )
