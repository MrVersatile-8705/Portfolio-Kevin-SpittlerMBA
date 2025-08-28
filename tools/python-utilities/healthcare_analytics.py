"""
Healthcare Data Analysis Utilities
A collection of reusable functions for healthcare analytics projects.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

def load_and_clean_data(file_path, date_columns=None):
    """
    Load healthcare data and perform basic cleaning.
    
    Parameters:
    file_path (str): Path to the data file
    date_columns (list): List of column names to convert to datetime
    
    Returns:
    pd.DataFrame: Cleaned dataset
    """
    # Load data
    if file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
    elif file_path.endswith('.xlsx'):
        df = pd.read_excel(file_path)
    else:
        raise ValueError("Unsupported file format")
    
    # Convert date columns
    if date_columns:
        for col in date_columns:
            df[col] = pd.to_datetime(df[col])
    
    # Basic cleaning
    df = df.drop_duplicates()
    
    print(f"Data loaded successfully: {df.shape[0]} rows, {df.shape[1]} columns")
    return df

def calculate_readmission_rate(df, patient_id_col='patient_id', 
                              admission_date_col='admission_date',
                              days_threshold=30):
    """
    Calculate 30-day readmission rates.
    
    Parameters:
    df (pd.DataFrame): Patient data
    patient_id_col (str): Patient ID column name
    admission_date_col (str): Admission date column name
    days_threshold (int): Days for readmission calculation
    
    Returns:
    float: Readmission rate as percentage
    """
    df_sorted = df.sort_values([patient_id_col, admission_date_col])
    df_sorted['next_admission'] = df_sorted.groupby(patient_id_col)[admission_date_col].shift(-1)
    df_sorted['days_to_next'] = (df_sorted['next_admission'] - df_sorted[admission_date_col]).dt.days
    
    readmissions = df_sorted[df_sorted['days_to_next'] <= days_threshold]
    readmission_rate = (len(readmissions) / len(df_sorted)) * 100
    
    return round(readmission_rate, 2)

def create_age_groups(age_series):
    """
    Create standard age groups for healthcare analysis.
    
    Parameters:
    age_series (pd.Series): Series containing age values
    
    Returns:
    pd.Series: Age groups
    """
    return pd.cut(age_series, 
                  bins=[0, 18, 35, 50, 65, 100], 
                  labels=['<18', '18-34', '35-49', '50-64', '65+'])

def plot_patient_flow(df, date_col='admission_date', title='Patient Flow Over Time'):
    """
    Create a patient flow visualization.
    
    Parameters:
    df (pd.DataFrame): Patient data
    date_col (str): Date column name
    title (str): Plot title
    """
    plt.figure(figsize=(12, 6))
    
    # Daily admissions
    daily_admissions = df.groupby(df[date_col].dt.date).size()
    
    plt.plot(daily_admissions.index, daily_admissions.values, linewidth=2)
    plt.title(title)
    plt.xlabel('Date')
    plt.ylabel('Number of Admissions')
    plt.xticks(rotation=45)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

def generate_summary_stats(df, numeric_columns=None):
    """
    Generate summary statistics for healthcare data.
    
    Parameters:
    df (pd.DataFrame): Dataset
    numeric_columns (list): Specific numeric columns to analyze
    
    Returns:
    pd.DataFrame: Summary statistics
    """
    if numeric_columns is None:
        numeric_columns = df.select_dtypes(include=[np.number]).columns
    
    summary = df[numeric_columns].describe()
    
    # Add additional healthcare-specific metrics
    summary.loc['missing_count'] = df[numeric_columns].isnull().sum()
    summary.loc['missing_percentage'] = (df[numeric_columns].isnull().sum() / len(df)) * 100
    
    return summary.round(2)

def calculate_length_of_stay(df, admit_col='admission_date', discharge_col='discharge_date'):
    """
    Calculate length of stay in days.
    
    Parameters:
    df (pd.DataFrame): Patient data
    admit_col (str): Admission date column
    discharge_col (str): Discharge date column
    
    Returns:
    pd.Series: Length of stay in days
    """
    return (df[discharge_col] - df[admit_col]).dt.days

# Example usage and testing
if __name__ == "__main__":
    print("Healthcare Analytics Utilities")
    print("Available functions:")
    print("- load_and_clean_data()")
    print("- calculate_readmission_rate()")
    print("- create_age_groups()")
    print("- plot_patient_flow()")
    print("- generate_summary_stats()")
    print("- calculate_length_of_stay()")
