"""
=================================================
DISASTER MANAGEMENT SYSTEM - Dataset Generator
=================================================
Yeh file 1000 rows ka dataset banati hai.
"""

import pandas as pd
import numpy as np
import random

random.seed(42)
np.random.seed(42)

disasters = ['Flood', 'Earthquake', 'Fire', 'Cyclone', 'Landslide', 'Tsunami', 'Drought', 'Heatwave']
locations = ['Karachi', 'Lahore', 'Islamabad', 'Peshawar', 'Quetta', 'Multan', 'Faisalabad',
             'Rawalpindi', 'Hyderabad', 'Sialkot', 'Gujranwala', 'Sukkur']
severities = ['Low', 'Medium', 'High', 'Critical']
priorities = ['Low', 'Medium', 'High', 'Critical']

n = 1000

# Severity aur Priority ke basis pe realistic data
severity_multiplier = {'Low': 0.5, 'Medium': 1.0, 'High': 2.0, 'Critical': 4.0}
priority_order = {'Low': 0, 'Medium': 1, 'High': 2, 'Critical': 3}

disaster_list = [random.choice(disasters) for _ in range(n)]
severity_list = [random.choice(severities) for _ in range(n)]

people_affected = [
    int(random.randint(100, 10000) * severity_multiplier[s])
    for s in severity_list
]
ambulance_needed = [
    max(1, int(p / 500) + random.randint(0, 5))
    for p in people_affected
]
resources_needed = [
    max(10, int(p / 100) + random.randint(0, 50))
    for p in people_affected
]
response_time = [
    max(5, int(240 - severity_multiplier[s] * 20) + random.randint(-20, 20))
    for s in severity_list
]

# Priority logically assign karo
priority_list = []
for s, p in zip(severity_list, people_affected):
    if s == 'Critical' or p > 30000:
        priority_list.append('Critical')
    elif s == 'High' or p > 15000:
        priority_list.append('High')
    elif s == 'Medium' or p > 5000:
        priority_list.append('Medium')
    else:
        priority_list.append('Low')

data = {
    'Disaster': disaster_list,
    'Location': [random.choice(locations) for _ in range(n)],
    'Severity': severity_list,
    'People_Affected': people_affected,
    'Ambulance_Needed': ambulance_needed,
    'Resources_Needed': resources_needed,
    'Response_Time': response_time,
    'Priority': priority_list,
}

df = pd.DataFrame(data)
df.to_csv('disaster_dataset.csv', index=False)

print("=" * 50)
print("✅ Dataset Successfully Created!")
print("=" * 50)
print(f"📊 Total Rows: {len(df)}")
print(f"📋 Columns: {list(df.columns)}")
print(f"\n🔍 Missing Values:\n{df.isnull().sum()}")
print(f"\n🔄 Duplicates: {df.duplicated().sum()}")
print(f"\n📈 Data Types:\n{df.dtypes}")
print(f"\n📊 Sample Data:")
print(df.head(5))
