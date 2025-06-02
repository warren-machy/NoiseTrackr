import azure.functions as func
from influxdb_client import Point
from influxdb_client.client import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

from raspberry.Datasender import Datasender

import json
import logging


def main(event: func.EventHubEvent):
    message_body = event.get_body().decode('utf-8')
    logging.info('Message received: %s', message_body)

    try:
        json_input = json.loads(message_body)
    except json.JSONDecodeError:
        logging.error('Invalid JSON format')
        return

    if 'uplink_message' not in json_input:
        logging.error('Missing uplink message data')
        return

    uplink_message = json_input['uplink_message']
    logging.info('============================================================')
    # Extract device and application IDs
    device_id = json_input['end_device_ids']['device_id']
    application_id = json_input['end_device_ids']['application_ids']['application_id']

    # Extract received timestamp
    received_at = json_input['received_at']

    # Extract gateway ID
    gateway_id = uplink_message['rx_metadata'][0]['gateway_ids']['gateway_id']

    # Extract decoded payload
    decoded_payload = uplink_message.get('decoded_payload', {})

    # Combine all extracted data
    token = "gQ9xR53v_LC_-li4zt9H6MEpOCr4Q-HsDrllePoIuW3L0nPdKoQ3N55Clul_4uZZgXi1T2RkK83TYJDA-wnwcg=="
    org = "iot"
    url = "http://20.79.153.237:8086"
    bucket = 'noisetrackr'

    client = influxdb_client.InfluxDBClient(
        url=url,
        token=token,
        org=org
    )

    write_api = client.write_api(write_options=SYNCHRONOUS)

    # Construct the Pointmk
    p = Point('noise') \
        .tag("location", 'Rosenheim') \
        .tag("latitude", 47.87006109706558) \
        .tag("longitude", 12.108124191410772) \
        .field("measurement", decoded_payload["soundAvg"])

    # Write the Point to InfluxDB

    try:
        write_api.write(bucket=bucket, org=org, record=p)
        logging.info(f'Data written to InfluxDB {p}')
    except Exception as e:
        logging.error(f'Error writing to InfluxDB: {e}')

