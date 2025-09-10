"""
Enhanced Certification Tracker Visualization Suite
Interactive and advanced Python visualizations for portfolio presentation
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.figure_factory as ff
from datetime import datetime, timedelta
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# Set up styling
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

# Brand colors for consistency
BRAND_COLORS = {
    'primary': '#2E86AB',
    'secondary': '#F26419', 
    'accent': '#F6F5F5',
    'success': '#4CAF50',
    'warning': '#FF9800',
    'danger': '#D32F2F',
    'info': '#2196F3'
}

def load_certification_data():
    """Load certification data from your tracker"""
    # Read from your actual certifications-tracker.md or create DataFrame
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
        ],
        'Priority': [
            'High', 'High', 'Medium',
            'High', 'Completed', 'Medium'
        ],
        'Cost': [
            '$49/month', '$49/month', 'Free',
            '$49/month', 'Free', 'Free'
        ],
        'Duration_Weeks': [24, 20, 12, 16, 8, 6]
    }
    
    df = pd.DataFrame(data)
    df['Target_Date'] = pd.to_datetime(df['Target_Date'])
    
    # Enhanced calculations
    today = pd.Timestamp.now()
    df['Days_Remaining'] = (df['Target_Date'] - today).dt.days
    df['Days_Remaining'] = df['Days_Remaining'].apply(lambda x: max(0, x) if pd.notna(x) else 0)
    
    # Add quarters for timeline analysis
    df['Target_Quarter'] = df['Target_Date'].dt.to_period('Q')
    
    # Calculate investment
    df['Monthly_Cost'] = df['Cost'].apply(
        lambda x: 49 if '$49' in x else 0
    )
    df['Total_Investment'] = df['Monthly_Cost'] * (df['Duration_Weeks'] / 4)
    
    return df

def create_interactive_dashboard(df):
    """Create comprehensive interactive dashboard using Plotly"""
    
    # Create subplots
    fig = make_subplots(
        rows=3, cols=2,
        subplot_titles=(
            'Certification Progress', 'Status Distribution',
            'Timeline View', 'Platform Analysis',
            'Investment Analysis', 'Quarterly Planning'
        ),
        specs=[
            [{"type": "bar"}, {"type": "pie"}],
            [{"type": "scatter"}, {"type": "bar"}],
            [{"type": "bar"}, {"type": "bar"}]
        ],
        vertical_spacing=0.1
    )
    
    # 1. Progress Chart
    progress_colors = [
        BRAND_COLORS['danger'] if x < 33 else 
        BRAND_COLORS['warning'] if x < 67 else 
        BRAND_COLORS['success'] 
        for x in df['Progress_Percent']
    ]
    
    fig.add_trace(
        go.Bar(
            y=df['Certification'],
            x=df['Progress_Percent'],
            orientation='h',
            marker_color=progress_colors,
            text=[f'{x}%' for x in df['Progress_Percent']],
            textposition='outside',
            name='Progress'
        ),
        row=1, col=1
    )
    
    # 2. Status Distribution
    status_counts = df['Status'].value_counts()
    fig.add_trace(
        go.Pie(
            labels=status_counts.index,
            values=status_counts.values,
            marker_colors=[BRAND_COLORS['success'], BRAND_COLORS['warning'], BRAND_COLORS['info']],
            name='Status'
        ),
        row=1, col=2
    )
    
    # 3. Timeline View
    future_certs = df[df['Status'] != 'Completed'].copy()
    fig.add_trace(
        go.Scatter(
            x=future_certs['Target_Date'],
            y=future_certs['Certification'],
            mode='markers+text',
            marker=dict(
                size=future_certs['Progress_Percent']/5 + 10,
                color=future_certs['Progress_Percent'],
                colorscale='RdYlGn',
                showscale=True
            ),
            text=future_certs['Days_Remaining'].astype(str) + ' days',
            textposition='top center',
            name='Timeline'
        ),
        row=2, col=1
    )
    
    # 4. Platform Analysis
    platform_counts = df['Platform'].value_counts()
    fig.add_trace(
        go.Bar(
            x=platform_counts.index,
            y=platform_counts.values,
            marker_color=BRAND_COLORS['primary'],
            name='Platforms'
        ),
        row=2, col=2
    )
    
    # 5. Investment Analysis
    investment_data = df[df['Total_Investment'] > 0]
    fig.add_trace(
        go.Bar(
            x=investment_data['Certification'],
            y=investment_data['Total_Investment'],
            marker_color=BRAND_COLORS['secondary'],
            name='Investment'
        ),
        row=3, col=1
    )
    
    # 6. Quarterly Planning
    quarterly_data = df.groupby('Target_Quarter').size()
    fig.add_trace(
        go.Bar(
            x=[str(q) for q in quarterly_data.index],
            y=quarterly_data.values,
            marker_color=BRAND_COLORS['accent'],
            name='Quarterly'
        ),
        row=3, col=2
    )
    
    # Update layout
    fig.update_layout(
        height=1200,
        title_text="Kevin Spittler MBA - Professional Certification Dashboard",
        title_x=0.5,
        title_font_size=20,
        showlegend=False,
        template='plotly_white'
    )
    
    # Update axes
    fig.update_xaxes(title_text="Progress (%)", row=1, col=1)
    fig.update_xaxes(title_text="Target Date", row=2, col=1)
    fig.update_xaxes(title_text="Platform", row=2, col=2)
    fig.update_xaxes(title_text="Certification", row=3, col=1)
    fig.update_xaxes(title_text="Quarter", row=3, col=2)
    
    fig.update_yaxes(title_text="Certification", row=1, col=1)
    fig.update_yaxes(title_text="Certification", row=2, col=1)
    fig.update_yaxes(title_text="Count", row=2, col=2)
    fig.update_yaxes(title_text="Investment ($)", row=3, col=1)
    fig.update_yaxes(title_text="Count", row=3, col=2)
    
    return fig

def create_progress_tracker(df):
    """Create animated progress tracker"""
    
    # Simulate progress over time for animation
    dates = pd.date_range(start='2024-01-01', end='2025-12-31', freq='M')
    
    progress_data = []
    for cert in df['Certification']:
        cert_data = df[df['Certification'] == cert].iloc[0]
        current_progress = cert_data['Progress_Percent']
        
        # Create realistic progress timeline
        for i, date in enumerate(dates):
            if cert_data['Status'] == 'Completed':
                progress = 100 if date <= cert_data['Target_Date'] else 100
            elif cert_data['Status'] == 'In Progress':
                # Simulate gradual progress
                months_since_start = max(0, i - 3)  # Assume started 3 months ago
                progress = min(current_progress, (months_since_start * 5))
            else:
                progress = 0
                
            progress_data.append({
                'Date': date,
                'Certification': cert,
                'Progress': progress,
                'Status': cert_data['Status'],
                'Category': cert_data['Category']
            })
    
    progress_df = pd.DataFrame(progress_data)
    
    # Create animated line chart
    fig = px.line(
        progress_df,
        x='Date',
        y='Progress',
        color='Certification',
        title='Certification Progress Over Time',
        labels={'Progress': 'Progress (%)', 'Date': 'Date'},
        range_y=[0, 100]
    )
    
    fig.update_layout(
        template='plotly_white',
        title_x=0.5,
        height=600
    )
    
    return fig

def create_skills_analysis(df):
    """Create skills development analysis"""
    
    # Define skills mapping
    skills_mapping = {
        'Google Data Analytics Professional': ['Data Cleaning', 'Statistical Analysis', 'Data Visualization', 'SQL', 'Spreadsheets'],
        'Microsoft Power BI Data Analyst Professional': ['DAX', 'Power Query', 'Data Modeling', 'Business Intelligence', 'Dashboards'],
        'Azure Data Engineer Associate': ['Cloud Computing', 'ETL Pipelines', 'Data Warehousing', 'Azure Services', 'Big Data'],
        'Python for Data Science': ['Python Programming', 'Pandas', 'NumPy', 'Machine Learning', 'Data Analysis'],
        'Tableau Desktop Specialist': ['Data Visualization', 'Tableau', 'Dashboard Design', 'Visual Analytics'],
        'dbt Fundamentals': ['Data Transformation', 'SQL', 'Data Modeling', 'Version Control', 'Testing']
    }
    
    # Create skills DataFrame
    skills_data = []
    for cert, skills in skills_mapping.items():
        cert_info = df[df['Certification'] == cert].iloc[0]
        for skill in skills:
            skills_data.append({
                'Certification': cert,
                'Skill': skill,
                'Status': cert_info['Status'],
                'Progress': cert_info['Progress_Percent'],
                'Category': cert_info['Category']
            })
    
    skills_df = pd.DataFrame(skills_data)
    
    # Create skills network visualization
    fig = px.sunburst(
        skills_df,
        path=['Category', 'Certification', 'Skill'],
        values='Progress',
        title='Skills Development Hierarchy',
        color='Progress',
        color_continuous_scale='RdYlGn'
    )
    
    fig.update_layout(
        template='plotly_white',
        title_x=0.5,
        height=700
    )
    
    return fig

def generate_portfolio_report(df):
    """Generate comprehensive portfolio report"""
    
    report = {
        'total_certifications': len(df),
        'completed': len(df[df['Status'] == 'Completed']),
        'in_progress': len(df[df['Status'] == 'In Progress']),
        'planned': len(df[df['Status'] == 'Planned']),
        'completion_rate': (len(df[df['Status'] == 'Completed']) / len(df)) * 100,
        'average_progress': df['Progress_Percent'].mean(),
        'total_investment': df['Total_Investment'].sum(),
        'next_completion': df[df['Status'] != 'Completed']['Target_Date'].min(),
        'skills_categories': df['Category'].nunique(),
        'platforms_used': df['Platform'].nunique()
    }
    
    return report

def save_all_visualizations(df):
    """Save all visualizations for portfolio"""
    
    print("🚀 Generating comprehensive certification visualizations...")
    
    # 1. Interactive Dashboard
    dashboard = create_interactive_dashboard(df)
    dashboard.write_html('certification_interactive_dashboard.html')
    dashboard.write_image('certification_interactive_dashboard.png', width=1400, height=1200)
    print("✅ Interactive dashboard saved")
    
    # 2. Progress Tracker
    progress_tracker = create_progress_tracker(df)
    progress_tracker.write_html('certification_progress_tracker.html')
    progress_tracker.write_image('certification_progress_tracker.png', width=1200, height=600)
    print("✅ Progress tracker saved")
    
    # 3. Skills Analysis
    skills_analysis = create_skills_analysis(df)
    skills_analysis.write_html('certification_skills_analysis.html')
    skills_analysis.write_image('certification_skills_analysis.png', width=800, height=700)
    print("✅ Skills analysis saved")
    
    # 4. Portfolio Report
    report = generate_portfolio_report(df)
    
    # Save report as JSON and formatted text
    import json
    with open('portfolio_report.json', 'w') as f:
        json.dump(report, f, indent=2, default=str)
    
    # Create formatted report
    report_text = f"""
