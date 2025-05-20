



from playwright.sync_api import sync_playwright
import json
import os
from datetime import datetime
import pandas as pd

API_KEY = "0b78d84a9fa142e886663442252005"

def get_actual_weather_ui(city, api_key):
    with sync_playwright() as p:
        # browser = p.chromium.launch(headless=False, slow_mo=50)
        HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"
        browser = p.chromium.launch(headless=HEADLESS, slow_mo=50 if not HEADLESS else 0)
        page = browser.new_page()
        page.goto("https://www.weatherapi.com/api-explorer.aspx#current")

        page.fill("#ctl00_MainContentHolder_txtAPIKey", api_key)
        page.fill("#ctl00_MainContentHolder_txtQ", city)
        page.wait_for_timeout(2000)
        page.click("text=Show Response")
        page.wait_for_selector("h4:text('Response Body') + pre code")
        json_element = page.query_selector("h4:text('Response Body') + pre code")
        response_json_str = json_element.inner_text().strip() if json_element else ""
        browser.close()

        try:
            return json.loads(response_json_str)
        except json.JSONDecodeError:
            print(f"Failed to parse JSON for city: {city}")
            return None

def get_actual_weather_today(cities):
    date_str = datetime.today().strftime("%Y-%m-%d")
    folder_path = "data/actual"
    file_path = os.path.join(folder_path, f"{date_str}.csv")
    os.makedirs(folder_path, exist_ok=True)
    all_data = []
    for city in cities:
        print(f"Fetching actual weather for: {city}")
        result = get_actual_weather_ui(city, API_KEY)
        if not result or 'current' not in result:
            print(f"No actual data for {city}")
            continue
        current = result['current']
        all_data.append({
            "City": city,
            "Date": date_str,
            "Actual_Temp_C": current['temp_c'],
            "Actual_Humidity": current['humidity'],
            "Actual_Condition": current['condition']['text']
        })
    df = pd.DataFrame(all_data)
    df.to_csv(file_path, index=False)
    print(f"Actual weather saved: {file_path}")


# if __name__ == "__main__":
#     # Example usage with one city; use main.py for multiple cities
#     get_actual_weather_today(["surat"])
