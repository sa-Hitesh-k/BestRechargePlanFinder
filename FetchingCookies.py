import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# 1. Setring up Chrome Options for Network Interception
chrome_options = Options()
chrome_options.add_argument("--headless") # Run in background
chrome_options.set_capability("goog:loggingPrefs", {"performance": "ALL"})

driver = webdriver.Chrome(options=chrome_options)

# 2. Navigating to the page
driver.get("https://www.jio.com/selfcare/plans/mobility/prepaid-plans-list/")

# 3. Capturing the Logs
logs = driver.get_log("performance")

for entry in logs:
    log = json.loads(entry["message"])["message"]
    
    # Checking whether this log is a Network Response
    if log["method"] == "Network.responseReceived":
        url = log["params"]["response"]["url"]
        
        # Looking for our URL keyword
        if "plans?productType=MOBILITY" in url:
            request_id = log["params"]["requestId"]
            print(f"Found API URL: {url}")
            
            # 4. Extracting the Body (The actual JSON)
            body = driver.execute_cdp_cmd("Network.getResponseBody", {"requestId": request_id})
            print("Successfully captured plan data.")

# 5. Extract Cookies for your main FastAPI script
cookies = driver.get_cookies()
with open("jio_cookies.json", "w") as f:
    json.dump(cookies, f)

driver.quit()