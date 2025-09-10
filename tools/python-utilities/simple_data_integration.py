"""
Simplified Data Integration for Certification Portfolio
Works with your existing markdown format and scraped data
"""

import pandas as pd
import json
import os
import re
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_certification_tracker():
    """Load certifications from your markdown tracker"""
    
    tracker_file = '../../docs/certifications-tracker.md'
    
    try:
        with open(tracker_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract data using regex to handle markdown formatting
        cert_pattern = r'\|\s*\[([^\]]+)\]'  # Extract certification names from links
        platform_pattern = r'\|\s*([^|]+?)\s*\|\s*<span[^>]*>([^<]+)</span>\s*\|\s*([^|]+?)\s*\|'
        
        lines = content.split('\n')
        certifications = []
        
        for line in lines:
            if '|' in line and 'Certification' not in line and '---' not in line and line.strip():
                # Split by | and clean up
                parts = [part.strip() for part in line.split('|')]
                
                if len(parts) >= 5:  # Should have empty, cert, platform, status, date, empty
                    cert_name_match = re.search(r'\[([^\]]+)\]', parts[1])
                    cert_name = cert_name_match.group(1) if cert_name_match else parts[1].strip()
                    
                    platform = parts[2].strip()
                    
                    status_match = re.search(r'>([^<]+)<', parts[3])
                    status = status_match.group(1) if status_match else parts[3].strip()
                    
                    target_date = parts[4].strip()
                    
                    certifications.append({
                        'Certification': cert_name,
                        'Platform': platform,
                        'Status': status,
                        'Target_Date': target_date,
                        'Progress_Percent': get_progress_from_status(status)
                    })
        
        return pd.DataFrame(certifications)
        
    except Exception as e:
        logger.error(f"Error loading tracker: {e}")
        return pd.DataFrame()

def get_progress_from_status(status):
    """Convert status to progress percentage"""
    status_lower = status.lower()
    if 'completed' in status_lower:
        return 100
    elif 'in progress' in status_lower:
        return 50
    else:
        return 0

def load_scraped_data():
    """Load scraped certification data"""
    scraped_data = {}
    external_dir = '../../data/external-sources'
    
    if os.path.exists(external_dir):
        for filename in os.listdir(external_dir):
            if filename.endswith('_study_guide.json'):
                cert_code = filename.replace('_study_guide.json', '')
                file_path = os.path.join(external_dir, filename)
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        scraped_data[cert_code] = data
                except Exception as e:
                    logger.error(f"Error loading {filename}: {e}")
    
    return scraped_data

def create_enhanced_dataset():
    """Create enhanced certification dataset"""
    
    # Load data
    tracker_df = load_certification_tracker()
    scraped_data = load_scraped_data()
    
    if tracker_df.empty:
        logger.error("No certification data loaded")
        return None
    
    logger.info(f"Loaded {len(tracker_df)} certifications from tracker")
    logger.info(f"Loaded {len(scraped_data)} scraped study guides")
    
    # Enhance with scraped data
    enhanced_data = []
    
    for _, cert in tracker_df.iterrows():
        cert_dict = {
            'certification': cert['Certification'],
            'platform': cert['Platform'],
            'status': cert['Status'],
            'target_date': cert['Target_Date'],
            'progress_percent': cert['Progress_Percent'],
            'skills_count': 0,
            'has_study_guide': False
        }
        
        # Check if we have scraped data for this certification
        cert_name_lower = cert['Certification'].lower()
        for scrape_key, scrape_data in scraped_data.items():
            if 'power bi' in cert_name_lower and 'pl300' in scrape_key:
                cert_dict['has_study_guide'] = True
                cert_dict['study_guide_url'] = scrape_data.get('url', '')
                
                # Add skills count if available
                if 'sections' in scrape_data and 'skills_measured' in scrape_data['sections']:
                    cert_dict['skills_count'] = len(scrape_data['sections']['skills_measured'])
                
                break
        
        enhanced_data.append(cert_dict)
    
    # Create DataFrame and save
    enhanced_df = pd.DataFrame(enhanced_data)
    
    # Save to CSV
    output_dir = '../../data/processed'
    os.makedirs(output_dir, exist_ok=True)
    
    csv_file = os.path.join(output_dir, 'enhanced_certifications.csv')
    enhanced_df.to_csv(csv_file, index=False)
    
    logger.info(f"Enhanced dataset saved to {csv_file}")
    
    return enhanced_df

def create_visualization_data():
    """Create data specifically for visualizations"""
    
    enhanced_df = create_enhanced_dataset()
    
    if enhanced_df is None:
        return None
    
    # Create visualization-ready data
    viz_data = {
        'certifications': enhanced_df.to_dict('records'),
        'summary': {
            'total': len(enhanced_df),
            'completed': len(enhanced_df[enhanced_df['status'].str.contains('Completed', case=False, na=False)]),
            'in_progress': len(enhanced_df[enhanced_df['status'].str.contains('In Progress', case=False, na=False)]),
            'planned': len(enhanced_df[enhanced_df['status'].str.contains('Planned', case=False, na=False)]),
            'with_study_guides': len(enhanced_df[enhanced_df['has_study_guide']]),
            'total_skills': int(enhanced_df['skills_count'].sum())
        },
        'platforms': enhanced_df['platform'].value_counts().to_dict(),
        'generated_date': datetime.now().strftime('%Y-%m-%d %H:%M')
    }
    
    # Save for visualization scripts
    viz_file = os.path.join('../../data/processed', 'visualization_data.json')
    with open(viz_file, 'w', encoding='utf-8') as f:
        json.dump(viz_data, f, indent=2, ensure_ascii=False)
    
    logger.info(f"Visualization data saved to {viz_file}")
    
    return viz_data

def update_visualization_script():
    """Update the visualization script to use the real data"""
    
    viz_data = create_visualization_data()
    
    if viz_data is None:
        return
    
    # Create updated visualization script
    updated_script = f'''"""
Updated Certification Visualizer with Real Data
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
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
        ax1.text(progress + 2, i, f'{{progress}}%', va='center', ha='left', fontweight='bold')
    
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
        print("\\n📈 Portfolio Summary:")
        print(f"Total Certifications: {{data['summary']['total']}}")
        print(f"Completed: {{data['summary']['completed']}}")
        print(f"In Progress: {{data['summary']['in_progress']}}")
        print(f"Planned: {{data['summary']['planned']}}")
        print(f"With Study Guides: {{data['summary']['with_study_guides']}}")
        
    except Exception as e:
        print(f"❌ Error: {{e}}")
'''
    
    # Save updated script
    script_file = 'real_certification_visualizer.py'
    with open(script_file, 'w', encoding='utf-8') as f:
        f.write(updated_script)
    
    logger.info(f"Updated visualization script saved as {script_file}")

def main():
    """Main execution function"""
    
    print("🔄 Starting Simple Data Integration")
    print("=" * 40)
    
    print("📊 Loading certification data...")
    enhanced_df = create_enhanced_dataset()
    
    if enhanced_df is not None:
        print(f"✅ Enhanced dataset created with {len(enhanced_df)} certifications")
        
        print("📈 Creating visualization data...")
        viz_data = create_visualization_data()
        
        print("🎨 Updating visualization script...")
        update_visualization_script()
        
        print("\\n🎉 Integration complete!")
        print("\\nFiles generated:")
        print("• enhanced_certifications.csv")
        print("• visualization_data.json") 
        print("• real_certification_visualizer.py")
        
        print("\\n📊 Portfolio Summary:")
        summary = viz_data['summary']
        print(f"Total Certifications: {summary['total']}")
        print(f"Completed: {summary['completed']}")
        print(f"In Progress: {summary['in_progress']}")
        print(f"Planned: {summary['planned']}")
        print(f"With Study Guides: {summary['with_study_guides']}")
        
        return viz_data
        
    else:
        print("❌ Failed to load certification data")
        return None

if __name__ == "__main__":
    main()
