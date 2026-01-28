import os
import requests
import hashlib
from urllib.parse import urlparse

def download_images(links_file, output_dir):
    if not os.path.exists(links_file):
        print(f"Links file not found: {links_file}")
        return

    os.makedirs(output_dir, exist_ok=True)
    
    with open(links_file, 'r') as f:
        links = [line.strip() for line in f if line.strip()]

    print(f"Found {len(links)} remote images to download.")
    
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    })

    downloaded = 0
    errors = 0
    skipped = 0

    for url in links:
        try:
            # Generate a clean filename from the URL path or hash it if suspicious
            parsed = urlparse(url)
            base_name = os.path.basename(parsed.path)
            
            # If the filename isn't unique enough or missing, use a hash of the URL
            if not base_name or len(base_name) < 5:
                base_name = hashlib.md5(url.encode()).hexdigest() + ".png"
            
            save_path = os.path.join(output_dir, base_name)

            if os.path.exists(save_path):
                skipped += 1
                continue

            response = session.get(url, timeout=10)
            if response.status_code == 200:
                with open(save_path, 'wb') as f:
                    f.write(response.content)
                downloaded += 1
                if downloaded % 10 == 0:
                    print(f"  Downloaded {downloaded}/{len(links)}...")
            else:
                print(f"  Failed to download {url}: Status {response.status_code}")
                errors += 1
        except Exception as e:
            print(f"  Error downloading {url}: {e}")
            errors += 1

    print("\nDownload Complete!")
    print(f"Success: {downloaded}")
    print(f"Skipped (Existing): {skipped}")
    print(f"Errors: {errors}")

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    links_txt = os.path.normpath(os.path.join(current_dir, "../extractions/extracted_image_links.txt"))
    images_dir = os.path.normpath(os.path.join(current_dir, "../extractions/images"))
    
    download_images(links_txt, images_dir)
