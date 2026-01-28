import re
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from io_utils import read_json, write_lines

def search_recursive(item, img_regex, links):
    if isinstance(item, dict):
        for v in item.values(): 
            search_recursive(v, img_regex, links)
    elif isinstance(item, list):
        for v in item: 
            search_recursive(v, img_regex, links)
    elif isinstance(item, str):
        for l in img_regex.findall(item): 
            if not l.startswith('data:'):
                links.add(l)

def extract_image_links(json_file):
    data = read_json(json_file)
    
    questions = []
    if isinstance(data, dict):
        for test in data.values():
            questions.extend(test.get('questions', []))
    else:
        questions = data

    img_regex = re.compile(r'<img [^>]*src="([^"]+)"', re.IGNORECASE)
    links = set()

    search_recursive(questions, img_regex, links)
    
    if not links:
        print(f"No image links found in: {json_file}")
        return []

    output_path = os.path.join(os.path.dirname(json_file), "extracted_image_links.txt")
    write_lines(sorted(list(links)), output_path)
    
    print(f"✓ Extracted {len(links)} unique remote image links to: {output_path}")
    return sorted(list(links))