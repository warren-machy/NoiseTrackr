import logging
import os
import pickle
from datetime import datetime
import azure.functions as func
from azure.storage.blob import BlobServiceClient
import pandas as pd
from ml_model.noise_prediction import make_predictions_json, make_predictions


def load_model_from_blob():
    connection_string = os.getenv("AzureWebJobsStorage")
    container_name = "noise"
    blob_name = "model.pkl"

    # Create a BlobServiceClient object
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)

    # Create a container client
    container_client = blob_service_client.get_container_client(container_name)

    # Create a blob client
    blob_client = container_client.get_blob_client(blob_name)

    # Check if the blob exists
    if not blob_client.exists():
        raise FileNotFoundError(f"The blob {blob_name} does not exist in the container {container_name}.")

    # Download and load the model
    model_pickle = blob_client.download_blob().readall()
    model = pickle.loads(model_pickle)

    return model


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('HTTP trigger function processed a request.')

    start_date = req.params.get('start_date')
    end_date = req.params.get('end_date')

    if not start_date or not end_date:
        req_body = req.get_json()
        start_date = start_date or req_body.get('start_date')
        end_date = end_date or req_body.get('end_date')

    if not start_date or not end_date:
        return func.HttpResponse("Please pass both start_date and end_date in the query string", status_code=400)

    try:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
    except ValueError:
        return func.HttpResponse("Invalid date format. Please enter dates in YYYY-MM-DD format.", status_code=400)

    if start_date >= end_date:
        return func.HttpResponse("Start date must be before end date.", status_code=400)

    try:
        model = load_model_from_blob()
    except FileNotFoundError as e:
        return func.HttpResponse(str(e), status_code=404)

    # Make predictions
    forecast = make_predictions(model, start_date, end_date)

    return func.HttpResponse(str(forecast), status_code=200)
