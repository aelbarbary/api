import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import boto3
from io import StringIO

# Load the CSV data
s3 = boto3.client('s3')

# Specify your bucket name and file key
bucket_name = 'ceo-ign'
file_key = 'Financials.csv'

# Download the file object from S3
s3_object = s3.get_object(Bucket=bucket_name, Key=file_key)

# Read the file content into a string buffer
file_content = s3_object['Body'].read().decode('utf-8')

df = pd.read_csv(StringIO(file_content))

# Remove leading and trailing spaces from column names
df.columns = df.columns.str.strip()

# Convert 'Sales' to numeric
df['Sales'] = df['Sales'].replace('[\$,]', '', regex=True).astype(float)

# Convert 'Date' to datetime
df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')

# Extract month and year from the Date
df['Month'] = df['Date'].dt.to_period('M')

# Aggregate total sales by month
monthly_sales = df.groupby('Month')['Sales'].sum().reset_index()

# Print total sales by month
print("Total Sales by Month:")
print(monthly_sales)

# Calculate historical benchmark (e.g., average monthly sales from historical data)
historical_monthly_sales = monthly_sales  # For example purposes, use the same data
historical_benchmark = historical_monthly_sales['Sales'].mean()

print(f"Historical Benchmark for Monthly Sales: ${historical_benchmark:.2f}")

# Compare current month sales to historical benchmark
monthly_sales['Benchmark'] = historical_benchmark
monthly_sales['Performance'] = monthly_sales['Sales'] > monthly_sales['Benchmark']

print("\nMonthly Sales Comparison:")
print(monthly_sales)