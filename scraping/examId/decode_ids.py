import base64
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from io_utils import read_json, write_json, write_lines

def decode_test_ids(file_path):
    data = read_json(file_path)
    
    results = []
    for item in data:
        test_id_base64 = item.get('testId')
        test_name = item.get('testName')
        
        try:
            # Decode base64
            decoded_bytes = base64.b64decode(test_id_base64)
            decoded_str = decoded_bytes.decode('utf-8')
            results.append({
                "testName": test_name,
                "originalId": test_id_base64,
                "decodedId": decoded_str
            })
        except Exception as e:
            results.append({
                "testName": test_name,
                "originalId": test_id_base64,
                "error": str(e)
            })
            
    return results

def get_decoded_id(item):
    try:
        return int(base64.b64decode(item['testId']).decode('utf-8'))
    except:
        return 0

if __name__ == "__main__":
    input_file = '/home/khushal/Desktop/Projects/MadeEasyTestSeries/scraping/examId/test_ids.json'
    output_file = '/home/khushal/Desktop/Projects/MadeEasyTestSeries/scraping/examId/decoded_test_ids.txt'
    
    data = read_json(input_file)
    
    # Sort the data list by decoding the testId to int
    data.sort(key=get_decoded_id)
    
    # Save sorted JSON back to file
    write_json(data, input_file)
    
    print(f"{'Base 10 ID':<12} | {'Test Name'}")
    print("-" * 80)
    
    output_lines = [
        f"{'Base 10 ID':<12} | {'Test Name'}",
        "-" * 80
    ]
    
    for item in data:
        val = get_decoded_id(item)
        name = item.get('testName', 'Unknown')
        if val > 0:
            print(f"{val:<12} | {name}")
            output_lines.append(f"{val:<12} | {name}")
    
    write_lines(output_lines, output_file)
    
    print(f"\nSorted {len(data)} items in {input_file}")
    print(f"Saved results to {output_file}")
