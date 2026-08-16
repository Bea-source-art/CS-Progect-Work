import os
import sys
import datetime
import pandas as pd
import matplotlib.pyplot as plt

# Automatically set working directory to the folder containing this script/CSV files
os.chdir(os.path.dirname(os.path.abspath(__file__)))

print("==================================================")
print("  TASK 2.3: BUSINESS INTELLIGENCE & RELIABILITY  ")
print("==================================================")

# 1. Load Data
try:
    lines = pd.read_csv('lines.csv')
    substations = pd.read_csv('substations.csv')
    utilities = pd.read_csv('utilities.csv')
    print("✓ Data successfully loaded!\n")
except FileNotFoundError as e:
    print(f"❌ Error loading files: {e}")
    print("Make sure lines.csv, substations.csv, and utilities.csv are in the same folder as this script!")
    sys.exit()

# --- 1. UTILITY FOOTPRINT ANALYSIS ---
merged_lines = lines.merge(utilities, on='Utility ID', how='left', suffixes=('', '_utility'))
util_name = 'Name_utility' if 'Name_utility' in merged_lines.columns else 'Utility ID'

print("\n--- 1. Utility Infrastructure Breakdown ---")
footprint = merged_lines.groupby([util_name, 'Voltage (kV)'])['Line ID'].count()
print(footprint)

# --- 2. ASSET AGE & RELIABILITY PROXIES ---
current_year = datetime.datetime.now().year
substations['Asset Age'] = current_year - substations['Commissioning Year']

print("\n--- 2. Asset Age Statistics ---")
print(substations[['Commissioning Year', 'Asset Age']].describe())

# Lines Under Maintenance / Status
print("\n--- 3. Line Status Breakdown ---")
print(lines['Status'].value_counts(dropna=False))

# Technical Loss Proxy = Length / Voltage
lines['Technical Loss Proxy'] = lines['Length (km)'] / lines['Voltage (kV)']

# --- 3. GENERATING VISUALIZATIONS ---

# Figure 1: Substation Age Distribution (Risk Indicator)
plt.figure(figsize=(10, 5))
substations['Asset Age'].plot(kind='hist', bins=10, color='#d62728', edgecolor='black')
plt.title('Substation Age Distribution (Older = Higher Risk Proxy)', fontweight='bold')
plt.xlabel('Age (Years)')
plt.ylabel('Count of Substations')
plt.tight_layout()
plt.savefig('asset_age_distribution.png')
plt.close()

# Figure 2: Top Technical Loss Risk Lines
plt.figure(figsize=(10, 5))
top_loss = lines.sort_values(by='Technical Loss Proxy', ascending=False).head(10)
plt.bar(top_loss['Line ID'].astype(str), top_loss['Technical Loss Proxy'], color='#ff7f0e')
plt.title('Top 10 Lines by Technical Loss Proxy (Length / Voltage)', fontweight='bold')
plt.xlabel('Line ID')
plt.ylabel('Loss Proxy Score')
plt.tight_layout()
plt.savefig('technical_loss_proxy.png')
plt.close()

# Figure 3: Capacity per Substation (Concentration Risk)
plt.figure(figsize=(10, 5))
substations.sort_values(by='Capacity (MVA)', ascending=False).head(10).plot(
    x='Name', y='Capacity (MVA)', kind='bar', color='#2ca02c', legend=False
)
plt.title('Top 10 Substations by Capacity (MVA)', fontweight='bold')
plt.xlabel('Substation')
plt.ylabel('Capacity (MVA)')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('substation_capacity_risk.png')
plt.close()

print("\n✓ All Task 2.3 analyses finished and charts saved successfully!")