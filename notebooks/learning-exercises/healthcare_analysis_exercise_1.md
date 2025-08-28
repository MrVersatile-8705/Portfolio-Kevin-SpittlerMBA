# Healthcare Data Analysis - Learning Exercise #1

## Objective
Learn basic data manipulation and visualization techniques using Python for healthcare analytics.

## Learning Goals
- Practice pandas data manipulation
- Create meaningful visualizations
- Calculate healthcare KPIs
- Document analysis process

## Dataset
*To be determined - suggest using public healthcare datasets from:*
- CMS.gov
- Healthcare.gov
- Kaggle healthcare datasets
- Synthetic data generators

## Analysis Steps

### 1. Environment Setup
```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Set style for better looking plots
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")
```

### 2. Data Loading and Exploration
```python
# Load your dataset here
# df = pd.read_csv('path_to_your_data.csv')

# Basic data exploration
print("Dataset shape:", df.shape)
print("\nColumn names:")
print(df.columns.tolist())
print("\nData types:")
print(df.dtypes)
print("\nMissing values:")
print(df.isnull().sum())
```

### 3. Data Cleaning
```python
# Handle missing values
# Convert date columns
# Remove duplicates
# Create derived columns
```

### 4. Exploratory Data Analysis
```python
# Patient demographics
# Admission patterns
# Length of stay analysis
# Cost analysis
```

### 5. Key Performance Indicators
```python
# Calculate healthcare-specific metrics:
# - Average length of stay
# - Readmission rates
# - Patient satisfaction
# - Cost per case
```

### 6. Visualizations
```python
# Create meaningful charts:
# - Patient flow over time
# - Demographics breakdown
# - Department performance
# - Financial metrics
```

## Key Insights
*Document your findings here*

## Next Steps
*Plan for follow-up analysis or improvements*

## Skills Practiced
- [ ] Data loading and inspection
- [ ] Data cleaning and preprocessing
- [ ] Exploratory data analysis
- [ ] Healthcare KPI calculation
- [ ] Data visualization
- [ ] Insight generation
- [ ] Documentation

---
*Completion Date: ___________*  
*Time Invested: _____ hours*  
*Difficulty Level: Beginner/Intermediate/Advanced*
