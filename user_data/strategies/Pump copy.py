# --- Do not remove these libs ---
# from freqtrade.strategy import IStrategy
from freqtrade.strategy import (IntParameter, IStrategy, CategoricalParameter, BooleanParameter)
from pandas import DataFrame
import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib


# --------------------------------


class Pumpo(IStrategy):
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
        "0": 0.08
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
    sell_rsi = IntParameter(70, 95, default=20, space="buy")



    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['rsi'] = ta.RSI(dataframe)

        # Volume Moving Average
        dataframe['volume_9'] = ta.MA(dataframe['volume'], timeperiod=9)
        dataframe['volume_200'] = ta.MA(dataframe['volume'], timeperiod=200)

        # volume_diff = dataframe['volume_9'] - dataframe['volume_15']
        # volume_av = (dataframe['volume_9'] + dataframe['volume_15']) / 2

        # print((dataframe['volume_15']/dataframe['volume_9']) * 100)
        

        dataframe['ma_9'] = ta.EMA(dataframe, timeperiod=9)
        dataframe['ma_50'] = ta.EMA(dataframe, timeperiod=50)



        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        
        dataframe.loc[
            (
                (dataframe['rsi'] > 50) &
                (dataframe['ma_9'] > dataframe['ma_50']) &
                # (dataframe['volume_9'].shift(1) < dataframe['volume_15'].shift(1)) &
                # (dataframe['volume_9'] > dataframe['volume_15']) &
                # (((dataframe['volume_15']/dataframe['volume_9']) * 100) > 50) &
                (dataframe['volume'] > (dataframe['volume_200'] * 15)) &
                (dataframe['volume'] > 0)
            ),
            'enter_long'] = 1
        return dataframe
# best sma 9 and 15
    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                (dataframe['rsi'] > 80) &
                # (dataframe['volume'] < (dataframe['volume'].shift(1) / 1.5)) &
                # (dataframe['ma_9'].shift(1) > dataframe['ma_50'].shift(1)) &
                # (dataframe['ma_9'] < dataframe['ma_50']) &
                # (dataframe['volume'] < (dataframe['volume_200'] * 10)) &
                (dataframe['volume'] > 0)
            ),
            'exit_long'] = 1
        return dataframe