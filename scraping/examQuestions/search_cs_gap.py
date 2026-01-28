import requests
import json
import base64
import time

current_token = "TRjvHnMfDl37k6pT+hMPL9J5B9ZFauy2x9*pVUcs1LXfUHTVSM131G1ezZB61eIoaxhzwAlrwt*OkuVMO9Pxjzx7+MuX+oqv9OKDIedE7iNbLhE6Mt4p8qBmGkqrJDur+Pc4Jog1Gap+DfbJ+FnDAJzB8WanyJ0WTmN47uYM2e0gE6t9nMtdGoFW7ZNi9Z*jTaBXXq*C7QA5w77kd6QVPM7oAEWSBgyUrRd5XYCtr7X5SMWH1R506rBEWLNmtW5i1MGf0MelWQV8bfNAICk*KRtGExUlDkpV2a5FUYQqNjOS33LEiROwFWda361yiSJjj7OE6jcx0UjV1WECo*aaoBORr69zYIFfWWa4W*2i0wj6tr+D7iQ1pPoDNVaJlvcHG+yNXzQr1ucsuUweOyWe3JaugCccTL77b25DLsawQlj+svWlFz4vonWCuf6eH2R1"

def check_cs(val):
    global current_token
    test_id_b64 = base64.b64encode(str(val).encode('utf-8')).decode('utf-8')
    
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
        response = requests.post(url, headers=headers, data=payload)
        if response.status_code == 200:
            resp = response.json()
            if 'ACCESS_TOKEN' in resp:
                current_token = resp['ACCESS_TOKEN']
            
            if 'data' in resp:
                data = json.loads(resp['data'])
                if isinstance(data, dict):
                    q_keys = [k for k in data.keys() if k.startswith('qu')]
                    if q_keys:
                        first_q = data[q_keys[0]]
                        subj = str(first_q.get('SUBJECT_NAME', '')).upper()
                        topic = str(first_q.get('TOPIC_NAME', '')).upper()
                        
                        if 'COMPUTER' in subj or 'COMPUTER' in topic or 'CS' in subj or 'CS' in topic:
                            return True, f"Match: {subj} / {topic}"
            return False, ""
        return False, ""
    except:
        return False, ""

if __name__ == "__main__":
    # Gap is roughly 6435005 to 6464583
    # That's ~30,000 IDs. Probing selectively.
    # Let's try every 500th ID to see if we find a "CS" zone.
    print("Searching for CS tests in the gap...")
    for uid in range(6435006, 6464583, 500):
        found, info = check_cs(uid)
        if found:
            print(f"FOUND at {uid}: {info}")
        else:
            # print(f"Tested {uid}: No CS")
            pass
        time.sleep(0.2)
    print("Search complete.")
