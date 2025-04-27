import pandas as pd

df = pd.read_csv("project_heart_disease.csv")

total_rows = len(df)

null_counts = df.isnull().sum()

missing_counts = df.applymap(lambda x: isinstance(x, str) and x.strip() == "").sum()

actual_counts = total_rows - (null_counts + missing_counts)

cardinality_counts = df.nunique(dropna=True)

completeness = (actual_counts / total_rows) * 100

uniqueness = (cardinality_counts / total_rows) * 100

distinctness = (cardinality_counts / actual_counts.replace(0, 1)) * 100  # Avoid division by zero

data_quality_summary = pd.DataFrame({
    "Field Name": df.columns,   
    "Total Rows": [total_rows] * len(df.columns),
    "Null Count": null_counts.values,
    "Missing Count": missing_counts.values,
    "Actual Count": actual_counts.values,
    "Completeness (%)": completeness.values,
    "Cardinality": cardinality_counts.values,
    "Uniqueness (%)": uniqueness.values,
    "Distinctness (%)": distinctness.values
})

data_quality_summary.reset_index(drop=True, inplace=True)

pd.set_option('display.max_rows', None) 
pd.set_option('display.max_columns', None) 
pd.set_option('display.width', None)  
pd.set_option('display.max_colwidth', None) 

print(data_quality_summary)