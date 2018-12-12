import os
from datetime import datetime

import pandas as pd

from data.energy_connection import EnergyConnection
from ts_decomp import TsDecomp 

def load_data(file_name, data_path=".."):
    csv_path = os.path.join(data_path, file_name)
    return pd.read_csv(csv_path)

if __name__ == "__main__":
    # Load the dataframe
    energy_data = load_data("energydata_complete.csv", data_path="../../data")

    # Influx
    # energy_connection = EnergyConnection()
    # energy_connection.print_energy_readings()

    # Put it in the TS object
    ts_decomp = TsDecomp(energy_data, 'date')

    # Decomp
    ts_decomp.day_of_week_class()
    ts_decomp.weekend_weekday_class()

    ts_decomp.split_ts(20)

    ts_decomp.print()