# app.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Page Configuration

st.set_page_config(
    page_title="EDA Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Exploratory Data Analysis Interface")


# 2. Sidebar: Dataset Ingestion

st.sidebar.header("Dataset Controls")

# File uploader in the sidebar, restricted to CSV files only
uploaded_file = st.sidebar.file_uploader("Upload CSV File for Analysis", type=["csv"])

if uploaded_file is not None:

    # Read dataset, and make sure it is actually a valid, non-empty CSV
    try:
        df = pd.read_csv(uploaded_file)
    except Exception:
        st.error("This file could not be read. Please upload a valid CSV file.")
        st.stop()

    if df.empty:
        st.error("The uploaded CSV file has no data in it.")
        st.stop()

    # 3. Dataset Overview

    st.subheader("Dataset Preview & Metadata")

    st.write("**First 5 Rows:**")
    st.dataframe(df.head())

    # Shape of the dataset (rows, columns)
    st.write("**Shape:**", df.shape)

    st.write("**Column Data Types:**")
    st.dataframe(df.dtypes.astype(str).rename("Data Type"))

    # Missing value summary
    st.write("**Missing Values per Column:**")
    missing_count = df.isnull().sum()
    missing_percent = (missing_count / len(df) * 100).round(2)
    missing_summary = pd.DataFrame({
        "Missing Count": missing_count,
        "Missing %": missing_percent
    })
    st.dataframe(missing_summary)

    # Basic statistics for numerical columns
    st.write("**Basic Numerical Statistics:**")
    numeric_df = df.select_dtypes(include="number")

    if not numeric_df.empty:
        stats = numeric_df.describe().loc[["mean", "50%", "min", "max"]]
        stats = stats.rename(index={"50%": "median"})
        st.dataframe(stats)
    else:
        st.info("This dataset has no numerical columns.")


    # 4. Attribute Selection

    st.sidebar.header("Attribute Selection")

    # Dropdown to choose a single column for visualization
    selected_column = st.sidebar.selectbox("Select Attribute for Visualization", df.columns)

    # Detect column type: numerical or categorical
    if pd.api.types.is_numeric_dtype(df[selected_column]):
        column_type = "Numerical"
    else:
        column_type = "Categorical"


    # 5. Visualization Rendering

    st.subheader("Visualization")

    if column_type == "Numerical":
        # Histogram with seaborn
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.histplot(df[selected_column].dropna(), kde=True, color="skyblue", ax=ax)
        ax.set_title(f"Histogram of {selected_column}")
        ax.set_xlabel(selected_column)
        ax.set_ylabel("Frequency")
        st.pyplot(fig)

    else:
        # Bar chart for categorical columns, with frequency counts
        value_counts = df[selected_column].value_counts()
        percentages = (value_counts / value_counts.sum() * 100).round(1)

        fig, ax = plt.subplots(figsize=(8, 5))
        sns.barplot(x=value_counts.index.astype(str), y=value_counts.values, color="skyblue", ax=ax)
        ax.set_title(f"Bar Chart of {selected_column}")
        ax.set_xlabel(selected_column)
        ax.set_ylabel("Count")
        plt.xticks(rotation=45, ha="right")
        st.pyplot(fig)

        # Optional: show percentage breakdown alongside the chart
        st.write("**Percentage Breakdown:**")
        st.dataframe(percentages.rename("Percentage (%)"))

else:
    st.info("Please upload a CSV file to start EDA.")