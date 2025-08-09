import pandas as pd

# 🔹 Load the full dataset
df = pd.read_csv("new_output.csv")  # Replace with your actual dataset path

# 🔹 Extract first 9 rows from the first column
test_logs_df = df.iloc[:9, [0]]  # [0] selects only the first column

# 🔹 Rename the column for clarity
test_logs_df.columns = ["log_input"]

# 🔹 Save to CSV
test_logs_df.to_csv("test_logs.csv", index=False)

print("✅ test_logs.csv has been created with the first 9 Sysmon logs.")