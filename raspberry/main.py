from Datasender import Datasender

'''
Requirement: InfluxDB client.
Install using: pip install influxdb-client
'''

if __name__ == "__main__":
    data = {
        "location" : "Rosenheim", #put the location of your device
        "latitude" : 47.87006109706558, #put the latitude of your current device (can also check on google maps)
        "longitude" : 12.108124191410772 #put the longitude of your current device (can also check on google maps)
    }
    
    datasender = Datasender(data).start(10.0)
