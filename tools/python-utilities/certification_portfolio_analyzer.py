"""
Interactive Certification Tracker - Python Environment
Simple but powerful visualizations using matplotlib and plotly
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Install plotly if not already installed: pip install plotly
try:
    import plotly.express as px
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    PLOTLY_AVAILABLE = True
except ImportError:
    print("📦 Install plotly for interactive charts: pip install plotly")
    PLOTLY_AVAILABLE = False

def load_data():
    """Load your certification data"""
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
    
    # Calculate days remaining safely
    today = pd.Timestamp.now()
    df['Days_Remaining'] = df['Target_Date'].apply(
        lambda x: max(0, (x - today).days) if pd.notna(x) else 0
    )
    
    return df

def create_static_dashboard(df):
    """Create comprehensive static dashboard"""
    
    # Set up the figure with subplots
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Kevin Spittler MBA - Certification Portfolio Dashboard', 
                 fontsize=20, fontweight='bold', y=0.95)
    
    # 1. Progress Bar Chart (Top Left)
    colors = ['#d32f2f' if x < 33 else '#ff9800' if x < 67 else '#4caf50' 
              for x in df['Progress_Percent']]
    
    bars = ax1.barh(df['Certification'], df['Progress_Percent'], color=colors)
    ax1.set_xlabel('Progress (%)', fontweight='bold')
    ax1.set_title('Certification Progress', fontweight='bold', fontsize=14)
    ax1.set_xlim(0, 100)
    
    # Add progress labels
    for i, (cert, progress) in enumerate(zip(df['Certification'], df['Progress_Percent'])):
        ax1.text(progress + 2, i, f'{progress}%', 
                va='center', ha='left', fontweight='bold')
    
    # 2. Status Distribution (Top Right)
    status_counts = df['Status'].value_counts()
    colors_pie = ['#4caf50', '#ff9800', '#2196f3']
    wedges, texts, autotexts = ax2.pie(status_counts.values, 
                                       labels=status_counts.index,
                                       autopct='%1.1f%%',
                                       colors=colors_pie,
                                       startangle=90)
    ax2.set_title('Status Distribution', fontweight='bold', fontsize=14)
    
    # 3. Platform Analysis (Bottom Left)
    platform_counts = df['Platform'].value_counts()
    bars3 = ax3.bar(platform_counts.index, platform_counts.values, 
                    color='#2E86AB', alpha=0.8)
    ax3.set_xlabel('Platform', fontweight='bold')
    ax3.set_ylabel('Number of Certifications', fontweight='bold')
    ax3.set_title('Learning Platforms', fontweight='bold', fontsize=14)
    plt.setp(ax3.get_xticklabels(), rotation=45, ha='right')
    
    # Add value labels on bars
    for bar in bars3:
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height + 0.05,
                f'{int(height)}', ha='center', va='bottom', fontweight='bold')
    
    # 4. Timeline View (Bottom Right)
    future_certs = df[df['Status'] != 'Completed'].copy()
    colors_timeline = ['#ff9800' if x == 'In Progress' else '#2196f3' 
                      for x in future_certs['Status']]
    
    y_pos = range(len(future_certs))
    scatter = ax4.scatter(future_certs['Target_Date'], y_pos, 
                         c=colors_timeline, s=100, alpha=0.7)
    
    ax4.set_yticks(y_pos)
    ax4.set_yticklabels([cert[:30] + '...' if len(cert) > 30 else cert 
                        for cert in future_certs['Certification']])
    ax4.set_xlabel('Target Completion Date', fontweight='bold')
    ax4.set_title('Upcoming Completions', fontweight='bold', fontsize=14)
    ax4.grid(True, alpha=0.3)
    
    # Add days remaining as text
    for i, (date, days) in enumerate(zip(future_certs['Target_Date'], 
                                        future_certs['Days_Remaining'])):
        ax4.text(date, i + 0.1, f'{days} days', 
                ha='center', va='bottom', fontsize=8)
    
    plt.tight_layout()
    return fig

def create_interactive_dashboard(df):
    """Create interactive dashboard with Plotly"""
    if not PLOTLY_AVAILABLE:
        print("❌ Plotly not available. Install with: pip install plotly")
        return None
        
    # Create subplot figure
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Certification Progress', 'Status Distribution', 
                       'Platform Analysis', 'Timeline View'),
        specs=[[{"type": "bar"}, {"type": "pie"}],
               [{"type": "bar"}, {"type": "scatter"}]]
    )
    
    # 1. Progress Chart
    progress_colors = ['#d32f2f' if x < 33 else '#ff9800' if x < 67 else '#4caf50' 
                      for x in df['Progress_Percent']]
    
    fig.add_trace(
        go.Bar(y=df['Certification'], x=df['Progress_Percent'],
               orientation='h', marker_color=progress_colors,
               text=[f'{x}%' for x in df['Progress_Percent']],
               textposition='outside', name='Progress'),
        row=1, col=1
    )
    
    # 2. Status Distribution
    status_counts = df['Status'].value_counts()
    fig.add_trace(
        go.Pie(labels=status_counts.index, values=status_counts.values,
               name='Status'),
        row=1, col=2
    )
    
    # 3. Platform Analysis
    platform_counts = df['Platform'].value_counts()
    fig.add_trace(
        go.Bar(x=platform_counts.index, y=platform_counts.values,
               marker_color='#2E86AB', name='Platforms'),
        row=2, col=1
    )
    
    # 4. Timeline
    future_certs = df[df['Status'] != 'Completed']
    fig.add_trace(
        go.Scatter(x=future_certs['Target_Date'], 
                  y=future_certs['Certification'],
                  mode='markers+text',
                  marker=dict(size=12, color='#F26419'),
                  text=[f'{days} days' for days in future_certs['Days_Remaining']],
                  textposition='top center', name='Timeline'),
        row=2, col=2
    )
    
    # Update layout
    fig.update_layout(
        height=800,
        title_text="Kevin Spittler MBA - Interactive Certification Dashboard",
        title_x=0.5,
        showlegend=False
    )
    
    return fig

def generate_summary_report(df):
    """Generate text summary report"""
    
    total = len(df)
    completed = len(df[df['Status'] == 'Completed'])
    in_progress = len(df[df['Status'] == 'In Progress'])
    planned = len(df[df['Status'] == 'Planned'])
    
    avg_progress = df['Progress_Percent'].mean()
    
    next_target = df[df['Status'] != 'Completed']['Target_Date'].min()
    
    report = f"""
