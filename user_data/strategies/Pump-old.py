# --- Do not remove these libs ---
# from freqtrade.strategy import IStrategy
from freqtrade.strategy import (BooleanParameter, CategoricalParameter, DecimalParameter,IStrategy, IntParameter)
from pandas import DataFrame
import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib
from functools import reduce


# --------------------------------


class PumpOld(IStrategy):
    """

    author@: Gert Wohlgemuth

    converted from:

    https://github.com/sthewissen/Mynt/blob/master/src/Mynt.Core/Strategies/BbandRsi.cs

    """

    INTERFACE_VERSION: int = 3
    # Minimal ROI designed for the strategy.
    # adjust based on market conditions. We would recommend to keep it low for quick turn arounds
    # This attribute will be overridden if the config file contains "minimal_roi"
    minimal_roi = {
        "0": 0.05
    }

    # minimal_roi = {
    #     "40": 0.0,
    #     "30": 0.01,
    #     "20": 0.02,
    #     "0": 0.04
    # }

    # Optimal stoploss designed for the strategy
    stoploss = -0.10

    # Optimal timeframe for the strategy
    timeframe = '3m'

    buy_rsi = IntParameter(5, 30, default=20, space="buy")
    sell_rsi = IntParameter(70, 95, default=70, space="sell")



    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['rsi'] = ta.RSI(dataframe, timeperiod=14)

        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        conditions = []
        conditions.append((dataframe['rsi'] < self.buy_rsi.value))

        if conditions:
            print('condition')
            dataframe.loc[
                reduce(lambda x, y: x & y, conditions),
                'buy'] = 1
        return dataframe
# best sma 9 and 15
    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        conditions = []
        conditions.append((dataframe['rsi'] < self.sell_rsi.value))

        if conditions:
            dataframe.loc[
                reduce(lambda x, y: x & y, conditions),
                'sell'] = 1
        return dataframe