import pandas
from pandas import Series
from datetime import datetime
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.seasonal import seasonal_decompose


'''
TEST

base:
base is df (nparray?)

Index series:
must be a datetime

Model:
model must be string


'''


# TODO: Inherit from df, so df calls go to base?
class TimeSeriesSample:
    """An object for holding time series data, for the purpose of data analysis and modeling."""

    # Base Dataframe
    # TODO: How do we deal with 'split' stuff? 'base' will be full until the split, then will only be
    #  the train set. 'base_valid' will be only be the validation set. Any transform over the full set will need to
    #  operate over the full set, but will also need to preserve the original split.
    #  possibility: with some decorator, merge the sets and save the split index, then re-split. Could just save the
    #  percent, but that seems less precise?
    base = None
    base_valid = None
    base_full = None

    index = None  # Should probably be a time index
    categorical_features = None
    # TODO: Come up with better name/system

    # TODO: Is this the best way to store?
    train_test_split_index = None

    docomposition = None  # TODO; Not sure how defined to make this schema?

    # Constructor
    # TODO: Move to validation instead of format
    def __init__(self, base, index, categorical_features=None, date_fmt_str="%Y-%m-%d %H:%M:%S"):
        # TODO: DataFrame, or NumPy Array?
        self.base = base

        # TODO: Check that index is a datetime, or try to parse it
        try:
            index_series = self.base[index]
        except KeyError:
            print("Index not found!")
            return

        # If the index is a string, parse w/ date_fmt_str TODO: Default?
        try:
            index_series = index_series.apply(lambda x: datetime.strptime(x, date_fmt_str))
        except TypeError:
            pass

        # TODO: Do we drop the "index" series?
        self.base.set_index(index_series, inplace=True)

        # # TODO: If one is null, do we try to make the compliment the other?
        # if series_features is not None and categorical_features is None:
        #     pass
        # if categorical_features is not None and series_features is None:
        #     pass
        #
        # if series_features is not None:
        #     #self.series_features = series_features
        #     pass
        if categorical_features is not None:
            self.categorical_features = categorical_features

    # Train/Test/Validation Split
    def train_test_split(self, valid_percent):
        """Splits off last valid_percent of the data to a validation set. Percent will come from last index of the
        array.
        """
        # Base
        if self.base is not None:
            self.base, self.base_valid = self._split_frame(self.base, valid_percent)

    @staticmethod
    def _split_frame(frame, percent):
        # TODO: Maybe some input validation?
        size = len(frame.index)
        factor = (100 - percent) / 100
        split_index = int(size * factor)
        train, validate = frame[0:split_index], frame[split_index:]

        return train, validate

    # Decorator funcs?? For splitting and rejoining, if necessary.
    def _rejoin(self):
        self.train_test_split_index = len(self.base)
        self.base = self.base + self.base_valid

    def _resplit(self):
        self.base, self.base_valid = self.base[:self.train_test_split_index], self.base[self.train_test_split_index:]

    # def plot_series_features(self):
    #
    #     series_plots = []
    #     for series in self.base:
    #         if series not in self.categorical_features:
    #             series_plots.append(self.base.plot(kind='line', x=self.base.index, y=series))
    #
    #     return series_plots
    #     pass
    #
    # def plot_categorical_features(self):
    #     series_plots = []
    #
    #     for series in self.base:
    #         if series in self.categorical_features:
    #             series_plots.append(self.base.plot(kind='line', x=self.base.index, y=series))
    #
    #     return series_plots

    # # Index
    # def _string_format_index(self, date_fmt_str="%Y-%m-%d %H:%M:%S"):
    #
    #     self.base[self.index] = self.base[self.index].apply(lambda x: datetime.strptime(x, date_fmt_str))
    #     self.base.set_index(self.index)
    #     self.base.sort_index(inplace=True)
    #
    #     return True

    # Diagnostics
    # TODO: All
    def stationality(self, series):
        """Print out the stationality of the series. Use multiple methods/test."""
        # ADF
        result = adfuller(self.base[series].values)

        print('ADF Statistic: %f' % result[0])
        print('p-value: %f' % result[1])
        print('Critical Values:')
        for key, value in result[4].items():
            print('\t%s: %.3f' % (key, value))

        return result

    def autocorrelation(self):
        """Check the degree of autocorrelation."""
        # TODO: Autocorr stepdown/degree. Take autocorr of resid?
        pass

    # Decomposition
    def decompose(self, series):
        period = 144  # Day
        # period = 1008 # Month

        two_side = True
        # two_side=False

        # model = 'additive'
        model = 'multiplicitive'

        result = seasonal_decompose(self.base[series].values, model=model, two_sided=two_side, freq=period)
        # Cut off the NaNa on either side, from Moving Average loss
        start_gap = period
        end_gap = len(result.resid) - period

        observed = result.observed[start_gap:end_gap]
        residual = result.resid[start_gap:end_gap]

        r_sqr = self.residual(observed, residual)

        print(r_sqr)

        return result

    @staticmethod
    def calc_r_sqr(observed, residual):
        """Calculate the r_sqr from an observed set and residual set."""
        ss_res = sum([(e * e) for e in residual])

        y_bar = sum(observed) / len(observed)
        ss_tot = sum([((y - y_bar) * (y - y_bar)) for y in observed])

        r_sqr = 1 - (ss_res / ss_tot)

        return r_sqr

    # Generate some Classifications For Weekday/Weekend
    def day_of_week_class(self):
        """Add series to dataframe for a day_of_week_class classification."""
        # # This func is for labels if needed
        # def get_day(date):
        #     day_int = date.weekday()
            
        #     day_switch = {
        #         0: "Monday",
        #         1: "Tuesday",
        #         2: "Wednesday",
        #         3: "Thursday",
        #         4: "Friday",
        #         5: "Saturday",
        #         6: "Sunday"
        #     }
        #     return day_switch.get(day_int, "Invalid day")

        # Just need datetime.weekday for #
        self.base['day_of_week_class'] = self.base[self.index].apply(datetime.weekday)

    def weekend_weekday_class(self):
        """Generate class for weekend_weekday_class. 0 is weekday."""
        def weekend_weekday(date):
            if date.weekday() == 5 or date.weekday() == 6:
                return 1
            else:
                return 0

        self.base['weekend_weekday_class'] = self.base[self.index].apply(weekend_weekday)

    # Clean
    def clean_lights(self, floor=0):
        """Add a light_on series to dataframe, indicating the lights were taking power. Add a light_cleaned with all
        zero light power values removed.
        """
        light_on_list = []
        light_cleaned_list = []

        for light_reading in self.base['light']:
            # Maybe some vals around 0?
            light_on = light_reading > floor

            if light_on:
                light_on_list.append(1)
                light_cleaned_list.append(light_reading)

            else:
                light_on_list.append(0)
                light_cleaned_list.append(None)

        light_on_series = Series(light_on_list)
        self.base['light_on'] = light_on_series

        light_cleaned_series = Series(light_cleaned_list)
        self.base['light_cleaned'] = light_cleaned_series

    # Util
    def print(self):
        # Base
        print("Base: ")
        print(self.base.describe())
        print(self.base.head())
        print(self.base.tail())
        print()

        # Base Valid
        print("Base Validation: ")
        print(self.base_valid.describe())
        print(self.base_valid[self.index])
        print()
