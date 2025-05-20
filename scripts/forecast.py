
from playwright.sync_api import sync_playwright
import json
import os
from datetime import datetime
import pandas as pd

FORECAST_DAYS = 14
API_KEY = "0b78d84a9fa142e886663442252005"

def get_weather_data_ui(city, api_key, days):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=50)
        page = browser.new_page()
        page.goto("https://www.weatherapi.com/api-explorer.aspx#forecast")
        page.fill("#ctl00_MainContentHolder_txtAPIKey", api_key)
        page.fill("#ctl00_MainContentHolder_txtQ", city)
        page.select_option("#ctl00_MainContentHolder_cmbDays", str(days))
        page.click("button[onclick='getdata(2);']")
        page.wait_for_selector("h4:text('Response Body') + pre code")
        json_element = page.query_selector("h4:text('Response Body') + pre code")
        response_json_str = json_element.inner_text().strip() if json_element else ""
        browser.close()
        try:
            return json.loads(response_json_str)
        except json.JSONDecodeError:
            print(f"Failed to decode JSON for city: {city}")
            return None

def get_forecast_with_ui(cities):
    month_str = datetime.today().strftime("%Y-%m")
    file_path = f"data/forecast_month_{month_str}.csv"
    os.makedirs("data", exist_ok=True)
    all_data = []
    for city in cities:
        print(f"Fetching forecast for: {city}")
        result = get_weather_data_ui(city, API_KEY, FORECAST_DAYS)
        if not result or 'forecast' not in result:
            print(f"No forecast data for {city}")
            continue
        for day in result['forecast']['forecastday']:
            all_data.append({
                "City": city,
                "Date": day['date'],
                "Forecast_Temp_C": day['day']['avgtemp_c'],
                "Forecast_Humidity": day['day']['avghumidity'],
                "Forecast_Condition": day['day']['condition']['text']
            })
    df = pd.DataFrame(all_data)
    df.to_csv(file_path, index=False)
    print(f"Forecast saved: {file_path}")


# if __name__ == "__main__":
#     # Example usage with one city; use main.py for multiple cities
#     get_forecast_with_ui(["surat"])