# Professional Certification Portfolio Report
Generated: {datetime.now().strftime('%B %d, %Y')}

## Summary Statistics
- Total Certifications: {report['total_certifications']}
- Completed: {report['completed']} ({report['completion_rate']:.1f}%)
- In Progress: {report['in_progress']}
- Planned: {report['planned']}
- Average Progress: {report['average_progress']:.1f}%
- Total Investment: ${report['total_investment']:.0f}
- Next Target Completion: {report['next_completion'].strftime('%B %Y') if pd.notna(report['next_completion']) else 'N/A'}
- Skill Categories: {report['skills_categories']}
- Learning Platforms: {report['platforms_used']}

## Portfolio Impact
This certification portfolio demonstrates:
1. Strategic learning approach across multiple platforms
2. Comprehensive skill development in healthcare analytics
3. Commitment to continuous professional development
4. Technical proficiency in modern data tools

## Files Generated
- certification_interactive_dashboard.html - Interactive web dashboard
- certification_progress_tracker.html - Progress timeline
- certification_skills_analysis.html - Skills development analysis
- Static PNG versions of all visualizations
- portfolio_report.json - Machine-readable data
"""
    
    with open('portfolio_report.md', 'w') as f:
        f.write(report_text)
    
    print("✅ Portfolio report saved")
    print("\n📊 Files Generated:")
    print("- certification_interactive_dashboard.html & .png")
    print("- certification_progress_tracker.html & .png") 
    print("- certification_skills_analysis.html & .png")
    print("- portfolio_report.json")
    print("- portfolio_report.md")
    
    return report

# Main execution
if __name__ == "__main__":
    print("🎯 Kevin Spittler MBA - Certification Portfolio Visualizer")
    print("=" * 60)
    
    # Load data
    df = load_certification_data()
    print(f"📚 Loaded {len(df)} certifications")
    
    # Generate all visualizations
    report = save_all_visualizations(df)
    
    print("\n🎉 Visualization suite complete!")
    print("💡 Open the HTML files in your browser for interactive dashboards")
    print("📱 Use PNG files for static presentations and portfolios")
    print("📝 Check portfolio_report.md for comprehensive analysis")
