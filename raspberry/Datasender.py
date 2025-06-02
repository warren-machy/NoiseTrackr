import random
import time

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import ASYNCHRONOUS


class Datasender:
    def __init__(self, data : dict):
        self.data = data

    def start(self, refresh_rate : float = 10.0):
        client = self.__get_client()
        while True:
            point = self.__create_point(self.data).field("measurement", random.randint(60,70)) # <----- THIS RANDOM MUST BE REPLACED BY NOISE DATA!
            client.write_api(write_options=ASYNCHRONOUS).write(bucket="noisetrackr", org="iot", record=point)
            print(f"SENT: {point}")
            time.sleep(refresh_rate)

    def __get_client(self):
        token = "gQ9xR53v_LC_-li4zt9H6MEpOCr4Q-HsDrllePoIuW3L0nPdKoQ3N55Clul_4uZZgXi1T2RkK83TYJDA-wnwcg=="
        org = "iot"
        url = "http://20.79.153.237:8086"
        return InfluxDBClient(url=url, token=token, org=org)
    
    def __create_point(self, data):
        point = Point("noise")
        for key, value in data.items():
            point = point.tag(key,value)
        return point
    