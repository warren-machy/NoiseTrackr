import pandas as pd
from prophet import Prophet
from influxdb_client import InfluxDBClient
import pickle
from datetime import datetime

bucket = "noisetrackr".strip()
org = "iot".strip()
token = "gQ9xR53v_LC_-li4zt9H6MEpOCr4Q-HsDrllePoIuW3L0nPdKoQ3N55Clul_4uZZgXi1T2RkK83TYJDA-wnwcg==".strip()
url = "http://20.79.153.237:8086".strip()

def fetch_data_from_influxdb():
    client = InfluxDBClient(url=url, token=token, org=org)

    query = f'from(bucket: "{bucket}") |> range(start: -30d) |> filter(fn: (r) => r._measurement == "noise")'
    tables = client.query_api().query(query)

    data = []
    for table in tables:
        for record in table.records:
            timestamp = record.get_time()
            value = record.get_value()
            longitude = record.values.get('longitude', None)
            latitude = record.values.get('latitude', None)
            location = record.values.get('location', None)
            data.append((timestamp, value, longitude, latitude, location))

    return pd.DataFrame(data, columns=['ds', 'y', 'longitude', 'latitude', 'location'])

def train_prophet_model(df):
    df['ds'] = pd.to_datetime(df['ds']).dt.tz_localize(None)
    
    if df.dropna().shape[0] < 2:
        raise ValueError('Dataframe has less than 2 non-NaN rows.')

    model = Prophet()
    model.fit(df[['ds', 'y']])
    return model

def make_predictions(model, start_date, end_date):
    # Create future dataframe based on start and end dates
    future_dates = pd.date_range(start=start_date, end=end_date, freq='D')
    future = pd.DataFrame(future_dates, columns=['ds'])
    # Make predictions
    forecast = model.predict(future)
    return forecast

def store_predictions_locally(forecast, file_path):
    # Convert forecast to JSON
    forecast.to_json(file_path, orient='records', date_format='iso')
    print(f"Predictions saved to {file_path}")

def main():
    # Fetch data
    df = fetch_data_from_influxdb()
    df['ds'] = pd.to_datetime(df['ds']).dt.tz_localize(None)  # Remove timezone info here if needed

    # Check data
    print("Fetched Data:")
    print(df.head())
    print(f"Total rows fetched: {df.shape[0]}")
    print(f"Non-NaN rows: {df.dropna().shape[0]}")

    # Train the model
    model = train_prophet_model(df)

    # Get user input for prediction start and end dates
    start_date = input("Enter the start date for predictions (YYYY-MM-DD): ")
    end_date = input("Enter the end date for predictions (YYYY-MM-DD): ")

    # Validate and parse dates
    try:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
    except ValueError:
        print("Invalid date format. Please enter dates in YYYY-MM-DD format.")
        return

    if start_date >= end_date:
        print("Start date must be before end date.")
        return

    # Make predictions
    forecast = make_predictions(model, start_date, end_date)

    # Store predictions locally
    predictions_file_path = 'predicted_noise_levels.json'
    store_predictions_locally(forecast, predictions_file_path)

    # Save the model locally
    model_file_path = 'prophet_model.pkl'
    with open(model_file_path, 'wb') as f:
        pickle.dump(model, f)
    print(f"Model saved to {model_file_path}")

if __name__ == "__main__":
    main()




