import requests
import json
import base64
import time

# Use the token from main.py
current_token = "TRjvHnMfDl37k6pT+hMPL9J5B9ZFauy2x9*pVUcs1LXfUHTVSM131G1ezZB61eIoaxhzwAlrwt*OkuVMO9Pxjzx7+MuX+oqv9OKDIedE7iNbLhE6Mt4p8qBmGkqrJDur+Pc4Jog1Gap+DfbJ+FnDAJzB8WanyJ0WTmN47uYM2e0gE6t9nMtdGoFW7ZNi9Z*jTaBXXq*C7QA5w77kd6QVPM7oAEWSBgyUrRd5XYCtr7X5SMWH1R506rBEWLNmtW5i1MGf0MelWQV8bfNAICk*KRtGExUlDkpV2a5FUYQqNjOS33LEiROwFWda361yiSJjj7OE6jcx0UjV1WECo*aaoBORr69zYIFfWWa4W*2i0wj6tr+D7iQ1pPoDNVaJlvcHG+yNXzQr1ucsuUweOyWe3JaugCccTL77b25DLsawQlj+svWlFz4vonWCuf6eH2R1"

def test_id(val):
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
                        # DEBUG: Print first question keys and a snippet of ENGLISH
                        print(f"\nDEBUG for {val}:")
                        print(f"Keys: {list(first_q.keys())}")
                        if 'ENGLISH' in first_q:
                            # Print common name-holding fields
                            for field in ['SUBJECT_NAME', 'TOPIC_NAME']:
                                print(f"{field}: {first_q.get(field)}")
                        
                        return True, len(q_keys), first_q.get('SUBJECT_NAME', 'Unknown')
            return False, 0, None
        else:
            return False, 0, None
    except Exception as e:
        return False, 0, None

if __name__ == "__main__":
    test_id(6464626)
