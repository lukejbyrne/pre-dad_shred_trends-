import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def identify_trend_before_binge(data, target_percentage, rebound_percentage):
    """
    Identifies trends before potential binges for each 7-day period and provides text and graph summaries.

    :param data: DataFrame containing the data.
    :param target_percentage: The percentage of the target calorie goal below which the trend is considered.
    :param rebound_percentage: The percentage of rebound calories above the lowest point of the trend.
    """

    # Set a constant calorie goal (e.g., 2100 kcal)
    calorie_goal = 2100

    i = 0  # Initialize the starting index
    while i + 6 < len(data):  # Iterate through each 7-day period
        weekly_data = data[i:i+7].copy()  # Make a copy of the slice

        # Detect when a trend before a binge occurs
        weekly_data.loc[:, 'Trend Before Binge'] = False  # Use .loc for assignment
        lowest_point = None  # Initialize lowest_point with None

        for j in range(7):
            if not np.isnan(weekly_data['Kcals in'].iloc[j]):  # Check for NaN
                if lowest_point is None or weekly_data['Kcals in'].iloc[j] < lowest_point:
                    lowest_point = weekly_data['Kcals in'].iloc[j]

                if weekly_data['Kcals in'].iloc[j] < target_percentage * calorie_goal:
                    weekly_data.loc[weekly_data.index[j], 'Trend Before Binge'] = True  # Use .loc for assignment

        # Calculate the rebound value as a percentage above the lowest point of the trend
        weekly_data.loc[:, 'Rebound'] = 0  # Use .loc for assignment
        for j in range(1, 7):
            if weekly_data['Trend Before Binge'].iloc[j]:
                weekly_data.loc[weekly_data.index[j], 'Rebound'] = ((weekly_data['Kcals in'].iloc[j] - lowest_point) / lowest_point) * 100  # Use .loc for assignment

        # Calculate the mean calories for the week, handling NaN values
        weekly_mean_calories = weekly_data['Kcals in'].mean(skipna=True)

        # Get the date range for this 7-day period
        date_range = f"{weekly_data.index[0].strftime('%d %b')} - {weekly_data.index[-1].strftime('%d %b')}"

        # Check if a trend before a binge was detected during the week
        if weekly_data['Trend Before Binge'].any():
            trend_summary = f"{date_range}: When you eat {int(calorie_goal - weekly_mean_calories)} kcals under your goal for {weekly_data['Trend Before Binge'].sum()} days, " \
                            f"you rebound eating {int(rebound_percentage * calorie_goal)} calories " \
                            f"({rebound_percentage * 100}% higher than the goal) for {weekly_data['Trend Before Binge'].sum()} days. " \
                            f"Meaning in any 7-day period, you could have instead eaten {int(weekly_mean_calories)} " \
                            f"mean calories for the same impact."

            # Print the trend summary for this 7-day period along with the date range
            print(trend_summary)
            print()

            # Plotting trends in 'Kcals in' with the identified trend before a binge
            plt.figure(figsize=(12, 6))
            plt.plot(weekly_data['Kcals in'], label='Kcals in', marker='o')
            plt.axhline(y=calorie_goal, color='r', linestyle='--', label=f'Calorie Goal ({calorie_goal} kcal)')
            plt.xlabel('Date')
            plt.ylabel('Kcals')
            plt.title(f'Caloric Trends with Trend Before a Binge ({date_range})')
            plt.legend()
            plt.grid(True)

            # Overlay the trend before a binge on the graph
            plt.fill_between(weekly_data.index, 0, weekly_data['Trend Before Binge'] * calorie_goal,
                            where=weekly_data['Trend Before Binge'], color='gray', alpha=0.5, label='Trend Before Binge')

            # Show the plot
            plt.show()

        i += 7  # Move to the next 7-day period

# Example usage
if __name__ == "__main__":
    # Load your data from a CSV file (replace 'data.csv' with your actual file)
    data = pd.read_csv('data.csv')

    # Assuming 'Date' is a column in your data, convert it to a datetime object with UK date format
    data['Date'] = pd.to_datetime(data['Date'], dayfirst=True)  # Specify dayfirst=True

    # Set 'Date' column as the index for time-based analysis
    data.set_index('Date', inplace=True)

    # Define the target percentage and rebound percentage (adjust as needed)
    target_percentage = 0.8  # Example: 80% of target
    rebound_percentage = 0.2  # Example: 20% rebound

    # Identify and summarize trends before potential binges for each 7-day period
    identify_trend_before_binge(data, target_percentage, rebound_percentage)
