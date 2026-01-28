import requests
import json
import base64
import time
import os

# Token from main.py
current_token = "TRjvHnMfDl37k6pT+hMPL9J5B9ZFauy2x9*pVUcs1LXfUHTVSM131G1ezZB61eIoaxhzwAlrwt*OkuVMO9Pxjzx7+MuX+oqv9OKDIedE7iNbLhE6Mt4p8qBmGkqrJDur+Pc4Jog1Gap+DfbJ+FnDAJzB8WanyJ0WTmN47uYM2e0gE6t9nMtdGoFW7ZNi9Z*jTaBXXq*C7QA5w77kd6QVPM7oAEWSBgyUrRd5XYCtr7X5SMWH1R506rBEWLNmtW5i1MGf0MelWQV8bfNAICk*KRtGExUlDkpV2a5FUYQqNjOS33LEiROwFWda361yiSJjj7OE6jcx0UjV1WECo*aaoBORr69zYIFfWWa4W*2i0wj6tr+D7iQ1pPoDNVaJlvcHG+yNXzQr1ucsuUweOyWe3JaugCccTL77b25DLsawQlj+svWlFz4vonWCuf6eH2R1"

# MCQ answer mapping
MCQ_MAPPING = {
    "Dsdj/LJX8pBs6q+b96fwiQ==": "Option 1",
    "fhPK/WKkcuYMengj9uY6cg==": "Option 2",
    "9m/iwvJKC6coEJr5HJJczQ==": "Option 3",
    "Wkw/v0ACIC+JhZVbmq0HcA==": "Option 4"
}

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

def download_hidden_test(test_id):
    global current_token
    test_id_b64 = base64.b64encode(str(test_id).encode('utf-8')).decode('utf-8')
    
    url = "https://think.thinkexam.com/api/v1/"
    headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
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
        "parameter": {"testId": test_id_b64},
        "returnType": "json"
    }

    payload = {'data': json.dumps(base_json)}
    
    try:
        response = requests.post(url, headers=headers, data=payload, timeout=15)
        if response.status_code == 200:
            resp = response.json()
            if 'ACCESS_TOKEN' in resp:
                current_token = resp['ACCESS_TOKEN']
            
            if 'data' in resp:
                data = json.loads(resp['data'])
                if isinstance(data, dict):
                    questions = []
                    for key in sorted(data.keys()):
                        if key.startswith('qu'):
                            q = data[key]
                            # Add readable answer
                            q['READABLE_ANSWER'] = decode_answer(q)
                            questions.append(q)
                    return questions
        return None
    except Exception as e:
        print(f"  Error: {e}")
        return None

if __name__ == "__main__":
    # All downloadable hidden test IDs
    hidden_tests = [
        6464563, 6464564, 6464565, 6464566, 6464567,
        6464568, 6464569, 6464570, 6464571, 6464572,
        6464626, 6464627, 6464628, 6464629, 6464630,
        6464631, 6464632, 6464633, 6464634, 6464635,
        6464636, 6464637, 6464638, 6464639, 6464640
    ]
    
    print(f"Downloading {len(hidden_tests)} hidden tests...")
    print("=" * 60)
    
    all_questions = []
    success_count = 0
    
    for test_id in hidden_tests:
        print(f"\nDownloading test {test_id}...", end=" ")
        questions = download_hidden_test(test_id)
        
        if questions:
            all_questions.extend(questions)
            success_count += 1
            print(f"✓ {len(questions)} questions")
        else:
            print("✗ Failed")
        
        time.sleep(1)  # Rate limiting
    
    # Save to file
    output_file = "extractions/hidden_tests_questions.json"
    with open(output_file, 'w') as f:
        json.dump(all_questions, f, indent=2)
    
    print(f"\n{'=' * 60}")
    print(f"✓ Downloaded {len(all_questions)} total questions from {success_count}/{len(hidden_tests)} tests")
    print(f"✓ Saved to: {output_file}")
