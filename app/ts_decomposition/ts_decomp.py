import pandas as pd

from datetime import datetime

'''
TEST

Index series must be date parsable
'''

# TODO: Inherit from df, so df calls go to base?
class TsDecomp:
    # Base Dataframe
    base = None
    base_valid = None

    # Stuff to keep track of
    index = None
    # TODO: Come up with better name/system
    series = None
    
    # Dataframes for decomposition
    trend = None
    trend_valid = None

    cycle = None
    cycle_valid = None

    season = None
    season_valid = None
    
    noise = None
    noise_valid = None


    # Contructor
    def __init__(self, base, index, series=None, non_series=None):
        self.base = base

        self.index = index

        self._format_index()

        if series:
            self.series = series


    # Index stuff
    
    def _format_index(self, date_fmt_str="%Y-%m-%d %H:%M:%S"):
        # Date Format (inplace)
        self.base[self.index] = self.base[self.index].apply(lambda x: datetime.strptime(x, date_fmt_str))

        # Index and sort
        self.base.set_index(self.index)
        self.base.sort_index(inplace=True)

        return True


    # Generate Decomposition Frames

    def generate_trend_frame(self):

        pass

    def generate_cycle_frame(self):
        pass

    def generate_season_frame(self):
        pass

    def generate_noise_frame(self):
        pass


    # Train/Test/Validation Split

    def split_ts(self, percent):
        # Base
        if self.base is not None:
           self.base, self.base_valid = self._split_dataframe(percent, self.base)

        # Trend
        if self.trend is not None:
           self.trend, self.trend_valid = self._split_dataframe(percent, self.trend)

        # Cycle
        if self.cycle is not None:
            self.cycle, self.cycle_valid = self._split_dataframe(percent, self.cycle)

        # Season
        if self.season is not None:
            self.season, self.season_valid = self._split_dataframe(percent, self.season)

        # Noise
        if self.noise is not None:
            self.noise, self.noise_valid = self._split_dataframe(percent, self.noise)


    # TODO: Date or some column is getting dropped here?
    def _split_dataframe(self, percent, series):
        size = len(series.index)

        # TODO: Maybe some input validation?
        factor = (100 - percent) / 100
      
        split_index = (int)(size * factor)
        
        train, validate = series[0:split_index], series[split_index:]
        
        return train, validate


    # Generate some Classifications For Weekday/Weekend

    def day_of_week_class(self):
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
        # 0 is weekday
        def weekend_weekday(date):
            if date.weekday() == 5 or date.weekday() == 6:
                return 1
            else:
                return 0

        self.base['weekend_weekday_class'] = self.base[self.index].apply(weekend_weekday) 


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
