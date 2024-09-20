
# risk_management.py

import pandas as pd

from helpers import Helpers  # Add this import
from indicators import Indicators

class RiskManagement:
    def __init__(self, atr_period=14, atr_multiplier=1.5, risk_ratio=1.5):
        self.atr_period = atr_period
        self.atr_multiplier = atr_multiplier
        self.risk_ratio = risk_ratio
        self.indicators = Indicators()

    def calculate_atr(self, df):
        high = df['high'].astype(float)
        low = df['low'].astype(float)
        close = df['close'].astype(float)
        df['previous_close'] = close.shift(1)
        df['tr'] = pd.concat([high - low, (high - df['previous_close']).abs(), (low - df['previous_close']).abs()], axis=1).max(axis=1)
        atr = df['tr'].rolling(window=self.atr_period).mean().iloc[-1]
        return atr

    def calculate_dynamic_risk_management(self, df, trend):
        rsi, bollinger_upper, bollinger_middle, bollinger_lower, current_price = Helpers.calculate_and_print_indicators(df, self.indicators)
        atr = self.calculate_atr(df)
        original_stop_loss_distance = self.atr_multiplier * atr
        stop_loss_distance = original_stop_loss_distance * 10  # Increase stop loss distance by 4 times
        # stop_loss_distance = original_stop_loss_distance

        # Calculate take profit using the original stop loss distance
        take_profit_distance = original_stop_loss_distance * self.risk_ratio

        if trend == 'long':
            stop_loss = float(current_price) - stop_loss_distance
            take_profit = float(current_price) + take_profit_distance
        elif trend == 'short':
            stop_loss = float(current_price) + stop_loss_distance
            take_profit = float(current_price) - take_profit_distance
        else:
            raise ValueError("Trend must be either 'long' or 'short'")

        return stop_loss, take_profit


