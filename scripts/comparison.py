# import pandas as pd
# import os
# from datetime import datetime
# import matplotlib.pyplot as plt

# def compare_forecast_and_actual():
#     today_str = datetime.today().strftime("%Y-%m-%d")
#     month_str = datetime.today().strftime("%Y-%m")
#     forecast_file = f"data/forecast/forecast_month_{month_str}.csv"
#     actual_file = f"data/actual/{today_str}.csv"
#     comparison_dir = f"data/comparison/{today_str}"
#     os.makedirs(comparison_dir, exist_ok=True)

#     if not os.path.exists(forecast_file):
#         raise FileNotFoundError(f"Forecast file not found: {forecast_file}")
#     if not os.path.exists(actual_file):
#         raise FileNotFoundError(f"Actual file not found: {actual_file}")

#     forecast_df = pd.read_csv(forecast_file)
#     actual_df = pd.read_csv(actual_file)

#     # Merge data
#     comparison_df = pd.merge(forecast_df, actual_df, on=["City", "Date"], how="inner")

#     # Save comparison CSV
#     comparison_csv_path = os.path.join(comparison_dir, "comparison_data.csv")
#     comparison_df.to_csv(comparison_csv_path, index=False)
#     print(f"✅ Comparison CSV saved: {comparison_csv_path}")

#     # Plot linear graph
#     plt.figure(figsize=(10, 6))
#     for city in comparison_df['City'].unique():
#         city_data = comparison_df[comparison_df['City'] == city]
#         plt.plot(city_data['Date'], city_data['Forecast_Temp_C'], label=f'{city} Forecast', linestyle='--')
#         plt.plot(city_data['Date'], city_data['Actual_Temp_C'], label=f'{city} Actual', marker='o')
#     plt.title('Forecast vs Actual Temperature')
#     plt.xlabel('Date')
#     plt.ylabel('Temperature (°C)')
#     plt.xticks(rotation=45)
#     plt.legend()
#     plt.tight_layout()
#     linear_path = os.path.join(comparison_dir, "linear_graph.png")
#     plt.savefig(linear_path)
#     plt.close()
#     print(f"📈 Linear graph saved: {linear_path}")

#     # Stacked area graph
#     plt.figure(figsize=(10, 6))
#     comparison_df.set_index('Date')[['Forecast_Temp_C', 'Actual_Temp_C']].plot.area()
#     plt.title('Stacked Area: Forecast vs Actual Temperature')
#     plt.xlabel('Date')
#     plt.ylabel('Temperature (°C)')
#     plt.tight_layout()
#     stacked_path = os.path.join(comparison_dir, "stacked_area_graph.png")
#     plt.savefig(stacked_path)
#     plt.close()
#     print(f"📊 Stacked area graph saved: {stacked_path}")

# # if __name__ == "__main__":
# #     compare_forecast_and_actual()





import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

def compare_forecast_and_actual():
    # Paths & folders
    today_str = datetime.today().strftime("%Y-%m-%d")
    data_folder = "data"
    actual_folder = os.path.join(data_folder, "actual")
    comparison_folder = os.path.join(data_folder, today_str)

    # Create comparison folder if not exists
    os.makedirs(comparison_folder, exist_ok=True)

    # Files
    forecast_month = datetime.today().strftime("%Y-%m")
    forecast_file = os.path.join(data_folder, f"forecast_month_{forecast_month}.csv")
    actual_file = os.path.join(actual_folder, f"{today_str}.csv")
    comparison_file = os.path.join(comparison_folder, "comparison_data.csv")
    linear_graph_file = os.path.join(comparison_folder, f"report_day_{today_str}_linear.png")
    stacked_area_file = os.path.join(comparison_folder, f"report_day_{today_str}_stacked_area.png")

    # Read data
    if not os.path.exists(forecast_file):
        print(f"Forecast file not found: {forecast_file}")
        return
    if not os.path.exists(actual_file):
        print(f"Actual file not found: {actual_file}")
        return

    forecast_df = pd.read_csv(forecast_file)
    actual_df = pd.read_csv(actual_file)

    # Filter forecast data only for today's date
    forecast_today_df = forecast_df[forecast_df['Date'] == today_str]

    # Merge actual and forecast on City and Date
    comparison_df = pd.merge(
        actual_df, forecast_today_df,
        on=["City", "Date"],
        how="inner",
        suffixes=('_actual', '_forecast')
    )

    if comparison_df.empty:
        print("No matching data between forecast and actual for today.")
        return

    # Save comparison CSV (overwrite)
    comparison_df.to_csv(comparison_file, index=False)
    print(f"Comparison data saved: {comparison_file}")

    # Plot linear graph (Temp Actual vs Forecast)
    plt.figure(figsize=(10, 6))
    for city in comparison_df['City'].unique():
        city_data = comparison_df[comparison_df['City'] == city]
        plt.plot(
            ['Actual', 'Forecast'],
            [city_data['Actual_Temp_C'].values[0], city_data['Forecast_Temp_C'].values[0]],
            marker='o', label=city
        )
    plt.title(f"Temperature: Actual vs Forecast ({today_str})")
    plt.ylabel("Temperature (°C)")
    plt.legend()
    plt.grid(True)
    plt.savefig(linear_graph_file)
    plt.close()
    print(f"Linear graph saved: {linear_graph_file}")

    # Plot stacked area graph for humidity (Actual and Forecast)
    plt.figure(figsize=(10, 6))
    cities = comparison_df['City'].tolist()
    actual_humidity = comparison_df['Actual_Humidity'].tolist()
    forecast_humidity = comparison_df['Forecast_Humidity'].tolist()

    plt.stackplot(
        cities,
        actual_humidity,
        forecast_humidity,
        labels=['Actual Humidity', 'Forecast Humidity'],
        colors=['#1f77b4', '#ff7f0e'],
        alpha=0.8
    )
    plt.title(f"Humidity: Actual vs Forecast (Stacked Area) ({today_str})")
    plt.ylabel("Humidity (%)")
    plt.xticks(rotation=45)
    plt.legend(loc='upper right')
    plt.tight_layout()
    plt.savefig(stacked_area_file)
    plt.close()
    print(f"Stacked area graph saved: {stacked_area_file}")

if __name__ == "__main__":
    compare_forecast_and_actual()
