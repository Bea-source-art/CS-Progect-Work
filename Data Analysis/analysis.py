import pandas as pd
import matplotlib.pyplot as plt

print("==================================================")
print("       EXPLORATORY DATA ANALYSIS (TASK 1.2)      ")
print("==================================================")

# 1. Load Datasets
try:
    lines = pd.read_csv('lines.csv')
    substations = pd.read_csv('substations.csv')
    utilities = pd.read_csv('utilities.csv')
    print("✓ Data successfully loaded!\n")
except Exception as e:
    print(f"❌ Error loading files: {e}")

# --- 1. NUMERICAL DESCRIPTIVE STATISTICS ---
print("--- 1. NUMERICAL DESCRIPTIVE STATISTICS ---")
print("\n[Substations Numerical Summary]")
print(substations[['Voltage (kV)', 'Capacity (MVA)', 'Commissioning Year', 'Latitude', 'Longitude']].describe())

print("\n[Lines Numerical Summary]")
print(lines[['Voltage (kV)', 'Length (km)', 'Capacity (MVA)']].describe())

# --- 2. CATEGORICAL FREQUENCY DISTRIBUTIONS ---
print("\n--- 2. CATEGORICAL FREQUENCY DISTRIBUTIONS ---")
print("\n[Substation Status Distribution]")
print(substations['Status'].value_counts(dropna=False))

print("\n[Substation Voltage Levels]")
print(substations['Voltage (kV)'].value_counts(dropna=False))

print("\n[Line Types]")
print(lines['Line Type'].value_counts(dropna=False))

# --- 3. Top Utilities by Number of Lines Operated ---
merged_lines_utility = lines.merge(utilities, on='Utility ID', how='left', suffixes=('', '_utility'))
utility_name_col = 'Name_utility' if 'Name_utility' in merged_lines_utility.columns else 'Utility ID'

plt.figure(figsize=(10, 5))
merged_lines_utility[utility_name_col].value_counts().plot(kind='bar', color='#1f77b4')
plt.title('Top Utilities by Number of Lines Operated', fontsize=12, fontweight='bold')
plt.xlabel('Utility Name')
plt.ylabel('Number of Lines')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('top_utilities.png')
plt.close()
print("✓ Saved chart: top_utilities.png")

# --- 4. Most-Connected Substations by Number of Lines ---
source_subs = lines['Source Substation'].dropna()
dest_subs = lines['Destination Substation'].dropna()
all_connections = pd.concat([source_subs, dest_subs])

plt.figure(figsize=(10, 5))
all_connections.value_counts().head(10).plot(kind='bar', color='#ff7f0e')
plt.title('Top 10 Most-Connected Substations', fontsize=12, fontweight='bold')
plt.xlabel('Substation Name')
plt.ylabel('Total Connected Lines')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('most_connected_substations.png')
plt.close()
print("✓ Saved chart: most_connected_substations.png")

# --- 5. Substation Status & Voltage Distribution ---
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

substations['Status'].value_counts().plot(kind='bar', ax=axes[0], color='#2ca02c')
axes[0].set_title('Substation Status Distribution', fontweight='bold')
axes[0].set_xlabel('Status')
axes[0].set_ylabel('Count')

substations['Voltage (kV)'].value_counts().sort_index().plot(kind='bar', ax=axes[1], color='#9467bd')
axes[1].set_title('Substation Voltage Level Distribution', fontweight='bold')
axes[1].set_xlabel('Voltage (kV)')
axes[1].set_ylabel('Count')

plt.tight_layout()
plt.savefig('substation_status_voltage.png')
plt.close()
print("✓ Saved chart: substation_status_voltage.png")

# --- 6. Geographic Distribution by Region ---
sub_region_map = substations.set_index('Substation ID')['Region'].to_dict()
lines['Region'] = lines['Source Substation ID'].map(sub_region_map)

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

substations['Region'].value_counts().plot(kind='bar', ax=axes[0], color='#17becf')
axes[0].set_title('Substations by Region', fontweight='bold')
axes[0].set_xlabel('Region')
axes[0].set_ylabel('Count')
axes[0].tick_params(axis='x', rotation=90)

lines['Region'].value_counts().plot(kind='bar', ax=axes[1], color='#e377c2')
axes[1].set_title('Lines by Region (by Source Substation)', fontweight='bold')
axes[1].set_xlabel('Region')
axes[1].set_ylabel('Count')
axes[1].tick_params(axis='x', rotation=90)

plt.tight_layout()
plt.savefig('geographic_distribution.png')
plt.close()
print("✓ Saved chart: geographic_distribution.png")

print("\n==================================================")
print("      EDA COMPLETED! ALL CHARTS GENERATED.        ")
print("==================================================")