📊 CERTIFICATION PORTFOLIO SUMMARY
{'='*50}

📈 PROGRESS OVERVIEW:
• Total Certifications: {total}
• Completed: {completed} ({completed/total*100:.1f}%)
• In Progress: {in_progress} ({in_progress/total*100:.1f}%)
• Planned: {planned} ({planned/total*100:.1f}%)
• Average Progress: {avg_progress:.1f}%

📅 TIMELINE:
• Next Target: {next_target.strftime('%B %Y') if pd.notna(next_target) else 'N/A'}

🏢 PLATFORMS:
{df['Platform'].value_counts().to_string()}

📚 CATEGORIES:
{df['Category'].value_counts().to_string()}

🎯 RECOMMENDATIONS:
• Focus on completing in-progress certifications first
• Consider prioritizing high-value certifications
• Plan learning schedule around target dates

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
"""
    
    return report

def main():
    """Main execution function"""
    print("🚀 Starting Certification Portfolio Analysis...")
    
    # Load data
    df = load_data()
    print(f"📚 Loaded {len(df)} certifications")
    
    # Create static dashboard
    print("📊 Creating static dashboard...")
    fig_static = create_static_dashboard(df)
    fig_static.savefig('certification_dashboard_static.png', 
                      dpi=300, bbox_inches='tight')
    print("✅ Static dashboard saved as 'certification_dashboard_static.png'")
    
    # Create interactive dashboard
    if PLOTLY_AVAILABLE:
        print("🎮 Creating interactive dashboard...")
        fig_interactive = create_interactive_dashboard(df)
        if fig_interactive:
            fig_interactive.write_html('certification_dashboard_interactive.html')
            print("✅ Interactive dashboard saved as 'certification_dashboard_interactive.html'")
            print("💡 Open the HTML file in your browser for interactive features!")
    
    # Generate summary report
    print("📝 Generating summary report...")
    report = generate_summary_report(df)
    
    with open('certification_summary_report.txt', 'w', encoding='utf-8') as f:
        f.write(report)
    
    print("✅ Summary report saved as 'certification_summary_report.txt'")
    print("\n" + report)
    
    print("\n🎉 Analysis complete! Files generated:")
    print("• certification_dashboard_static.png - High-quality static image")
    if PLOTLY_AVAILABLE:
        print("• certification_dashboard_interactive.html - Interactive web dashboard")
    print("• certification_summary_report.txt - Text summary")
    
    # Show the static plot
    plt.show()

if __name__ == "__main__":
    main()
