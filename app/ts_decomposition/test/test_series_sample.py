import unittest

from model import series_sample
# TODO: Is this bad?
import pandas


class TestTsDecomp(unittest.TestCase):

    def test_init_index(self):
        dataframe = pandas.read_csv('./data/test_data.csv')
        decomp = series_sample.TimeSeriesSample(dataframe, 'test')
        print(dataframe.head())


        self.assertIsInstance(decomp, series_sample.TimeSeriesSample)


if __name__ == '__main__':
    dataframe = pandas.read_csv('./data/test_data.csv')
    decomp = series_sample.TimeSeriesSample(dataframe, 'testing')
    print(dataframe.head())

    # unittest.main()
