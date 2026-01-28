import requests
import json
import base64
from .config import DEFAULT_HEADERS, INITIAL_TOKEN

class MadeEasyAPI:
    def __init__(self, token=INITIAL_TOKEN):
        self.token = token
        self.url = "https://think.thinkexam.com/api/v1/"

    def scrape_test(self, test_id):
        """
        Fetches question data for a given test_id.
        test_id can be a number or a base64 encoded string.
        """
        # If test_id is an integer or numeric string, encode it to base64
        if isinstance(test_id, int) or (isinstance(test_id, str) and test_id.isdigit()):
            test_id = base64.b64encode(str(test_id).encode('utf-8')).decode('utf-8')

        base_json = {
            "publicKey": "QAZWSXEDCRFVTGBYtinksaas_1@pt",
            "accessToken": self.token,
            "requestUrl": "ots2026.onlinetestseriesmadeeasy.in",
            "async": False,
            "service": "Thinkexam",
            "apiUrl": "https://think.thinkexam.com",
            "action": "getQuestiondata",
            "parameter": {"testId": test_id},
            "returnType": "json"
        }

        payload = {'data': json.dumps(base_json)}

        try:
            response = requests.post(self.url, headers=DEFAULT_HEADERS, data=payload, timeout=15)
            if response.status_code == 200:
                resp_json = response.json()
                
                # Update token if a new one is provided
                if 'ACCESS_TOKEN' in resp_json:
                    self.token = resp_json['ACCESS_TOKEN']
                
                if 'data' in resp_json:
                    return json.loads(resp_json['data'])
            return None
        except Exception as e:
            print(f"API Error: {e}")
            return None
