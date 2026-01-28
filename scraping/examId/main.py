import requests
import json

url = "https://apilaratest.thinkexam.com/api/v1/feedback/questions"

headers = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-US,en;q=0.5",
    "authorization": "TRjvHnMfDl37k6pT+hMPL9J5B9ZFauy2x9*pVUcs1LXfUHTVSM131G1ezZB61eIom1+iAxjaoK9OIerey1LgktagAq3S+MZ33lLNHTGozEzhcl4w8Zl2WjAw7pcvNMf+ripvPEMa5NYl2DcL3vvzvYri0uMi0PC0zHgie4+DUN*WlmIjfNdvyLb2MfVazAMu25BUH1CntskJLq*f8rem2lXafl*vIsNFJNcJl2yKibP0M0ltaiqAl*wxzRontmod972jbcQlxopoTbSu0CU0KLEEnwj7IwDwwr5LUiv3Ks1VmffQBmRpdQYik5+JFP5*USAWsyyBNeGcqtThTWL2DE0gVS5KZH+2YYDTaR6pfP7cZqU0DuQk+727gaBvVzYKRoa2EB7gyWp+gQBm0DqmczHZ02kS7JbL71dDvWLwtxndL37mo+5pp3NhY3YLmoWkSye57vLIH41dpX111Bo*IaAMyJ+a4tHonKL2RteFmn5kaktSS2J4ynKRiZMwzZ7UYYNxNN3dAplXj+u6LaII7bqqWzbbof4o8bkGe0O8jMg=",
    "cache-control": "no-cache",
    "custom-header": "{\"token\":\"MjNjNTJhZDA1NjkyNDkzY/UEAHOqwG9ppBEFQJIw7DCBOVtmwzT6ea3sOz2GTwsPCrxTPjreYtausY0jdK7rgtovkkNA4ehyKoQ2VX78WnUaexV/ff10lKwvGbbczxTp+zlm94jPfHt4TNaS1Ohijh4P3encXB1Pm6RSXNoGLNclyAUV3nKqYP+O9cx1zZht6swCs3nRmCSZvDLfWJVsyciiliHjD+2Fm/c+mz0r4M1t/JTM4maf64cWyStbU0Q8bt+VhdTWtEb7tjtz12iVwPwoBWS54V2ZolbFsQgN41lgBdAFNlTsQzheETkWp4+yKwiaDRI4YcaQo9KJK824ij5SX9z3UXfqEooh4v+GHIJCazV4TD7VlwxETQQ/rzUOiC4jkt2lO1+XhDHAHaE5mYJaBgKTuG1DsGdS90sdwOFb4HvDyXFzh5DQISjvnlRR7/1MMgkpmTNiANLOvMqjWqOLYHPPsXFO3X1kA2r0qVKprr50E+7hA2JprACyyr+ue2oQ8q8eGC6wFfhd7g5GLE3Yn/PpVwPPDtaNwYDaph7JigH+43ICMqifBJqaNylW\",\"loginTime\":\"1769527108931\"}",
    "pragma": "no-cache",
    "priority": "u=1, i",
    "sec-ch-ua": "\"Brave\";v=\"143\", \"Chromium\";v=\"143\", \"Not A(Brand\";v=\"24\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Linux\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site",
    "sec-gpc": "1",
    "Referer": "https://ots2026.onlinetestseriesmadeeasy.in/"
}

# The body was multipart/form-data with a 'data' field
data = {
    "data": '{"studentId":"ODc4MjY2OTU=","testId":"NjQzMzExNQ=="}'
}

response = requests.post(url, headers=headers, data=data)

print(f"Status Code: {response.status_code}")
try:
    print(json.dumps(response.json(), indent=2))
except Exception as e:
    print(f"Error parsing JSON: {e}")
    print(response.text)