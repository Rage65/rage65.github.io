from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import threading

# Lock to prevent race conditions when writing to file
lock = threading.Lock()

# Function to extract episode title and download link
def extract_episode_info(episode):
    episode_info = ""
    
    # Find the episode title in the <h2> tag
    title_tag = episode.find('h2', class_='title')
    if title_tag:
        episode_title = title_tag.get_text(strip=True)
        
        # Find the download link in the <li> tag with class 'audio-tool-download'
        download_li = episode.find('li', class_='audio-tool-download')
        if download_li:
            a_tag = download_li.find('a', href=True)
            if a_tag:
                download_link = a_tag['href']
                # Format the episode info as title and download link
                episode_info = f"{episode_title} {download_link}"
    
    return episode_info

# Function to write the extracted data to file in a thread-safe manner
def write_to_file(data):
    with lock:
        with open('links.txt', 'a') as file:
            file.write(f"{data}\n")

# Load your HTML file
with open('index.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

# Parse the HTML content
soup = BeautifulSoup(html_content, 'html.parser')

# Find all 'article' elements with class 'podcast-episode'
episodes = soup.find_all('article', class_='podcast-episode')

# Use ThreadPoolExecutor to handle multi-threading
with ThreadPoolExecutor(max_workers=10) as executor:
    for episode in episodes:
        # Extract episode info in a separate thread and write it to the file
        episode_info = executor.submit(extract_episode_info, episode)
        if episode_info.result():  # Ensure that valid data is processed
            executor.submit(write_to_file, episode_info.result())

print(f"Extracted and saved episode titles and download links using multi-threading.")
