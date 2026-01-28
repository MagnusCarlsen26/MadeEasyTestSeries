import os
import re
import hashlib
from urllib.parse import urlparse

import functools

def replace_src(match, images_path):
    url = match.group(1)
    parsed = urlparse(url)
    basename = os.path.basename(parsed.path)
    if not basename or len(basename) < 5:
        basename = hashlib.md5(url.encode()).hexdigest() + ".png"
    return f'src="{images_path}{basename}"'

def localize_html(html, images_path="images/"):
    """Replaces absolute image URLs with local paths."""
    if not html:
        return html

    callback = functools.partial(replace_src, images_path=images_path)
    return re.sub(r'src="([^"]+)"', callback, html)
