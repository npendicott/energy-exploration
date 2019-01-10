# Webserver
from flask import Flask
import os
import socket

# Data
from ts_decomposition.data.energy_connection import EnergyConnection

# Model
#import ts_decomposition
from ts_decomposition.model.series_sample import TimeSeriesSample

# Copypasta from TS main 
from datetime import datetime
import pandas as pd

app = Flask(__name__)

energy_connection = EnergyConnection()

# Routes 
# TODO: Break out
# TODO: Get rid of the new "main" debug hax
@app.route("/")
def root():
    html = "<h3>{name}</h3>" \
           "<b>Hostname:</b> {hostname}<br/>"
    return html.format(name=os.getenv("NAME", "world"), hostname=socket.gethostname())

@app.route("/test")
def test_route():
    series = [
        'appliance',
        'humidity',
        'tempurature',
        'tdewpoint',
        'pressure'
    ]

    sample_frame = energy_connection.sample_series('energy_readings')
    # TODO: Rooms/QL Extract

    sample_frame = energy_connection.sample_series('external_readings', append_frame=sample_frame)

    sample = TimeSeriesSample(sample_frame, 'time')

    # TODO: Figure out what needs to be moved to constructor
    sample.train_test_split(20)  # Make sure everything can be done AFTER split

    print(sample.base.index)

    sample.clean_lights()
    
    result = sample.stationality('appliance')

    html = "<h3>{name}</h3>" \
           "<b>{result}<br/>" \
           "Hey!"
    return html.format(name=os.getenv("NAME", "world"), result=result)

# Run the server
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8789)
