"""
Updated Certification Visualizer with Real Data
Generated: 2025-09-10 05:10
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
from datetime import datetime

# Load real data
def load_real_data():
    """Load the real certification data"""
    with open('../../data/processed/visualization_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    df = pd.DataFrame(data['certifications'])
    return df, data

def create_real_dashboard():
    """Create dashboard with real data"""
    df, data = load_real_data()
    
    # Set up the figure
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Kevin Spittler MBA - Real Certification Portfolio', 
                 fontsize=20, fontweight='bold', y=0.95)
    
    # 1. Progress by Certification
    colors = ['#d32f2f' if x < 33 else '#ff9800' if x < 67 else '#4caf50' 
              for x in df['progress_percent']]
    
    bars = ax1.barh(df['certification'], df['progress_percent'], color=colors)
    ax1.set_xlabel('Progress (%)')
    ax1.set_title('Certification Progress')
    ax1.set_xlim(0, 100)
    
    # Add progress labels
    for i, (cert, progress) in enumerate(zip(df['certification'], df['progress_percent'])):
        ax1.text(progress + 2, i, f'{progress}%', va='center', ha='left', fontweight='bold')
    
    # 2. Status Distribution
    status_data = data['summary']
    labels = ['Completed', 'In Progress', 'Planned']
    sizes = [status_data['completed'], status_data['in_progress'], status_data['planned']]
    colors_pie = ['#4caf50', '#ff9800', '#2196f3']
    
    ax2.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors_pie, startangle=90)
    ax2.set_title('Status Distribution')
    
    # 3. Platform Distribution
    platforms = data['platforms']
    ax3.bar(platforms.keys(), platforms.values(), color='#2E86AB')
    ax3.set_xlabel('Platform')
    ax3.set_ylabel('Number of Certifications')
    ax3.set_title('Learning Platforms')
    plt.setp(ax3.get_xticklabels(), rotation=45, ha='right')
    
    # 4. Study Guide Coverage
    with_guides = status_data['with_study_guides']
    without_guides = status_data['total'] - with_guides
    
    ax4.bar(['With Study Guides', 'Without Study Guides'], 
            [with_guides, without_guides], 
            color=['#4caf50', '#ff9800'])
    ax4.set_ylabel('Number of Certifications')
    ax4.set_title('Study Guide Coverage')
    
    plt.tight_layout()
    return fig

if __name__ == "__main__":
    print("📊 Creating dashboard with real certification data...")
    
    try:
        fig = create_real_dashboard()
        fig.savefig('real_certification_dashboard.png', dpi=300, bbox_inches='tight')
        print("✅ Real dashboard saved as 'real_certification_dashboard.png'")
        plt.show()
        
        # Print summary
        _, data = load_real_data()
        print("\n📈 Portfolio Summary:")
        print(f"Total Certifications: {data['summary']['total']}")
        print(f"Completed: {data['summary']['completed']}")
        print(f"In Progress: {data['summary']['in_progress']}")
        print(f"Planned: {data['summary']['planned']}")
        print(f"With Study Guides: {data['summary']['with_study_guides']}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
