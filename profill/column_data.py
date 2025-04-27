import pandas as pd

file_path = "project_heart_disease.csv"
df = pd.read_csv(file_path)

column_name = "BMI"  
column_data = df[column_name]

field_name = column_name
field_data_type = column_data.dtype  

missing_count = column_data.apply(lambda x: isinstance(x, str) and x.strip() == "").sum()

null_count = column_data.isnull().sum()

valid_data = column_data.replace("", pd.NA).dropna().astype(str)
field_length_min = valid_data.apply(len).min() if not valid_data.empty else "N/A"
field_length_max = valid_data.apply(len).max() if not valid_data.empty else "N/A"

total_values = len(column_data)
actual_count = total_values - (null_count + missing_count)
completeness = (actual_count / total_values) * 100 if total_values > 0 else 0

cardinality = valid_data.nunique()
uniqueness = (cardinality / total_values) * 100 if total_values > 0 else 0
distinctness = (cardinality / actual_count) * 100 if actual_count > 0 else 0

# Field Data Types (counts distinct types)
field_data_types = valid_data.apply(lambda x: type(x).__name__).nunique()
numeric_column = pd.to_numeric(valid_data, errors='coerce')
field_value_min = numeric_column.min(skipna=True) if numeric_column.notna().any() else "N/A"
field_value_max = numeric_column.max(skipna=True) if numeric_column.notna().any() else "N/A"

def get_format_pattern(value):
    return ''.join(['n' if c.isdigit() else 'a' for c in str(value)])

field_format_patterns = valid_data.apply(get_format_pattern)
field_format_counts = field_format_patterns.value_counts().reset_index()
field_format_counts.columns = ["Format Pattern", "Count"]
field_format_counts["Percentage"] = (field_format_counts["Count"] / actual_count) * 100

top_values = valid_data.value_counts().head(5).reset_index()
top_values.columns = ["Value", "Count"]
top_values["Percentage"] = (top_values["Count"] / actual_count) * 100

metadata_df = pd.DataFrame([{
    "Field Name": field_name,
    "Field Data Type": str(field_data_type)
}])

summary_df = pd.DataFrame([{
    "Total Values": total_values,
    "Null Count": null_count,  # True null values (NaN)
    "Missing Count": missing_count,  # Empty or whitespace values
    "Actual Count": actual_count,
    "Completeness (%)": completeness,
    "Cardinality (Excluding Missing & Null)": cardinality,
    "Uniqueness (%)": uniqueness,
    "Distinctness (%)": distinctness
}])

additional_stats_df = pd.DataFrame([{
    "Field Data Types": field_data_types,
    "Field Length (MIN)": field_length_min,
    "Field Length (MAX)": field_length_max,
    "Field Value (MIN)": field_value_min,
    "Field Value (MAX)": field_value_max,
}])

pd.set_option("display.max_rows", None)  
pd.set_option("display.max_columns", None) 
pd.set_option("display.width", 1000)  
pd.set_option("display.max_colwidth", None) 

# Print results
print("Input Metadata:")
print(metadata_df.to_string())

print("\nData Profiling Summary Statistics:")
print(summary_df.to_string())

print("\nData Profiling Additional Statistics:")
print(additional_stats_df.to_string())

print("\nTop 5 Values:")
print(top_values.to_string())

print("\nField Format:")
print(field_format_counts.to_string())
