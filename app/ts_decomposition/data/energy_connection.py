import os
from datetime import datetime
import pandas
from pandas import DataFrame, Series

from influxdb import InfluxDBClient

'''
This means we will probably want some query object. Hopefully there is json/yml like query in influxdb

TEST: the values/columns unpack
'''


# TODO: validate connaction on init
class EnergyConnection:
    """A class for connecting to InfluxDB, with a specific energy readings schema"""

    # TODO: I probably should not even have these here anyway?
    ENERGY_DB_HOST = None
    ENERGY_DB_PORT = None
    ENERGY_DB_USER = None
    ENERGY_DB_PASSWORD = None

    # Not really ENVs I think, will deal later
    ENERGY_DB_ENERGY_DATABASE = None
    ENERGY_DB_INDEX = None

    client = None

    def __init__(self):
        # TODO: Load in ENVs during class constuction? Yes, if they change it is because they probably should
        self.ENERGY_DB_HOST = os.getenv('ENERGY_DB_HOST')
        print(self.ENERGY_DB_HOST)
        self.ENERGY_DB_PORT = os.getenv('ENERGY_DB_PORT')

        self.ENERGY_DB_USER = os.getenv('ENERGY_DB_USER')
        self.ENERGY_DB_PASSWORD = os.getenv('ENERGY_DB_PASSWORD')

        self.ENERGY_DB_ENERGY_DATABASE = os.getenv('ENERGY_DB_ENERGY_DATABASE')

        self.ENERGY_DB_INDEX = os.getenv('ENERGY_DB_INDEX')

        # TODO: could probably load ENVs straight to client?
        self.client = InfluxDBClient(
            self.ENERGY_DB_HOST,
            self.ENERGY_DB_PORT,
            self.ENERGY_DB_USER,
            self.ENERGY_DB_PASSWORD,
            self.ENERGY_DB_ENERGY_DATABASE

        )

        # TODO: Test client connection at init?

    @staticmethod
    def format_index(frame, index, date_fmt_str="%Y-%m-%dT%H:%M:%SZ"):
        frame[index] = frame[index].apply(lambda x: datetime.strptime(x, date_fmt_str))

        frame.set_index(index)
        frame.sort_index(inplace=True)

        return frame

    # TODO: form rooms to work we need to stop shoving stuff into QL

    def get_readings(self, series, elements=None):
        """Get the colum headers and values from an InfluxDB series"""

        query_fmt = "SELECT * FROM {0};".format(series)
        result = self.client.query(query_fmt)

        values = result.raw['series'][0]['values']
        columns = result.raw['series'][0]['columns']

        return columns, values
        # return result

    # TODO: Should we introduce pandas here??
    def sample_series(self, series, append_frame=None):
        """Create a pandas dataframe from specific series. Append to a given frame, if supplied."""

        columns, values = self.get_readings(series)

        dataframe = DataFrame(values, columns=columns)
        dataframe = self.format_index(dataframe, self.ENERGY_DB_INDEX)

        # https://pandas.pydata.org/pandas-docs/stable/merging.html
        if append_frame is not None:
            # dataframe = pandas.concat([dataframe, input_frame], axis=1, join='inner', join_axes=[input_frame.index])
            dataframe = pandas.merge(append_frame, dataframe, on=['time', 'time'])
        # print(dataframe)

        return dataframe

