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

# Function to convert values in parentheses to negative numbers
def convert_parentheses(val):
    if isinstance(val, str):
        if val.startswith('(') and val.endswith(')'):
            return -float(val[1:-1].replace(',', ''))
        else:
            return float(val)
    else:
        return val

# List of columns to clean
columns_to_clean = ['Units Sold', 'Manufacturing Price', 'Sale Price', 'Gross Sales', 'Discounts', 'Sales', 'COGS', 'Profit']

# Remove '$', '-' and ',' from the columns, convert values in parentheses to negative numbers, convert empty strings to NaN, and then convert to float
for col in columns_to_clean:
    if df[col].dtype == 'object':
        df[col] = df[col].str.replace('$', '').str.replace('-', '').str.replace(',', '').str.strip()
        df[col] = df[col].replace('', np.nan).apply(convert_parentheses).astype(float)

# Convert 'Date' column to datetime format
df['Date'] = pd.to_datetime(df['Date'])

# Display the cleaned data
print(df.head())

# Group data by Date
grouped_df = df.groupby('Date').agg({'Sales': 'sum', 'Profit': 'sum'})

# Plot Sales and Profit over time
plt.figure(figsize=(14, 7))
plt.plot(grouped_df.index, grouped_df['Sales'], label='Sales')
plt.plot(grouped_df.index, grouped_df['Profit'], label='Profit')
plt.title('Sales and Profit over Time')
plt.xlabel('Date')
plt.ylabel('Amount')
plt.legend()
plt.grid()
plt.show()

# Group data by Segment
grouped_segment = df.groupby('Segment').agg({'Sales': 'sum', 'Profit': 'sum'})

# Plot Sales and Profit by Segment
fig, ax = plt.subplots(2, 1, figsize=(12, 12))

ax[0].bar(grouped_segment.index, grouped_segment['Sales'], color='blue', alpha=0.7)
ax[0].set_title('Sales by Segment')
ax[0].set_xlabel('Segment')
ax[0].set_ylabel('Sales')
ax[0].grid()

ax[1].bar(grouped_segment.index, grouped_segment['Profit'], color='green', alpha=0.7)
ax[1].set_title('Profit by Segment')
ax[1].set_xlabel('Segment')
ax[1].set_ylabel('Profit')
ax[1].grid()

plt.tight_layout()
plt.show()

# Group data by Country
grouped_country = df.groupby('Country').agg({'Sales': 'sum', 'Profit': 'sum'})

# Sort data by Sales
grouped_country = grouped_country.sort_values(by='Sales', ascending=False)

# Plot Sales and Profit by Country
fig, ax = plt.subplots(2, 1, figsize=(14, 14))

ax[0].bar(grouped_country.index, grouped_country['Sales'], color='blue', alpha=0.7)
ax[0].set_title('Sales by Country')
ax[0].set_xlabel('Country')
ax[0].set_ylabel('Sales')
ax[0].tick_params(axis='x', rotation=90)
ax[0].grid()

ax[1].bar(grouped_country.index, grouped_country['Profit'], color='green', alpha=0.7)
ax[1].set_title('Profit by Country')
ax[1].set_xlabel('Country')
ax[1].set_ylabel('Profit')
ax[1].tick_params(axis='x', rotation=90)
ax[1].grid()

plt.tight_layout()
plt.show()

# Summary statistics for 'Discounts'
print(df['Discounts'].describe())

# Create a scatter plot of 'Discounts' vs 'Profit'
plt.figure(figsize=(12, 7))
plt.scatter(df['Discounts'], df['Profit'], alpha=0.5)
plt.title('Discounts vs Profit')
plt.xlabel('Discounts')
plt.ylabel('Profit')
plt.grid()
plt.show()

# Group data by Product
grouped_product = df.groupby('Product').agg({'Sales': 'sum', 'Profit': 'sum'})

# Sort data by Sales
grouped_product = grouped_product.sort_values(by='Sales', ascending=False)

# Plot Sales and Profit by Product
fig, ax = plt.subplots(2, 1, figsize=(14, 14))

ax[0].bar(grouped_product.index, grouped_product['Sales'], color='blue', alpha=0.7)
ax[0].set_title('Sales by Product')
ax[0].set_xlabel('Product')
ax[0].set_ylabel('Sales')
ax[0].tick_params(axis='x', rotation=90)
ax[0].grid()

