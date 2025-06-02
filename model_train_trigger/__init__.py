import logging
import os
import pickle

import azure.functions as func
import pandas as pd
from azure.storage.blob import BlobServiceClient

from ml_model.noise_prediction import fetch_data_from_influxdb, train_prophet_model

CONTAINER_NAME = 'noise'


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    connect_str = os.getenv('AzureWebJobsStorage')

    df = fetch_data_from_influxdb()
    df['ds'] = pd.to_datetime(df['ds']).dt.tz_localize(None)  # Remove timezone info here if needed

    # Train the model
    model = train_prophet_model(df)

    with open('model.pkl', 'wb') as f:
        pickle.dump(model, f)
    blob_name = local_file_name = 'model.pkl'
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)

    # Create a container client
    container_client = blob_service_client.get_container_client(CONTAINER_NAME)

    # Create the container if it doesn't exist
    try:
        container_client.create_container()
    except Exception as e:
        print(f"Container already exists: {e}")

    # Create a blob client using the local file name as the name for the blob
    blob_client = container_client.get_blob_client(blob_name)

    # Upload the file
    with open(local_file_name, "rb") as data:
        blob_client.upload_blob(data, overwrite=True)

    print(f"{local_file_name} uploaded to {CONTAINER_NAME} container.")
    return func.HttpResponse(f"{local_file_name} uploaded to {CONTAINER_NAME} container.", status_code=200)

