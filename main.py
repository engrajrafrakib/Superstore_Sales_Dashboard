import pandas as pd
import numpy as np

# External stylesheet used for icons.  
font_awesome = 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.2.1/css/all.min.css'
# Consider only 2 decimal points for all float values of dataframes.
pd.options.display.float_format = "{:,.2f}".format

# Source file path
source_file_path = "./dataset/Sample - Superstore.xlsx"

# Create a base/main dataframe to be used as a primary dataframe for any pages.

# Create dataframe with 'Orders' data by considering 'Orders' worksheet from the source file.
df_orders_data = pd.read_excel(source_file_path, sheet_name="Orders", usecols=lambda x: x not in ['Row ID', 'Customer ID', 'Country', 'Postal Code', 'Product ID'])
# Create dataframe with 'Returns' data by considering 'Returns' worksheet from the source file.
df_returns_data = pd.read_excel(source_file_path, sheet_name="Returns")
# Merge above dataframes based on 'Order ID' as this column is common between two dataframe.
df_main = pd.merge(df_orders_data, df_returns_data, on='Order ID', how='left')
# Fill missing entries of 'Returned' column with 'No'. Then assign numeric vlues: 1 for all Yes and 0 for all No values for later calculation. 
df_main['Returned'] = df_main['Returned'].fillna('No').map(dict(Yes=1, No=0))
# Add 'Days to Ship' column to keep the information of taken shipment days for individual order.
df_main['Days to Ship'] = (df_main['Ship Date'] - df_main['Order Date']).dt.days + 1
# Calculate and Add 'Profit Ratio' column to the dataframe.
df_main['Profit Ratio'] = df_main['Profit'] / df_main['Sales']
df_main = np.round(df_main, decimals=2).sort_values(by='Order Date')
# Create granularity columns. 
df_main['Year'], df_main['Month'], df_main['Quarter'], df_main['Week'] = df_main['Order Date'].dt.year, df_main['Order Date'].dt.month, df_main['Order Date'].dt.quarter, df_main['Order Date'].dt.isocalendar().week
