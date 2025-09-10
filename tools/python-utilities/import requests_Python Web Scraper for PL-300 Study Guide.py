import requests
from bs4 import BeautifulSoup

# Target URL
url = "https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/pl-300"

# Send GET request
response = requests.get(url)
response.raise_for_status()  # Raise error if request fails

# Parse HTML content
soup = BeautifulSoup(response.text, 'html.parser')

# Extract key sections
def extract_section(header_text):
    header = soup.find(lambda tag: tag.name.startswith('h') and header_text.lower() in tag.text.lower())
    if not header:
        return f"Section '{header_text}' not found."
    section = []
    for sibling in header.find_next_siblings():
        if sibling.name and sibling.name.startswith('h'):
            break  # Stop at next header
        section.append(sibling.get_text(strip=True))
    return "\n".join(section)

# Sections to extract
sections = ["Purpose of this document", "Skills measured", "Study resources", "Certification"]

# Save to local file
with open("pl300_study_guide.txt", "w", encoding="utf-8") as file:
    for section in sections:
        content = extract_section(section)
        file.write(f"=== {section} ===\n{content}\n\n")

print("PL-300 study guide content saved to pl300_study_guide.txt")
