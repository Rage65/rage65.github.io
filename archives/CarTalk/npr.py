import os
import requests
from concurrent.futures import ThreadPoolExecutor

# Create directory to save HTML files if it doesn't exist
output_dir = "HTML"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Function to download and save the HTML document
def save_html(start_number):
    url = f"https://www.npr.org/podcasts/510208/car-talk/partials?start={start_number}"
    response = requests.get(url)

    # Save the HTML content without checking the status code
    file_name = os.path.join(output_dir, f"{start_number}.html")
    with open(file_name, "w", encoding="utf-8") as file:
        file.write(response.text)
    print(f"Saved {file_name}")

# Number of threads to use
max_threads = 10

# Use ThreadPoolExecutor to download HTML files concurrently
with ThreadPoolExecutor(max_workers=max_threads) as executor:
    # Submit tasks for each HTML page
    executor.map(save_html, range(1, 1199))  # From 1 to 900
