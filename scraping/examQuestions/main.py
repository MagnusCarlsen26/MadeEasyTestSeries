import requests
import json
import urllib.parse
import os
import time

# Initial token from the first successful request
INITIAL_TOKEN = "TRjvHnMfDl37k6pT+hMPL9J5B9ZFauy2x9*pVUcs1LXfUHTVSM131G1ezZB61eIoaxhzwAlrwt*OkuVMO9Pxjzx7+MuX+oqv9OKDIedE7iNbLhE6Mt4p8qBmGkqrJDur+Pc4Jog1Gap+DfbJ+FnDAJzB8WanyJ0WTmN47uYM2e0gE6t9nMtdGoFW7ZNi9Z*jTaBXXq*C7QA5w77kd6QVPM7oAEWSBgyUrRd5XYCtr7X5SMWH1R506rBEWLNmtW5i1MGf0MelWQV8bfNAICk*KRtGExUlDkpV2a5FUYQqNjOS33LEiROwFWda361yiSJjj7OE6jcx0UjV1WECo*aaoBORr69zYIFfWWa4W*2i0wj6tr+D7iQ1pPoDNVaJlvcHG+yNXzQr1ucsuUweOyWe3JaugCccTL77b25DLsawQlj+svWlFz4vonWCuf6eH2R1"

current_token = INITIAL_TOKEN

# Mapping for MCQ answers
MCQ_MAPPING = {
    "Dsdj/LJX8pBs6q+b96fwiQ==": "Option 1",
    "fhPK/WKkcuYMengj9uY6cg==": "Option 2",
    "9m/iwvJKC6coEJr5HJJczQ==": "Option 3",
    "Wkw/v0ACIC+JhZVbmq0HcA==": "Option 4"
}

# Fields to remove
GARBAGE_FIELDS = [
    "LABEL_1", "LABEL_2", "fldUnit", "IS_IMAGE_TYPE", "IS_COMPILER", 
    "IS_RECORDER", "TEST_CASE_TYPE", "fldTextAreaEnable", "ESSAY_SORT", 
    "SORTING_OPTIONS", "OPTION_LABEL", "FREE_SPACE", "ESSAY_TIME", 
    "MINIMUM_QUE_TIME", "isAnswerFileUpload", "MAX_OPT_LIMIT", "TIME", 
    "ESSAY_SORT_H", "SORTING_OPTIONS_H", "TEST_CASE_TYPE_H", "OPTION_LABEL_H",
    "DIFFCULTY_NAME", "ANSWER_TYPE"
]

GARBAGE_ENGLISH_FIELDS = [
    "SOLUTION", "ESSAY_ID", "EASSY_DETAILS", "ESSAY_NAME"
]

def decode_answer(q):
    q_type = str(q.get("QUESTION_TYPE"))
    english = q.get("ENGLISH", {})
    ans_encrypted = english.get("CORRECT_ANSWER")
    
    if q_type == "2":
        return english.get("OPT1", "Unknown")
    if q_type in ["7", "1"]:
        return MCQ_MAPPING.get(ans_encrypted, f"Encrypted MCQ ({ans_encrypted})")
    if q_type == "5":
        return f"Encrypted MSQ ({ans_encrypted})"
    return f"Unknown Type ({q_type})"

def scrape_test(test_id, test_name):
    global current_token
    url = "https://think.thinkexam.com/api/v1/"

    headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-language": "en-US,en;q=0.5",
        "cache-control": "no-cache",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "pragma": "no-cache",
        "priority": "u=0, i",
        "sec-ch-ua": '"Brave";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Linux"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "sec-gpc": "1",
        "Referer": "https://ots2026.onlinetestseriesmadeeasy.in/"
    }

    base_json = {
        "publicKey": "QAZWSXEDCRFVTGBYtinksaas_1@pt",
        "accessToken": current_token,
        "requestUrl": "ots2026.onlinetestseriesmadeeasy.in",
        "async": False,
        "service": "Thinkexam",
        "apiUrl": "https://think.thinkexam.com",
        "action": "getQuestiondata",
        "parameter": {"testId": test_id},
        "returnType": "json"
    }

    payload = {
        'data': json.dumps(base_json)
    }

    try:
        response = requests.post(url, headers=headers, data=payload)
        if response.status_code == 200:
            response_json = response.json()
            if 'ACCESS_TOKEN' in response_json:
                current_token = response_json['ACCESS_TOKEN']
            
            if 'data' in response_json:
                data_field = json.loads(response_json['data'])
                questions = []
                
                if isinstance(data_field, dict):
                    # Sort keys to maintain order if possible
                    sorted_keys = sorted([k for k in data_field.keys() if k.startswith('qu')], key=lambda x: int(x[2:]))
                    for key in sorted_keys:
                        value = data_field[key]
                        if isinstance(value, dict):
                            # Clean HINDI
                            if 'HINDI' in value:
                                del value['HINDI']
                            
                            # Clean Garbage
                            for field in GARBAGE_FIELDS:
                                if field in value:
                                    del value[field]
                            
                            english = value.get("ENGLISH")
                            if isinstance(english, dict):
                                for field in GARBAGE_ENGLISH_FIELDS:
                                    if field in english:
                                        del english[field]
                            
                            # Add Readable Answer
                            value['READABLE_ANSWER'] = decode_answer(value)
                            
                            # Add Test Info
                            value['TEST_NAME'] = test_name
                            value['TEST_ID'] = test_id
                            
                            questions.append(value)
                return questions
            else:
                print(f"  No 'data' key in response for {test_name}.")
        else:
            print(f"  Failed to fetch {test_name}. Status: {response.status_code}")
    except Exception as e:
        print(f"  Error scraping {test_name}: {e}")
    
    return None

def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    test_ids_file = os.path.normpath(os.path.join(current_dir, "../examId/test_ids.json"))
    output_file = os.path.join(current_dir, "all_tests_questions.json")
    
    with open(test_ids_file, 'r') as f:
        tests = json.load(f)

    all_questions = []
    
    # Process all tests
    for test in tests:
        test_id = test['testId']
        test_name = test['testName']
        
        print(f"Scraping: {test_name}...")
        questions = scrape_test(test_id, test_name)
        
        if questions:
            all_questions.extend(questions)
            print(f"  Fetched {len(questions)} questions.")
        
        # Save incrementally to avoid losing data
        with open(output_file, 'w') as f:
            json.dump(all_questions, f, indent=2)
        
        time.sleep(1) # Be a bit nice to the server

if __name__ == "__main__":
    main()