import json
import base64

def decode_test_ids(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    
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

if __name__ == "__main__":
    input_file = '/home/khushal/Desktop/Projects/MadeEasyTestSeries/scraping/examId/test_ids.json'
    output_file = '/home/khushal/Desktop/Projects/MadeEasyTestSeries/scraping/examId/decoded_test_ids.txt'
    
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    # Sort the data list by decoding the testId to int
    def get_decoded_id(item):
        try:
            return int(base64.b64decode(item['testId']).decode('utf-8'))
        except:
            return 0

    data.sort(key=get_decoded_id)
    
    # Save sorted JSON back to file
    with open(input_file, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"{'Base 10 ID':<12} | {'Test Name'}")
    print("-" * 80)
    
    with open(output_file, 'w') as f:
        f.write(f"{'Base 10 ID':<12} | {'Test Name'}\n")
        f.write("-" * 80 + "\n")
        for item in data:
            val = get_decoded_id(item)
            name = item.get('testName', 'Unknown')
            if val > 0:
                print(f"{val:<12} | {name}")
                f.write(f"{val:<12} | {name}\n")
    
    print(f"\nSorted {len(data)} items in {input_file}")
    print(f"Saved results to {output_file}")
