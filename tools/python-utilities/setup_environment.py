"""
Setup script for certification visualization environment
Run this to install required packages and test your environment
"""

import subprocess
import sys
import importlib

def install_package(package):
    """Install a package using pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        return True
    except subprocess.CalledProcessError:
        return False

def check_package(package_name, import_name=None):
    """Check if a package is installed"""
    if import_name is None:
        import_name = package_name
    
    try:
        importlib.import_module(import_name)
        return True
    except ImportError:
        return False

def setup_environment():
    """Set up the Python environment for certification visualization"""
    
    print("🐍 Setting up Python Environment for Certification Visualization")
    print("=" * 65)
    
    # Required packages
    packages = [
        ('pandas', 'pandas'),
        ('matplotlib', 'matplotlib'),
        ('seaborn', 'seaborn'),
        ('numpy', 'numpy'),
        ('plotly', 'plotly'),
        ('kaleido', 'kaleido')  # For plotly image export
    ]
    
    missing_packages = []
    
    print("📦 Checking installed packages...")
    for package, import_name in packages:
        if check_package(package, import_name):
            print(f"✅ {package} - installed")
        else:
            print(f"❌ {package} - missing")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n📥 Installing {len(missing_packages)} missing packages...")
        for package in missing_packages:
            print(f"Installing {package}...")
            if install_package(package):
                print(f"✅ {package} installed successfully")
            else:
                print(f"❌ Failed to install {package}")
    else:
        print("\n🎉 All packages are already installed!")
    
    print("\n🧪 Testing environment...")
    
    # Test imports
    try:
        import pandas as pd
        import matplotlib.pyplot as plt
        import seaborn as sns
        import numpy as np
        print("✅ Core packages working")
        
        import plotly.express as px
        import plotly.graph_objects as go
        print("✅ Plotly working")
        
        print("\n🎯 Environment setup complete!")
        print("\nYou can now run:")
        print("python certification_portfolio_analyzer.py")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please check package installations")
        return False

def create_sample_data():
    """Create a sample CSV file for testing"""
    import pandas as pd
    
    sample_data = {
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
        'Progress_Percent': [75, 40, 0, 0, 100, 0]
    }
    
    df = pd.DataFrame(sample_data)
    df.to_csv('certification_data.csv', index=False)
    print("📄 Sample data created: certification_data.csv")

if __name__ == "__main__":
    success = setup_environment()
    
    if success:
        print("\n📊 Creating sample data file...")
        create_sample_data()
        
        print("\n🚀 Next steps:")
        print("1. Run: python certification_portfolio_analyzer.py")
        print("2. Open the generated HTML file in your browser")
        print("3. Use the PNG file for presentations")
        print("4. Customize the data in certification_data.csv")
    else:
        print("\n❌ Setup incomplete. Please resolve package installation issues.")
