"""
Enhanced Certification Data Scraper
Integrated with Kevin Spittler's Portfolio Project
Scrapes and processes certification study guides and tracks learning progress
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
from datetime import datetime, timedelta
import os
import time
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CertificationScraper:
    """Scraper for certification study guides and related data"""
    
    def __init__(self, output_dir='../../data/external-sources'):
        self.output_dir = output_dir
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
    def scrape_microsoft_pl300(self):
        """Scrape PL-300 Microsoft Power BI Data Analyst study guide"""
        
        url = "https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/pl-300"
        
        try:
            logger.info(f"Scraping PL-300 study guide from {url}")
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            study_guide_data = {
                'certification': 'Microsoft Power BI Data Analyst (PL-300)',
                'url': url,
                'scraped_date': datetime.now().isoformat(),
                'sections': {}
            }
            
            # Extract main content
            content_area = soup.find('main') or soup.find('div', class_='content')
            
            if content_area:
                # Extract skills measured
                skills_section = self._extract_skills_measured(content_area)
                if skills_section:
                    study_guide_data['sections']['skills_measured'] = skills_section
                
                # Extract study resources
                resources_section = self._extract_study_resources(content_area)
                if resources_section:
                    study_guide_data['sections']['study_resources'] = resources_section
                
                # Extract exam details
                exam_details = self._extract_exam_details(content_area)
                if exam_details:
                    study_guide_data['sections']['exam_details'] = exam_details
            
            # Save the data
            self._save_study_guide_data(study_guide_data, 'pl300')
            
            return study_guide_data
            
        except Exception as e:
            logger.error(f"Error scraping PL-300 study guide: {e}")
            return None
    
    def _extract_skills_measured(self, content):
        """Extract skills measured section"""
        skills = []
        
        # Look for skills measured section
        skills_headers = content.find_all(['h1', 'h2', 'h3'], 
                                        string=lambda text: text and 'skills measured' in text.lower())
        
        for header in skills_headers:
            # Find the next list or content
            current = header.next_sibling
            while current:
                if hasattr(current, 'name'):
                    if current.name in ['ul', 'ol']:
                        for li in current.find_all('li'):
                            skills.append(li.get_text(strip=True))
                    elif current.name in ['h1', 'h2', 'h3']:
                        break
                current = current.next_sibling
        
        return skills
    
    def _extract_study_resources(self, content):
        """Extract study resources section"""
        resources = []
        
        # Look for study resources, preparation materials, etc.
        resource_keywords = ['study resources', 'preparation', 'learning path', 'training']
        
        for keyword in resource_keywords:
            headers = content.find_all(['h1', 'h2', 'h3'], 
                                     string=lambda text: text and keyword in text.lower())
            
            for header in headers:
                current = header.next_sibling
                while current:
                    if hasattr(current, 'name'):
                        if current.name in ['ul', 'ol']:
                            for li in current.find_all('li'):
                                text = li.get_text(strip=True)
                                link = li.find('a')
                                if link:
                                    resources.append({
                                        'text': text,
                                        'url': link.get('href', '')
                                    })
                                else:
                                    resources.append({'text': text, 'url': ''})
                        elif current.name in ['h1', 'h2', 'h3']:
                            break
                    current = current.next_sibling
        
        return resources
    
    def _extract_exam_details(self, content):
        """Extract exam details like duration, questions, etc."""
        details = {}
        
        # Look for exam details in text
        text_content = content.get_text()
        
        # Common patterns for exam details
        patterns = {
            'duration': r'(\d+)\s*minutes?',
            'questions': r'(\d+)[\s-]*(\d+)?\s*questions?',
            'passing_score': r'(\d+)%?\s*pass',
        }
        
        import re
        for key, pattern in patterns.items():
            match = re.search(pattern, text_content, re.IGNORECASE)
            if match:
                details[key] = match.group(0)
        
        return details
    
    def _save_study_guide_data(self, data, certification_code):
        """Save study guide data to files"""
        
        # Save JSON data
        json_file = os.path.join(self.output_dir, f'{certification_code}_study_guide.json')
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        # Save formatted text
        txt_file = os.path.join(self.output_dir, f'{certification_code}_study_guide.txt')
        with open(txt_file, 'w', encoding='utf-8') as f:
            f.write(f"STUDY GUIDE: {data['certification']}\n")
            f.write("=" * 60 + "\n\n")
            f.write(f"Source: {data['url']}\n")
            f.write(f"Scraped: {data['scraped_date']}\n\n")
            
            for section_name, section_data in data['sections'].items():
                f.write(f"{section_name.upper().replace('_', ' ')}\n")
                f.write("-" * 40 + "\n")
                
                if isinstance(section_data, list):
                    for item in section_data:
                        if isinstance(item, dict):
                            f.write(f"• {item.get('text', '')}\n")
                            if item.get('url'):
                                f.write(f"  Link: {item['url']}\n")
                        else:
                            f.write(f"• {item}\n")
                elif isinstance(section_data, dict):
                    for key, value in section_data.items():
                        f.write(f"• {key}: {value}\n")
                else:
                    f.write(f"{section_data}\n")
                f.write("\n")
        
        logger.info(f"Study guide data saved to {json_file} and {txt_file}")
    
    def update_certification_tracker(self, certification_data):
        """Update the certification tracker with scraped data"""
        
        tracker_file = '../../docs/certifications-tracker.md'
        
        try:
            # Read current tracker
            with open(tracker_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse the markdown table (simple approach)
            lines = content.split('\n')
            
            # Find the table
            table_start = -1
            for i, line in enumerate(lines):
                if '| Certification |' in line:
                    table_start = i
                    break
            
            if table_start >= 0:
                # Add study guide information as a comment
                update_line = f"\n<!-- Study guide data updated: {datetime.now().strftime('%Y-%m-%d %H:%M')} -->\n"
                
                # Find end of table
                table_end = len(lines)
                for i in range(table_start + 3, len(lines)):  # Skip header and separator
                    if not lines[i].strip() or not lines[i].startswith('|'):
                        table_end = i
                        break
                
                # Insert update comment
                lines.insert(table_end, update_line)
                
                # Write back
                with open(tracker_file, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(lines))
                
                logger.info(f"Updated certification tracker: {tracker_file}")
        
        except Exception as e:
            logger.error(f"Error updating certification tracker: {e}")
    
    def scrape_all_certifications(self):
        """Scrape study guides for all certifications in the tracker"""
        
        results = {}
        
        # PL-300 Microsoft Power BI
        pl300_data = self.scrape_microsoft_pl300()
        if pl300_data:
            results['pl300'] = pl300_data
            time.sleep(2)  # Be respectful to servers
        
        # Add more certification scrapers here
        # azure_data = self.scrape_azure_certifications()
        # google_data = self.scrape_google_certifications()
        
        return results

def create_learning_progress_tracker(scraped_data):
    """Create a learning progress tracker from scraped data"""
    
    if not scraped_data:
        return None
    
    progress_data = []
    
    for cert_code, cert_data in scraped_data.items():
        if 'sections' in cert_data and 'skills_measured' in cert_data['sections']:
            skills = cert_data['sections']['skills_measured']
            
            for skill in skills:
                progress_data.append({
                    'certification': cert_data['certification'],
                    'skill': skill,
                    'status': 'Not Started',
                    'progress_percent': 0,
                    'last_updated': datetime.now().isoformat(),
                    'notes': ''
                })
    
    # Save as CSV for easy tracking
    if progress_data:
        df = pd.DataFrame(progress_data)
        output_file = '../../data/processed/learning_progress_tracker.csv'
        df.to_csv(output_file, index=False)
        
        logger.info(f"Learning progress tracker created: {output_file}")
        return df
    
    return None

def main():
    """Main execution function"""
    
    print("🔍 Starting Certification Data Scraper")
    print("=" * 50)
    
    # Initialize scraper
    scraper = CertificationScraper()
    
    # Scrape certification data
    print("📚 Scraping certification study guides...")
    results = scraper.scrape_all_certifications()
    
    if results:
        print(f"✅ Successfully scraped {len(results)} certifications")
        
        # Update certification tracker
        print("📝 Updating certification tracker...")
        for cert_data in results.values():
            scraper.update_certification_tracker(cert_data)
        
        # Create learning progress tracker
        print("📊 Creating learning progress tracker...")
        progress_df = create_learning_progress_tracker(results)
        
        if progress_df is not None:
            print(f"📈 Progress tracker created with {len(progress_df)} skills to track")
        
        print("\n🎉 Scraping complete!")
        print("\nFiles generated:")
        print("• Study guide JSON and text files in data/external-sources/")
        print("• Learning progress tracker CSV in data/processed/")
        print("• Updated certification tracker markdown")
        
    else:
        print("❌ No data was successfully scraped")

if __name__ == "__main__":
    main()
