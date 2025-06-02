import pandas as pd
import matplotlib.pyplot as plt

# Specify the full path to the CSV file
csv_file_path = "C:/Users/lulan/Temp_db/noise_data.csv"

# Load the CSV file into a DataFrame
df = pd.read_csv(csv_file_path, names=["Date_Time", "Noise_Level"])

# Convert the "Date_Time" column to datetime format
df["Date_Time"] = pd.to_datetime(df["Date_Time"])

# Plot the noise data
plt.figure(figsize=(10, 6))
plt.plot(df["Date_Time"], df["Noise_Level"], marker='o', linestyle='-')
plt.title("Noise Data")
plt.xlabel("Date and Time")
plt.ylabel("Noise Level (dB)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
