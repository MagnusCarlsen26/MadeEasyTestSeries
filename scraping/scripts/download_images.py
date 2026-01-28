import os
import sys
import requests

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)

from downloadImages.extract_links import extract_image_links
from downloadImages.downloader import download_single_image
from io_utils import read_lines

def run_image_download(json_path, images_dir):
    """Orchestrates image extraction and downloading."""
    scraped_data_dir = os.path.dirname(json_path)
    
    # 1. Step 1: Link Extraction
    print(f"[*] Scanning {os.path.basename(json_path)} for image links...")
    links = extract_image_links(json_path)
    
    # 2. Step 2: Downloading
    print(f"[*] Found {len(links)} unique links.")
    
    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0"})

    stats = {'downloaded': 0, 'skipped': 0, 'error': 0}
    
    for i, url in enumerate(links, 1):
        status = download_single_image(url, images_dir, session)
        stats[status] += 1
        
        if i % 10 == 0 or i == len(links):
            print(f"  > Progress: {i}/{len(links)} (New: {stats['downloaded']}, Skipped: {stats['skipped']}, Errors: {stats['error']})", end='\r')

    print_stats(stats, links)

def print_stats(stats, links):
    print(f"Total Processed : {len(links)}")
    print(f"New Downloads   : {stats['downloaded']}")
    print(f"Already Exists  : {stats['skipped']}")
    print(f"Failed Tasks    : {stats['error']}")

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    scraped_data_dir = os.path.normpath(os.path.join(current_dir, "../scraped_data"))
    
    json_path = os.path.join(scraped_data_dir, "all_tests_questions.json")
    images_dir = os.path.join(scraped_data_dir, "images")
    
    run_image_download(json_path, images_dir)
