import requests

# 1. Use the EXACT URL from your working Selenium logs
PLANS_URL = "https://www.jio.com/api/jio-mdmdata-service/mdmdata/recharge/plans"
PAGE_URL = "https://www.jio.com/selfcare/plans/mobility/prepaid-plans-list/"

def fetch_plans():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Referer": PAGE_URL,
        "Origin": "https://www.jio.com",
    }
    
    params = {
        "productType": "MOBILITY",
        "billingType": "1"  # Don't forget the billingType!
    }

    with requests.Session() as session:
        session.headers.update(headers)
        # Optional: Visit page to get initial session cookies
        session.get(PAGE_URL, timeout=30)
        
        response = session.get(PLANS_URL, params=params, timeout=30)
        response.raise_for_status()
        return response.json()

# --- THE GUARDRAIL ---
if __name__ == "__main__":
    try:
        data = fetch_plans()
        # with open("jio_cookies.json", "w") as f:
        #     json.dump(data, f)
        print("✅ Successfully fetched plan data.")
    except Exception as e:
        print(f"❌ Failed: {e}")