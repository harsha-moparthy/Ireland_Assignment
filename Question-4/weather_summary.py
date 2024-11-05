import pandas as pd

# Load the consumed data
weather_df = pd.read_csv('weather_updates.csv')

# Display summary statistics
print("\nSummary of Weather Updates:")
print(weather_df.describe())
print("\nNumber of Updates Consumed:", len(weather_df))
print("\nUnique Locations:", weather_df['location'].nunique())
