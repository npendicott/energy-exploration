from datetime import datetime
import pandas
from pandas import DataFrame, Series

from influxdb import InfluxDBClient

'''
This means we will probably want some query object. Hopefully there is json/yml like query in influxdb

TEST: the values/columns unpack
'''


# TODO: Bring in from an ENV file!! Dynamics configs for Docker
# ENERGY_DB_HOST = 'localhost'
ENERGY_DB_HOST = 'influx'
ENERGY_DB_PORT = '8086'

ENERGY_DB_USER = 'root'
ENERGY_DB_PASSWORD = 'root'

ENERGY_DB_ENERGY_DATABASE = 'energydb'

ENERGY_DB_INDEX = 'time'


# TODO: validate connaction on init
class EnergyConnection:
    """A class for connecting to InfluxDB, with a specific energy readings schema"""

    client = None

    def __init__(self):
        self.client = InfluxDBClient(
            ENERGY_DB_HOST,
            ENERGY_DB_PORT,
            ENERGY_DB_USER,
            ENERGY_DB_PASSWORD,
            ENERGY_DB_ENERGY_DATABASE

        )

        # TODO: Test client?

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
        dataframe = self.format_index(dataframe, ENERGY_DB_INDEX)

        # https://pandas.pydata.org/pandas-docs/stable/merging.html
        if append_frame is not None:
            # dataframe = pandas.concat([dataframe, input_frame], axis=1, join='inner', join_axes=[input_frame.index])
            dataframe = pandas.merge(append_frame, dataframe, on=['time', 'time'])
        # print(dataframe)

        return dataframe

