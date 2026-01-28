import json
import re
import os

def extract_image_links(json_file):
    if not os.path.exists(json_file):
        print(f"File not found: {json_file}")
        return

    with open(json_file, 'r', encoding='utf-8') as f:
        questions = json.load(f)

    # Regex to find src attribute in img tags
    img_regex = re.compile(r'<img [^>]*src="([^"]+)"', re.IGNORECASE)
    
    image_links = set()
    base64_count = 0
    url_links = []

    for q in questions:
        # Check all fields in the question object recursively for HTML with img tags
        search_in_dict(q, img_regex, image_links)

    for link in image_links:
        if link.startswith('data:image'):
            base64_count += 1
        else:
            url_links.append(link)

    print(f"Total Unique Images Found: {len(image_links)}")
    print(f"Base64 Embedded Images: {base64_count}")
    print(f"Remote URL Images: {len(url_links)}")
    
    output_file = os.path.join(os.path.dirname(json_file), "extracted_image_links.txt")
    with open(output_file, 'w') as f:
        for link in sorted(url_links):
            f.write(link + "\n")
    
    print(f"Remote image URLs saved to: {output_file}")

def search_in_dict(item, regex, found_links):
    if isinstance(item, dict):
        for val in item.values():
            search_in_dict(val, regex, found_links)
    elif isinstance(item, list):
        for val in item:
            search_in_dict(val, regex, found_links)
    elif isinstance(item, str):
        found = regex.findall(item)
        if found:
            for link in found:
                found_links.add(link)

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.normpath(os.path.join(current_dir, "../extractions/all_tests_questions.json"))
    extract_image_links(json_path)
