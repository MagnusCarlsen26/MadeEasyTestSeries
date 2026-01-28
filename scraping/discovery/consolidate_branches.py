import requests
import json
import os
import re

def discover_all_packages():
    url = "https://apilaratest.thinkexam.com/api/v1/getPackageDetail"
    
    # Store known tokens. Each token represents a session for a specific branch.
    tokens = {
        "Chemical": {
            "authorization": "W0n4i4pj+w40sULY6j5o2qQqIyG2HoGZHk+oi+08V1pjyvLzubRRih87yQzCBWVigf+tI4YuAKG8iCI3HXD+hEKceIq4om1hZaecVBRap*lPpHwf2GWj80pUTFdHoWc7gn9cu3A3ma77pCJrUYKJTKProWbE4qzbG22aKQmoRCeQWg9+SE0G03E5CEzY0g9h*QZjKh9Vqyoo1ADBBENlYsneDnq+O8mo+YNYIeiodmNKrI9p1VQusQrqV7GbTGwdLsfeodRlCQY64qCqhVU2GxXSkpN9oLnOEwQt786rVnW6jfkTBRcia0XgFucUYeeuyK5rnFiBFqR5UNq5gd*3eY+wDAiPoCpqQ1PuuUem1ZMZXrGvgAgXg072S5Ji+BBEVUZeMe+5GNm9oU+oCfbzfcL74MgeLY00kqbAFaAUN8c8xQ5YeL0c38pFgiuvQJq7ao50aaaUJaszYcLCMyRxs0abHjhpKwtk82pLJA384Z5gM4acAaskXzfiAD9ff3ohmy0RKPO6ijE9o*j21sKY+xrYHGRBem6fHE3HZvuH8zg=",
            "custom-header": "{\"token\":\"MjNjNTJhZDA1NjkyNDkzY/UEAHOqwG9ppBEFQJIw7DCBOVtmwzT6ea3sOz2GTwsPCrxTPjreYtausY0jdK7rgtovkkNA4ehyKoQ2VX78WnW7AdzVTabtDKfdAvWf83UDIe+6sOfKVSoARy4RHxIK9k2M4bzPid/os1cFdG01GRQ5Lju9iFIe6tEmsJLeX1i4hE5A91kuTKfk44k1e+Tfc5Kl3/jJ0npp4edhvYvwrf3dASfBeAEctJ+lo2hQT3QJJnbBo0dK/M9RbjyGxSYJOVP34OBksKSzk7t9n+IIPATFwqDDT9L2EpUJDX4FJ2Y7O4BAmKTrOMjWsHXa+KRnaemWI3fqbgUrj6uV3ClHMqeZ7WGL6ixYMdGIkrz8uQCMh8X3AJrLxVHIoiuo5WcTEaRzewGpuQZh4ereBqFI5P3hz3azOauDOUU3ZEyqj8VI2J21OL6n3s6X6ipanbEltIG74XdZVQU/puFqbNeI7tOPraft614z01X1MjAZSBJ9\",\"loginTime\":\"\"}"
        },
        "Computer Science": {
            "authorization": "TRjvHnMfDl37k6pT+hMPL9J5B9ZFauy2x9*pVUcs1LXfUHTVSM131G1ezZB61eIom1+iAxjaoK9OIerey1LgktagAq3S+MZ33lLNHTGozEzhcl4w8Zl2WjAw7pcvNMf+ripvPEMa5NYl2DcL3vvzvYri0uMi0PC0zHgie4+DUN*WlmIjfNdvyLb2MfVazAMu25BUH1CntskJLq*f8rem2lXafl*vIsNFJNcJl2yKibP0M0ltaiqAl*wxzRontmod972jbcQlxopoTbSu0CU0KLEEnwj7IwDwwr5LUiv3Ks1VmffQBmRpdQYik5+JFP5*USAWsyyBNeGcqtThTWL2DE0gVS5KZH+2YYDTaR6pfP7cZqU0DuQk+727gaBvVzYKRoa2EB7gyWp+gQBm0DqmczHZ02kS7JbL71dDvWLwtxndL37mo+5pp3NhY3YLmoWkSye57vLIH41dpX111Bo*IaAMyJ+a4tHonKL2RteFmn5kaktSS2J4ynKRiZMwzZ7UYYNxNN3dAplXj+u6LaII7bqqWzbbof4o8bkGe0O8jMg=",
            "custom-header": "{\"token\":\"MjNjNTJhZDA1NjkyNDkzY/UEAHOqwG9ppBEFQJIw7DCBOVtmwzT6ea3sOz2GTwsPCrxTPjreYtausY0jdK7rgtovkkNA4ehyKoQ2VX78WnUaexV/ff10lKwvGbbczxTp+zlm94jPfHt4TNaS1Ohijh4P3encXB1Pm6RSXNoGLNclyAUV3nKqYP+O9cx1zZht6swCs3nRmCSZvDLfWJVsyciiliHjD+2Fm/c+mz0r4M1t/JTM4maf64cWyStbU0Q8bt+VhdTWtEb7tjtz12iVwPwoBWS54V2ZolbFsQgN41lgBdAFNlTsQzheETkWp4+yKwiaDRI4YcaQo9KJK824ij5SX9z3UXfqEooh4v+GHIJCazV4TD7VlwxETQQ/rzUOiC4jkt2lO1+XhDHAHaE5mYJaBgKTuG1DsGdS90sdwOFb4HvDyXFzh5DQISjvnlRR7/1MMgkpmTNiANLOvMqjWqOLYHPPsXFO3X1kA2r0qVKprr50E+7hA2JprACyyr+ue2oQ8q8eGC6wFfhd7g5GLE3Yn/PpVwPPDtaNwYDaph7JigH+43ICMqifBJqaNylW\",\"loginTime\":\"1769527108931\"}"
        }
    }

    all_branches_data = {}

    for branch_name, auth in tokens.items():
        print(f"Fetching packages for {branch_name}...")
        headers = {
            "accept": "application/json, text/plain, */*",
            "authorization": auth["authorization"],
            "custom-header": auth["custom-header"],
            "Referer": "https://ots2026.onlinetestseriesmadeeasy.in/"
        }
        
        response = requests.post(url, headers=headers, data={"data": '{"dummyData":"dummy"}'})
        result = response.json()
        
        packages = result.get('data', [])
        print(f"  Found {len(packages)} packages.")
        
        for p in packages:
            # Determine branch from packageName if possible
            p_name = p.get('packageName', '')
            # Extract test IDs as a list
            test_ids = p.get('testId', '').split(',')
            
            # Clean up test IDs (remove empty strings)
            test_ids = [tid for tid in test_ids if tid]
            
            branch_key = branch_name
            if "Chemical" in p_name: branch_key = "Chemical"
            elif "Computer Science" in p_name or "CS & IT" in p_name: branch_key = "Computer Science"
            
            if branch_key not in all_branches_data:
                all_branches_data[branch_key] = []
            
            all_branches_data[branch_key].append({
                "packageName": p_name,
                "packageId": p.get('packageId'),
                "testCount": p.get('examCount'),
                "testIds": test_ids
            })

    # Save to final file
    with open("all_branches_data.json", "w") as f:
        json.dump(all_branches_data, f, indent=4)
    
    print("\nDiscovery Complete.")
    for branch, pkgs in all_branches_data.items():
        print(f"{branch}: {len(pkgs)} packages found.")

if __name__ == "__main__":
    discover_all_packages()
