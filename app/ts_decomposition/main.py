import os
from datetime import datetime
import pandas as pd

from data.energy_connection import EnergyConnection
from model.series_sample import TimeSeriesSample

series = [
    'appliance',
    'humidity',
    'tempurature',
    'tdewpoint',
    'pressure'
]

def load_data(file_name, data_path=".."):
    csv_path = os.path.join(data_path, file_name)
    return pd.read_csv(csv_path)


if __name__ == "__main__":
    # sample_data = load_data("energydata_complete.csv", data_path="../../data")

    # Influx
    energy_connection = EnergyConnection()

    sample_frame = energy_connection.sample_series('energy_readings')
    # TODO: Rooms/QL Extract
    sample_frame = energy_connection.sample_series('external_readings', append_frame=sample_frame)

    sample = TimeSeriesSample(sample_frame, index='time', series=series)

    # TODO: Figure out what needs to be moved to constructor
    sample.split_ts(20) # Make sure everything can be done AFTER split

    sample.day_of_week_class()
    sample.weekend_weekday_class()
    sample.clean_lights()

    for s in series:
        sample.stationality(s)

    sample.decompose('appliance')

