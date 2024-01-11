import pandas as pd
import matplotlib.pyplot as plt

# Load your data from a CSV file (replace 'data.csv' with your actual file)
data = pd.read_csv('data.csv')

# Assuming 'Date' is a column in your data, convert it to a datetime object with UK date format
data['Date'] = pd.to_datetime(data['Date'], dayfirst=True)  # Specify dayfirst=True

# Set 'Date' column as the index for time-based analysis
data.set_index('Date', inplace=True)

# Define the threshold for a different term (e.g., 'Calorie Goal')
calorie_goal = 2100

# Detect when you might exceed the calorie goal after 4 days of being below it
data['Calorie Prediction'] = False
for i in range(4, len(data)):
    if all(data['Kcals in'][i-4:i] < calorie_goal):
        data.loc[data.index[i], 'Calorie Prediction'] = True

# Plotting trends in 'Kcals in' instead of 'Net Diff (kcals)' with an average line
plt.figure(figsize=(12, 6))
plt.plot(data['Kcals in'], label='Kcals in', marker='o')
plt.axhline(y=calorie_goal, color='r', linestyle='--', label=f'Calorie Goal ({calorie_goal} kcal)')
plt.axhline(y=data['Kcals in'].mean(), color='g', linestyle='-', label=f'Average Kcals in ({data["Kcals in"].mean():.2f} kcal)')
plt.xlabel('Date')
plt.ylabel('Kcals')
plt.title('Caloric Trends and Calorie Prediction')
plt.legend()
plt.grid(True)

# Find dates when exceeding the calorie goal is predicted
calorie_prediction_dates = data[data['Calorie Prediction']].index

# Print the dates when exceeding the calorie goal is predicted
if not calorie_prediction_dates.empty:
    print("Dates when exceeding the calorie goal is predicted:")
    print(calorie_prediction_dates)
else:
    print("No predictions of exceeding the calorie goal in the data.")

# Show plots
plt.show()
