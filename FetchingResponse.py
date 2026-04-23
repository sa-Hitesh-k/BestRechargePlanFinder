import requests

def fetch_jio_data():
    """
    Directly hits the Jio API. 
    Maintains cookies in memory during the session.
    Returns the JSON data or None if failed.
    """
    plans_url = "https://www.jio.com/api/jio-mdmdata-service/mdmdata/recharge/plans"
    page_url = "https://www.jio.com/selfcare/plans/mobility/prepaid-plans-list/"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Referer": page_url,
        "Origin": "https://www.jio.com",
    }
    
    params = {
        "productType": "MOBILITY",
        "billingType": "1"
    }

    # The Session object acts like a mini-browser in memory
    with requests.Session() as session:
        session.headers.update(headers)
        
        # Step 1: Visit the page to establish a session/get initial cookies
        try:
            session.get(page_url, timeout=15)
            
            # Step 2: Request the actual JSON data
            response = session.get(plans_url, params=params, timeout=15)
            response.raise_for_status() # Crashes if 404 or 500
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Data Fetch Error: {e}")
            return None

# --- THE GUARDRAIL ---
if __name__ == "__main__":
    # This block ONLY runs if you run THIS file. 
    # It won't run when CreatingTable.py imports it.
    print("Running manual test fetch...")
    data = fetch_jio_data()
    if data:
        print(f"✅ Success! Captured {len(str(data))} bytes of data.")