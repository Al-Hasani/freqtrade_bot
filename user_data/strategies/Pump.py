# --- Do not remove these libs ---
from freqtrade.strategy import IStrategy
from pandas import DataFrame
import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib


# --------------------------------


class Pump(IStrategy):
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
        "0": 0.20
    }

    # Optimal stoploss designed for the strategy
    stoploss = -0.95

    # Optimal timeframe for the strategy
    timeframe = '3m'

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['rsi'] = ta.RSI(dataframe, timeperiod=14)

        # Volume Moving Average
        dataframe['volume_9'] = ta.MA(dataframe['volume'], timeperiod=9)
        dataframe['volume_15'] = ta.MA(dataframe['volume'], timeperiod=15)
        dataframe['volume_50'] = ta.MA(dataframe['volume'], timeperiod=50)

        volume_diff = dataframe['volume_9'] - dataframe['volume_15']
        volume_av = (dataframe['volume_9'] + dataframe['volume_15']) / 2

        # print((dataframe['volume_15']/dataframe['volume_9']) * 100)
        

        dataframe['sma_9'] = ta.MA(dataframe, timeperiod=9)
        dataframe['sma_15'] = ta.MA(dataframe, timeperiod=15)

        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        
        dataframe.loc[
            (
                (dataframe['rsi'] < 45) &
                (dataframe['sma_9'] > dataframe['sma_15']) &
                ((dataframe['volume_9'].shift(1) < dataframe['volume_15'].shift(1)) | (dataframe['volume_9'].shift(2) < dataframe['volume_15'].shift(2))) &
                ((dataframe['sma_9'].shift(1) < dataframe['sma_15'].shift(1)) | (dataframe['sma_9'].shift(2) < dataframe['sma_15'].shift(2))) &
                # (dataframe['close'].shift(1) > dataframe['open'].shift(1)) & 
                (((dataframe['volume_15']/dataframe['volume_9']) * 100) > 100) &
                # (dataframe['volume'] > dataframe['volume_50'] * 2) &
                (dataframe['volume'] > 0)
            ),
            'enter_long'] = 1
        return dataframe
# Ignored exit_trend from config.json use_exit_signal
    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                (dataframe['rsi'] > 80) &
                (dataframe['sma_9'] < dataframe['sma_15']) &
                (dataframe['volume'] > 0)
            ),
            'exit_long'] = 1
        return dataframe