# EDA Dashboard (Streamlit)

A simple Streamlit app for exploratory data analysis (EDA) on any CSV file.

## Features
- Upload a CSV file and preview the first 5 rows
- See dataset shape, column data types, and missing values
- View basic statistics (mean, median, min, max) for numerical columns
- Pick any column and get an automatic histogram (numerical) or bar chart (categorical)

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

Then open the local URL shown in the terminal (usually `http://localhost:8501`).

## Test dataset
Tested using `titanic.csv`.