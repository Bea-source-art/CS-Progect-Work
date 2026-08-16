import pandas as pd 
import numpy as np
  

# The generator script already writes proper headers, so we can read directly. 

utilities = pd.read_csv('utilities.csv') 

substations = pd.read_csv('substations.csv') 

lines = pd.read_csv('lines.csv') 

  

# Inspect the data 

print("Utilities DataFrame Info:") 

print(utilities.info(), "\n") 

print("Utilities First 5 Rows:") 

print(utilities.head(), "\n") 

  

print("Substations DataFrame Info:") 

print(substations.info(), "\n") 

print("Substations First 5 Rows:") 

print(substations.head(), "\n") 

  

print("Lines DataFrame Info:") 

print(lines.info(), "\n") 

print("Lines First 5 Rows:") 

print(lines.head(), "\n") 


# Check for missing values 

print("Missing Values in Utilities:") 

print(utilities.isnull().sum(), "\n") 

print("Missing Values in Substations:") 

print(substations.isnull().sum(), "\n") 

print("Missing Values in Lines:") 

print(lines.isnull().sum(), "\n") 

  

# Convert numeric columns to appropriate types 

substations['Latitude'] = pd.to_numeric(substations['Latitude'], errors='coerce') 

substations['Longitude'] = pd.to_numeric(substations['Longitude'], errors='coerce') 

substations['Capacity (MVA)'] = pd.to_numeric(substations['Capacity (MVA)'], errors='coerce') 

lines['Length (km)'] = pd.to_numeric(lines['Length (km)'], errors='coerce') 

  

# Check for duplicates 
print(utilities.shape)
print(utilities.to_string())
print("Duplicate Rows in Utilities:", utilities.duplicated().sum()) 

print("Duplicate Rows in Substations:", substations.duplicated().sum()) 

print("Duplicate Rows in Lines:", lines.duplicated().sum()) 

  

# Drop duplicates if any 

utilities = utilities.drop_duplicates() 

substations = substations.drop_duplicates() 

lines = lines.drop_duplicates() 

utilities.to_csv('utilities_cleaned.csv', index=False)

# Verify data types and missing values after cleaning 

print("\nAfter Cleaning - Substations Info:") 

print(substations.info(), "\n")

# Utilities 
#removes rows with missing values
utilities = utilities.dropna(subset=['Utility ID', 'Name'])
print(utilities)
#finds and replaces missing value with "Unknown"
utilities['Alias'] = utilities['Alias'].fillna('Unknown')
utilities['Code'] = utilities['Code'].fillna('Unknown')
utilities['Type'] = utilities['Type'].fillna(utilities['Type'].mode()[0])
utilities['Country'] = utilities['Country'].fillna(utilities['Country'].mode()[0])
utilities['Active'] = utilities['Active'].fillna('Unknown')
# uses single most common value to fill in any blank space 
utilities['Type'] = utilities['Type'].fillna(utilities['Type'].mode()[0])
utilities['Type'] = utilities['Country'].fillna(utilities['Country'].mode()[0])
# finds missing operational status and replaces it with "Unknown"
utilities['Active'] = utilities['Active'].fillna('Unknown')

# VERIFICATION 
print(utilities.isnull().sum(), "\n")

# SUBSTATIONS
#Drops rows missing the ID
substations = substations.dropna(subset=['Substation ID'])
# replaces missing capacity values with median
substations['Capacity (MVA)'] = substations['Capacity (MVA)'].fillna(
    substations['Capacity (MVA)'].median()
)


#LINES 
#deletes any row where Line ID, From Substation, or To Substation is missing
lines = lines.dropna(subset=['Line ID', 'From Substation', 'To Substation'])
#fills in missing lenghts with median
lines['Length (km)'] = lines['Length (km)'].fillna(lines['Length (km)'].median())
#uses a common voltage value to fill in any blanks 
lines['Voltage'] = lines['Voltage'].fillna(lines['Voltage'].mode()[0])