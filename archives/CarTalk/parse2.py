from bs4 import BeautifulSoup
import threading
import requests
import re
import os
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

# Lock to prevent race conditions when writing to file
lock = threading.Lock()

# Function to extract episode title and write it to file in a thread-safe manner
def extract_episode_info(episode):
    episode_info = ""
    
    # Find the episode title in the <h2> tag
    title_tag = episode.find('h2', class_='title')
    if title_tag:
        episode_title = title_tag.get_text(strip=True)
        # Format the episode info as title
        episode_info = f"{episode_title}"

    return episode_info

# Function to write the extracted data to file in a thread-safe manner
def write_to_file(data):
    with lock:
        with open('links.txt', 'a') as file:
            file.write(f"{data}\n")

# Load your HTML file
with open('combined.html', 'r', encoding='utf-8') as file:
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

print(f"Extracted and saved episode titles using multi-threading.")

# Function to sanitize the title to make it a valid filename
def sanitize_filename(name):
    # Remove characters that are not allowed in filenames
    return re.sub(r'[<>:"/\|?*]', '', name)

# Ensure the 'audio' folder exists, create if not
if not os.path.exists('audio'):
    os.makedirs('audio')

# Open and read the list.txt file
with open('links.txt', 'r') as file:
    lines = file.readlines()

# Loop through each line in the file
for line in lines:
    # Split the line into two parts: title and URL
    if 'https://' in line:
        parts = line.split('https://', 1)
        name = parts[0].strip()  # The title before 'https://'
        url = 'https://' + parts[1].strip()  # The URL starting from 'https://'

        # Sanitize the title to create a valid filename
        filename = f"{sanitize_filename(name)}.mp3"

        # Path to save in the 'audio' folder
        filepath = os.path.join('audio', filename)

        # Download the MP3 file from the URL with a progress bar
        print(f"Downloading {name}...")

        # Get the file size from the headers
        response = requests.get(url, stream=True)
        total_size = int(response.headers.get('content-length', 0))

        # Progress bar setup
        with open(filepath, 'wb') as mp3_file, tqdm(
            desc=name,
            total=total_size,
            unit='B',
            unit_scale=True,
            unit_divisor=1024,
        ) as bar:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:  # Filter out keep-alive new chunks
                    mp3_file.write(chunk)
                    bar.update(len(chunk))

        # Print done message after finishing the current file
        print(f"Done with {name}")
