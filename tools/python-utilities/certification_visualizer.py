"""
Certification Tracker Visualization - Python Approach
Creating professional charts for portfolio presentation
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import numpy as np

# Set up the visual style
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

def create_certification_data():
    """Create the certification tracker dataset"""
    data = {
        'Certification': [
            'Google Data Analytics Professional',
            'Microsoft Power BI Data Analyst Professional',
            'Azure Data Engineer Associate',
            'Python for Data Science',
            'Tableau Desktop Specialist',
            'dbt Fundamentals'
        ],
        'Platform': [
            'Coursera', 'Coursera', 'Microsoft Learn', 
            'Coursera', 'Tableau', 'dbt Labs'
        ],
        'Status': [
            'In Progress', 'In Progress', 'Planned',
            'Planned', 'Completed', 'Planned'
        ],
        'Target_Date': [
            '2025-03-01', '2025-10-01', '2025-05-01',
            '2025-04-01', '2021-01-01', '2025-11-01'
        ],
        'Progress_Percent': [75, 40, 0, 0, 100, 0],
        'Category': [
            'Analytics', 'Analytics', 'Engineering',
            'Programming', 'Visualization', 'Engineering'
        ]
    }
    
    df = pd.DataFrame(data)
    df['Target_Date'] = pd.to_datetime(df['Target_Date'])
    
    # Calculate days remaining
    today = datetime.now()
    df['Days_Remaining'] = (df['Target_Date'] - today).dt.days
    df['Days_Remaining'] = df['Days_Remaining'].apply(
        lambda x: 0 if x < 0 else x
    )
    
    return df

def create_progress_chart(df):
    """Create horizontal bar chart showing progress"""
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Create the horizontal bar chart
    bars = ax.barh(df['Certification'], df['Progress_Percent'])
    
    # Color bars based on progress
    colors = ['#d32f2f' if x < 33 else '#ff9800' if x < 67 else '#4caf50' 
              for x in df['Progress_Percent']]
    
    for bar, color in zip(bars, colors):
        bar.set_color(color)
    
    # Customize the chart
    ax.set_xlabel('Progress (%)')
    ax.set_title('Professional Certification Progress', fontsize=16, fontweight='bold')
    ax.set_xlim(0, 100)
    
    # Add progress labels on bars
    for i, (cert, progress) in enumerate(zip(df['Certification'], df['Progress_Percent'])):
        ax.text(progress + 2, i, f'{progress}%', 
                va='center', ha='left', fontweight='bold')
    
    plt.tight_layout()
    return fig

def create_timeline_chart(df):
    """Create timeline chart showing target completion dates"""
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Filter out completed certifications for timeline
    future_certs = df[df['Status'] != 'Completed'].copy()
    
    # Create timeline
    y_positions = range(len(future_certs))
    
    # Plot target dates
    ax.scatter(future_certs['Target_Date'], y_positions, 
               s=100, c='blue', alpha=0.7)
    
    # Add certification names
    for i, cert in enumerate(future_certs['Certification']):
        ax.text(future_certs['Target_Date'].iloc[i], i, 
                f'  {cert}', va='center', ha='left')
    
    # Customize
    ax.set_ylabel('Certifications')
    ax.set_xlabel('Target Completion Date')
    ax.set_title('Certification Timeline', fontsize=16, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig

def create_status_distribution(df):
    """Create pie chart showing status distribution"""
    fig, ax = plt.subplots(figsize=(8, 8))
    
    status_counts = df['Status'].value_counts()
    colors = ['#4caf50', '#ff9800', '#2196f3']  # Green, Orange, Blue
    
    wedges, texts, autotexts = ax.pie(status_counts.values, 
                                      labels=status_counts.index,
                                      autopct='%1.1f%%',
                                      colors=colors,
                                      startangle=90)
    
    ax.set_title('Certification Status Distribution', 
                 fontsize=16, fontweight='bold')
    
    return fig

def create_platform_analysis(df):
    """Create analysis by platform"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Platform distribution
    platform_counts = df['Platform'].value_counts()
    ax1.bar(platform_counts.index, platform_counts.values)
    ax1.set_title('Certifications by Platform')
    ax1.set_ylabel('Number of Certifications')
    plt.setp(ax1.get_xticklabels(), rotation=45)
    
    # Category distribution
    category_counts = df['Category'].value_counts()
    ax2.pie(category_counts.values, labels=category_counts.index, autopct='%1.1f%%')
    ax2.set_title('Certifications by Category')
    
    plt.tight_layout()
    return fig