ax[1].bar(grouped_product.index, grouped_product['Profit'], color='green', alpha=0.7)
ax[1].set_title('Profit by Product')
ax[1].set_xlabel('Product')
ax[1].set_ylabel('Profit')
ax[1].tick_params(axis='x', rotation=90)
ax[1].grid()

plt.tight_layout()
plt.show()

# Group data by Discount Band
grouped_discount = df.groupby('Discount Band').agg({'Sales': 'sum'})

# Sort data by Sales
grouped_discount = grouped_discount.sort_values(by='Sales', ascending=False)

# Plot Sales by Discount Band
plt.figure(figsize=(10, 6))
plt.bar(grouped_discount.index, grouped_discount['Sales'], color='purple', alpha=0.7)
plt.title('Sales by Discount Band')
plt.xlabel('Discount Band')
plt.ylabel('Sales')
plt.grid()
plt.show()

# Calculate correlation
correlation = df[['Manufacturing Price', 'Sale Price', 'Sales', 'Profit']].corr()

# Plot heatmap of correlation
plt.figure(figsize=(10, 8))
sns.heatmap(correlation, annot=True, cmap='coolwarm', center=0)
plt.title('Correlation Heatmap')
plt.show()

# Create a new dataframe with total monthly sales and profit
monthly_data = df.groupby([df['Date'].dt.year, df['Date'].dt.month]).agg({'Sales': 'sum', 'Profit': 'sum'})
monthly_data.index.names = ['Year', 'Month']
monthly_data.reset_index(inplace=True)

# Create a 'Year-Month' column for easier plotting
monthly_data['Year-Month'] = pd.to_datetime(monthly_data[['Year', 'Month']].assign(day=1))

# Plot monthly sales and profit
plt.figure(figsize=(14, 7))
plt.plot(monthly_data['Year-Month'], monthly_data['Sales'], label='Sales')
plt.plot(monthly_data['Year-Month'], monthly_data['Profit'], label='Profit')
plt.title('Monthly Sales and Profit')
plt.xlabel('Date')
plt.ylabel('Amount')
plt.legend()
plt.grid()
plt.show()

# Create a cross-tabulation of 'Product' and 'Segment'
product_segment_crosstab = pd.crosstab(df['Product'], df['Segment'])

# Plot a heatmap of the cross-tabulation
plt.figure(figsize=(10, 8))
sns.heatmap(product_segment_crosstab, annot=True, fmt='d', cmap='viridis')
plt.title('Product Distribution across Market Segments')
plt.show()

# Calculate average 'Manufacturing Price' and 'Sale Price' for each product
average_prices = df.groupby('Product').agg({'Manufacturing Price': 'mean', 'Sale Price': 'mean'})

# Create a scatter plot of 'Manufacturing Price' vs 'Sale Price'
plt.figure(figsize=(10, 8))
for i, product in enumerate(average_prices.index):
    plt.scatter(average_prices['Manufacturing Price'][i], average_prices['Sale Price'][i], label=product)
plt.title('Manufacturing Price vs Sale Price')
plt.xlabel('Manufacturing Price')
plt.ylabel('Sale Price')
plt.legend()
plt.grid()
plt.show()

# Calculate total 'Units Sold' for each product
product_units_sold = df.groupby('Product').agg({'Units Sold': 'sum'})

# Sort data by 'Units Sold'
product_units_sold = product_units_sold.sort_values(by='Units Sold', ascending=False)

# Plot 'Units Sold' by Product
plt.figure(figsize=(10, 8))
plt.bar(product_units_sold.index, product_units_sold['Units Sold'], color='purple', alpha=0.7)
plt.title('Units Sold by Product')
plt.xlabel('Product')
plt.ylabel('Units Sold')
plt.xticks(rotation=90)
plt.grid()
plt.show()

# Create a cross-tabulation of 'Segment' and 'Country' with 'Sales' as values
segment_country_sales = df.pivot_table(values='Sales', index='Segment', columns='Country', aggfunc='sum')

# Plot a heatmap of the cross-tabulation
plt.figure(figsize=(12, 8))
sns.heatmap(segment_country_sales, annot=True, fmt='.0f', cmap='viridis')
plt.title('Sales across Market Segments and Countries')
plt.show()

# Create histograms for 'Sales' and 'Profit'
fig, ax = plt.subplots(2, 1, figsize=(12, 12))

ax[0].hist(df['Sales'], bins=30, color='blue', alpha=0.7)
ax[0].set_title('Distribution of Sales')
ax[0].set
