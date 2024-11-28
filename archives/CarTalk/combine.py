import os
from bs4 import BeautifulSoup, Comment

# Get a list of all HTML files in the current directory
html_files = [f for f in os.listdir('.') if f.endswith('.html')]

# Create an empty string to store the combined HTML content
combined_html = ''

for file in html_files:
    # Open each HTML file and read its contents
    with open(file, 'r') as html_doc:
        soup = BeautifulSoup(html_doc.read(), 'html.parser')
        
        # Remove comments from the HTML content (to prevent them from showing up in the combined output)
        for element in soup.find_all(string=lambda text:isinstance(text, Comment)):
            element.extract()
        
        # Append the parsed and comment-free HTML to the combined content
        combined_html += str(soup)

# Save the combined HTML content to a new file called 'combined.html'
with open('combined.html', 'w') as f:
    f.write(combined_html)