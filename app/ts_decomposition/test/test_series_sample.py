import unittest

from model import series_sample
from model.series_sample import TimeSeriesSample

# TODO: Is this bad? To have to import the test_target's dependencies?
import pandas
from datetime import datetime


class TestSeriesSample(unittest.TestCase):

    def test_init_index_key(self):
        # TODO: Setup?
        test_frame = pandas.read_csv('./data/test_data.csv')

        self.assertRaises(KeyError, TimeSeriesSample, test_frame, 'bad_key')

    def test_index_datetime_unparsable(self):
        test_frame = pandas.read_csv('./data/test_data.csv')

        self.assertRaises(TypeError, TimeSeriesSample, test_frame, 'good_key')

    def test_default_index_datetime_parse(self):
        test_frame = pandas.read_csv('./data/test_data.csv')
        sample = TimeSeriesSample(test_frame, 'datetime')

        first_index = sample.base.index[0]

        self.assertIsInstance(first_index, datetime)

    def test_train_test_split_result_size(self):
        test_frame = pandas.read_csv('./data/test_data.csv')
        sample = TimeSeriesSample(test_frame, 'datetime')

        sample.train_test_split(0.2)

        self.assertEqual(len(sample.base), 8)
        # size = len(frame.index)
        # factor = (100 - percent) / 100
        # split_index = int(size * factor)
        # train, validate = frame[0:split_index], frame[split_index:]
        #
        # return train, validate



# if __name__ == '__main__':
#     dataframe = pandas.read_csv('./data/test_data.csv')
#     decomp = series_sample.TimeSeriesSample(dataframe, 'testing')
#     print(dataframe.head())

