import os
import requests
import hashlib
import sys
from urllib.parse import urlparse

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from io_utils import write_binary

def download_single_image(url, output_dir, session=None):
    """Downloads a single image and returns status: 'downloaded', 'skipped', or 'error'"""
    try:
        save_path = get_save_path(url, output_dir)
        if os.path.exists(save_path):
            return 'skipped'

        s = session or requests.Session()
        response = s.get(url, timeout=10)
        if response.status_code == 200:
            write_binary(response.content, save_path)
            return 'downloaded'
        else:
            return 'error'
    except:
        return 'error'

def get_save_path(url, output_dir):
    parsed = urlparse(url)
    basename = os.path.basename(parsed.path)
    if not basename or len(basename) < 5:
        basename = hashlib.md5(url.encode()).hexdigest() + ".png"
    return os.path.join(output_dir, basename)
