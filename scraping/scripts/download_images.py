import os
import sys
import requests

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)

from downloadImages.extract_links import extract_image_links
from downloadImages.downloader import download_single_image
from utils.io_utils import read_lines, ensure_dir

def run_image_download(json_path, images_dir, max_workers=None):
    """
    Orchestrates image extraction and downloading sequentially (single-threaded).
    Note: max_workers parameter is kept for compatibility but ignored.
    """
    scraped_data_dir = os.path.dirname(json_path)
    ensure_dir(images_dir)
    
    print(f"[*] Scanning {os.path.basename(json_path)} for image links...")
    links = extract_image_links(json_path)
    
    total = len(links)
    print(f"[*] Found {total} unique links. Downloading sequentially (single-threaded for ethical scraping)...")
    
    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0"})

    stats = {'downloaded': 0, 'skipped': 0, 'error': 0}
    
    # Sequential processing - one at a time
    for i, url in enumerate(links, 1):
        try:
            status = download_single_image(url, images_dir, session)
            stats[status] += 1
        except Exception as e:
            stats['error'] += 1
        
        if i % 10 == 0 or i == total:
            sys.stdout.write(f"\r  > Progress: {i}/{total} (New: {stats['downloaded']}, Skipped: {stats['skipped']}, Errors: {stats['error']})")
            sys.stdout.flush()

    print()

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    scraped_data_dir = os.path.normpath(os.path.join(current_dir, "../scraped_data"))
    
    json_path = os.path.join(scraped_data_dir, "all_tests_questions.json")
    images_dir = os.path.join(scraped_data_dir, "images")
        
    run_image_download(json_path, images_dir)
