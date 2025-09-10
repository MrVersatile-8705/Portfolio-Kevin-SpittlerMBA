"""
Data Integration Script
Combines scraped certification data with portfolio visualization system
"""

import pandas as pd
import json
import os
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CertificationDataIntegrator:
    """Integrates scraped certification data with portfolio system"""
    
    def __init__(self):
        self.data_dir = '../../data'
        self.external_sources = os.path.join(self.data_dir, 'external-sources')
        self.processed_dir = os.path.join(self.data_dir, 'processed')
        
        # Ensure directories exist
        os.makedirs(self.external_sources, exist_ok=True)
        os.makedirs(self.processed_dir, exist_ok=True)
    
    def load_scraped_data(self):
        """Load all scraped certification data"""
        
        scraped_data = {}
        
        # Look for JSON files in external-sources
        if os.path.exists(self.external_sources):
            for filename in os.listdir(self.external_sources):
                if filename.endswith('_study_guide.json'):
                    cert_code = filename.replace('_study_guide.json', '')
                    file_path = os.path.join(self.external_sources, filename)
                    
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            scraped_data[cert_code] = data
                            logger.info(f"Loaded scraped data for {cert_code}")
                    except Exception as e:
                        logger.error(f"Error loading {filename}: {e}")
        
        return scraped_data
    
    def create_enhanced_certification_dataset(self):
        """Create enhanced dataset combining tracker data with scraped information"""
        
        # Load your current certification tracker
        tracker_data = self._load_certification_tracker()
        
        # Load scraped data
        scraped_data = self.load_scraped_data()
        
        # Enhance the dataset
        enhanced_data = []
        
        for _, cert in tracker_data.iterrows():
            cert_dict = cert.to_dict()
            
            # Add scraped information if available
            cert_name = cert['Certification']
            
            # Match certification to scraped data
            matched_scrape = None
            for scrape_key, scrape_data in scraped_data.items():
                if 'power bi' in cert_name.lower() and 'pl300' in scrape_key:
                    matched_scrape = scrape_data
                    break
                # Add more matching logic for other certifications
            
            if matched_scrape:
                # Add skills count
                if 'sections' in matched_scrape and 'skills_measured' in matched_scrape['sections']:
                    cert_dict['skills_count'] = len(matched_scrape['sections']['skills_measured'])
                    cert_dict['skills_list'] = matched_scrape['sections']['skills_measured']
                else:
                    cert_dict['skills_count'] = 0
                    cert_dict['skills_list'] = []
                
                # Add study resources count
                if 'sections' in matched_scrape and 'study_resources' in matched_scrape['sections']:
                    cert_dict['resources_count'] = len(matched_scrape['sections']['study_resources'])
                    cert_dict['study_resources'] = matched_scrape['sections']['study_resources']
                else:
                    cert_dict['resources_count'] = 0
                    cert_dict['study_resources'] = []
                
                # Add exam details
                if 'sections' in matched_scrape and 'exam_details' in matched_scrape['sections']:
                    cert_dict.update(matched_scrape['sections']['exam_details'])
            else:
                # Default values for non-scraped certifications
                cert_dict['skills_count'] = 0
                cert_dict['skills_list'] = []
                cert_dict['resources_count'] = 0
                cert_dict['study_resources'] = []
            
            enhanced_data.append(cert_dict)
        
        # Create DataFrame
        enhanced_df = pd.DataFrame(enhanced_data)
        
        # Save enhanced dataset
        output_file = os.path.join(self.processed_dir, 'enhanced_certifications.csv')
        enhanced_df.to_csv(output_file, index=False)
        
        # Also save as JSON for richer data structure
        json_file = os.path.join(self.processed_dir, 'enhanced_certifications.json')
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(enhanced_data, f, indent=2, ensure_ascii=False, default=str)
        
        logger.info(f"Enhanced certification dataset saved to {output_file}")
        return enhanced_df
    
    def _load_certification_tracker(self):
        """Load certification tracker from markdown file"""
        
        tracker_file = '../../docs/certifications-tracker.md'
        
        try:
            with open(tracker_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract table data (simple approach)
            lines = content.split('\n')
            
            # Find table rows
            data_rows = []
            in_table = False
            
            for line in lines:
                if '| Certification |' in line:
                    in_table = True
                    continue
                elif in_table and line.startswith('|') and '---' not in line:
                    # Parse table row
                    cells = [cell.strip() for cell in line.split('|')[1:-1]]  # Remove empty first/last
                    if len(cells) >= 4:
                        data_rows.append({
                            'Certification': cells[0],
                            'Platform': cells[1],
                            'Status': cells[2],
                            'Target_Completion': cells[3]
                        })
                elif in_table and not line.strip():
                    break
            
            df = pd.DataFrame(data_rows)
            
            # Convert target completion to datetime
            df['Target_Date'] = pd.to_datetime(df['Target_Completion'], errors='coerce')
            
            # Add progress percentages (estimated based on status)
            status_to_progress = {
                'Completed': 100,
                'In Progress': 50,  # You can update these manually
                'Planned': 0
            }
            
            df['Progress_Percent'] = df['Status'].map(status_to_progress).fillna(0)
            
            return df
            
        except Exception as e:
            logger.error(f"Error loading certification tracker: {e}")
            
            # Return default data if file doesn't exist
            return pd.DataFrame({
                'Certification': ['Microsoft Power BI Data Analyst Professional'],
                'Platform': ['Coursera'],
                'Status': ['In Progress'],
                'Target_Completion': ['October 2025'],
                'Target_Date': [pd.to_datetime('2025-10-01')],
                'Progress_Percent': [40]
            })
    
    def create_skills_breakdown(self):
        """Create detailed skills breakdown from scraped data"""
        
        scraped_data = self.load_scraped_data()
        skills_data = []
        
        for cert_code, cert_info in scraped_data.items():
            if 'sections' in cert_info and 'skills_measured' in cert_info['sections']:
                cert_name = cert_info['certification']
                skills = cert_info['sections']['skills_measured']
                
                for skill in skills:
                    skills_data.append({
                        'certification': cert_name,
                        'certification_code': cert_code,
                        'skill': skill,
                        'skill_category': self._categorize_skill(skill),
                        'priority': self._assess_skill_priority(skill),
                        'current_level': 'Beginner',  # Default, can be updated manually
                        'target_level': 'Intermediate',
                        'learning_resources': [],
                        'notes': ''
                    })
        
        if skills_data:
            skills_df = pd.DataFrame(skills_data)
            
            # Save skills breakdown
            output_file = os.path.join(self.processed_dir, 'skills_breakdown.csv')
            skills_df.to_csv(output_file, index=False)
            
            logger.info(f"Skills breakdown saved to {output_file}")
            return skills_df
        
        return None
    
    def _categorize_skill(self, skill):
        """Categorize a skill based on keywords"""
        
        skill_lower = skill.lower()
        
        if any(word in skill_lower for word in ['data', 'dataset', 'source', 'warehouse']):
            return 'Data Management'
        elif any(word in skill_lower for word in ['visual', 'chart', 'dashboard', 'report']):
            return 'Visualization'
        elif any(word in skill_lower for word in ['model', 'relationship', 'dax', 'measure']):
            return 'Data Modeling'
        elif any(word in skill_lower for word in ['analysis', 'analytics', 'insight']):
            return 'Analysis'
        elif any(word in skill_lower for word in ['security', 'permission', 'access']):
            return 'Security'
        else:
            return 'General'
    
    def _assess_skill_priority(self, skill):
        """Assess priority of a skill for healthcare analytics"""
        
        skill_lower = skill.lower()
        
        # High priority for healthcare analytics
        high_priority_keywords = ['dashboard', 'visual', 'data', 'analysis', 'report']
        medium_priority_keywords = ['model', 'security', 'performance']
        
        if any(word in skill_lower for word in high_priority_keywords):
            return 'High'
        elif any(word in skill_lower for word in medium_priority_keywords):
            return 'Medium'
        else:
            return 'Low'
    
    def generate_learning_roadmap(self):
        """Generate a learning roadmap based on scraped certification data"""
        
        enhanced_df = self.create_enhanced_certification_dataset()
        skills_df = self.create_skills_breakdown()
        
        roadmap = {
            'generated_date': datetime.now().isoformat(),
            'total_certifications': len(enhanced_df),
            'total_skills': len(skills_df) if skills_df is not None else 0,
            'certifications': [],
            'quarterly_plan': self._create_quarterly_plan(enhanced_df)
        }
        
        for _, cert in enhanced_df.iterrows():
            cert_info = {
                'name': cert['Certification'],
                'platform': cert['Platform'],
                'status': cert['Status'],
                'target_date': str(cert.get('Target_Date', '')),
                'skills_count': cert.get('skills_count', 0),
                'estimated_hours': self._estimate_study_hours(cert),
                'priority': self._assess_certification_priority(cert)
            }
            roadmap['certifications'].append(cert_info)
        
        # Save roadmap
        roadmap_file = os.path.join(self.processed_dir, 'learning_roadmap.json')
        with open(roadmap_file, 'w', encoding='utf-8') as f:
            json.dump(roadmap, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Learning roadmap generated: {roadmap_file}")
        return roadmap
    
    def _create_quarterly_plan(self, df):
        """Create quarterly learning plan"""
        
        # Group by target quarter
        df['target_quarter'] = pd.to_datetime(df['Target_Date'], errors='coerce').dt.to_period('Q')
        
        quarterly_plan = {}
        for quarter, group in df.groupby('target_quarter'):
            if pd.notna(quarter):
                quarterly_plan[str(quarter)] = {
                    'certifications': group['Certification'].tolist(),
                    'total_skills': group['skills_count'].sum(),
                    'focus_areas': self._identify_focus_areas(group)
                }
        
        return quarterly_plan
    
    def _identify_focus_areas(self, cert_group):
        """Identify focus areas for a group of certifications"""
        
        platforms = cert_group['Platform'].unique()
        
        focus_areas = []
        if 'Coursera' in platforms:
            focus_areas.append('Online Learning')
        if 'Microsoft Learn' in platforms:
            focus_areas.append('Microsoft Technologies')
        if 'Tableau' in platforms:
            focus_areas.append('Data Visualization')
        
        return focus_areas
    
    def _estimate_study_hours(self, cert):
        """Estimate study hours for certification"""
        
        base_hours = {
            'Google Data Analytics': 120,
            'Microsoft Power BI': 80,
            'Azure Data Engineer': 100,
            'Python for Data Science': 60,
            'Tableau Desktop': 40,
            'dbt Fundamentals': 30
        }
        
        cert_name = cert['Certification']
        for key, hours in base_hours.items():
            if key.lower() in cert_name.lower():
                return hours
        
        return 50  # Default estimate
    
    def _assess_certification_priority(self, cert):
        """Assess certification priority for healthcare analytics career"""
        
        cert_name = cert['Certification'].lower()
        
        if 'power bi' in cert_name or 'tableau' in cert_name:
            return 'High'
        elif 'azure' in cert_name or 'google' in cert_name:
            return 'Medium'
        else:
            return 'Low'

def main():
    """Main execution function"""
    
    print("🔄 Starting Data Integration Process")
    print("=" * 40)
    
    integrator = CertificationDataIntegrator()
    
    print("📊 Creating enhanced certification dataset...")
    enhanced_df = integrator.create_enhanced_certification_dataset()
    print(f"✅ Enhanced dataset created with {len(enhanced_df)} certifications")
    
    print("🎯 Creating skills breakdown...")
    skills_df = integrator.create_skills_breakdown()
    if skills_df is not None:
        print(f"✅ Skills breakdown created with {len(skills_df)} skills")
    
    print("🗺️ Generating learning roadmap...")
    roadmap = integrator.generate_learning_roadmap()
    print(f"✅ Learning roadmap generated for {roadmap['total_certifications']} certifications")
    
    print("\n🎉 Data integration complete!")
    print("\nFiles generated in data/processed/:")
    print("• enhanced_certifications.csv")
    print("• enhanced_certifications.json")
    print("• skills_breakdown.csv")
    print("• learning_roadmap.json")
    
    return {
        'enhanced_certifications': enhanced_df,
        'skills_breakdown': skills_df,
        'learning_roadmap': roadmap
    }

if __name__ == "__main__":
    main()