def create_comprehensive_dashboard(df):
    """Create a comprehensive dashboard with multiple charts"""
    fig = plt.figure(figsize=(16, 12))
    
    # Create subplots
    gs = fig.add_gridspec(3, 2, height_ratios=[2, 1, 1])
    
    # Progress chart (top, full width)
    ax1 = fig.add_subplot(gs[0, :])
    bars = ax1.barh(df['Certification'], df['Progress_Percent'])
    colors = ['#d32f2f' if x < 33 else '#ff9800' if x < 67 else '#4caf50' 
              for x in df['Progress_Percent']]
    for bar, color in zip(bars, colors):
        bar.set_color(color)
    ax1.set_xlabel('Progress (%)')
    ax1.set_title('Professional Certification Dashboard - Kevin Spittler MBA', 
                  fontsize=16, fontweight='bold')
    
    # Status distribution (bottom left)
    ax2 = fig.add_subplot(gs[1, 0])
    status_counts = df['Status'].value_counts()
    ax2.pie(status_counts.values, labels=status_counts.index, autopct='%1.1f%%')
    ax2.set_title('Status Distribution')
    
    # Platform distribution (bottom right)
    ax3 = fig.add_subplot(gs[1, 1])
    platform_counts = df['Platform'].value_counts()
    ax3.bar(platform_counts.index, platform_counts.values)
    ax3.set_title('Platform Distribution')
    plt.setp(ax3.get_xticklabels(), rotation=45)
    
    # Summary statistics (bottom)
    ax4 = fig.add_subplot(gs[2, :])
    ax4.axis('off')
    
    # Calculate summary stats
    total_certs = len(df)
    completed = len(df[df['Status'] == 'Completed'])
    in_progress = len(df[df['Status'] == 'In Progress'])
    planned = len(df[df['Status'] == 'Planned'])
    avg_progress = df['Progress_Percent'].mean()
    
    summary_text = f"""
    Total Certifications: {total_certs}
    Completed: {completed} ({completed/total_certs*100:.1f}%)
    In Progress: {in_progress} ({in_progress/total_certs*100:.1f}%)
    Planned: {planned} ({planned/total_certs*100:.1f}%)
    Average Progress: {avg_progress:.1f}%
    
    Last Updated: {datetime.now().strftime('%B %Y')}
    """
    
    ax4.text(0.1, 0.5, summary_text, fontsize=12, 
             verticalalignment='center', fontfamily='monospace')
    
    plt.tight_layout()
    return fig

# Example usage
if __name__ == "__main__":
    # Create the dataset
    df = create_certification_data()
    
    # Generate all visualizations
    print("Creating certification tracker visualizations...")
    
    # Individual charts
    fig1 = create_progress_chart(df)
    fig1.savefig('certification_progress.png', dpi=300, bbox_inches='tight')
    
    fig2 = create_timeline_chart(df)
    fig2.savefig('certification_timeline.png', dpi=300, bbox_inches='tight')
    
    fig3 = create_status_distribution(df)
    fig3.savefig('certification_status.png', dpi=300, bbox_inches='tight')
    
    fig4 = create_platform_analysis(df)
    fig4.savefig('certification_platforms.png', dpi=300, bbox_inches='tight')
    
    # Comprehensive dashboard
    fig5 = create_comprehensive_dashboard(df)
    fig5.savefig('certification_dashboard.png', dpi=300, bbox_inches='tight')
    
    print("Visualizations saved successfully!")
    print("Files created:")
    print("- certification_progress.png")
    print("- certification_timeline.png") 
    print("- certification_status.png")
    print("- certification_platforms.png")
    print("- certification_dashboard.png")
    
    plt.show()
