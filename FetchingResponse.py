import json
import httpx
import os
import pandas as pd

COOKIES_FILE="jio_cookies.json"
def load_cookies(filename=COOKIES_FILE):
    
    if not  os.path.isfile(filename):
        print(f"cookie file not found in {filename}")
        return None
    with open(filename) as f:
        cookies_dict=json.load(f)
        formatted_cookies={c['name']: c['value'] for c in cookies_dict}
        url="https://www.jio.com/api/jio-mdmdata-service/mdmdata/recharge/plans?productType=MOBILITY&billingType=1"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Referer": "https://www.jio.com/selfcare/plans/mobility/prepaid-plans-list/",
                }
        with httpx.Client(cookies=formatted_cookies, headers=headers) as client:
            response = client.get(url)
    
            if response.status_code == 200:
                # print("✅ Success! Captured the 31.6 KB Goldmine.")
                jsonData=response.json()
            else:
                print(f"❌ Failed with status {response.status_code}")
                print(response.text)
    # print(f"Cookies loaded from {filename}")
    return jsonData

loaded_json=load_cookies()
# print(loaded_json)

with open("RawData.json","w") as f:
    json.dump(loaded_json,f)