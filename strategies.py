import pandas as pd
from indicators import Indicators  # Add this import

class Strategies:
    def __init__(self):
        self.indicators = Indicators()

    def prepare_dataframe(self, historical_data):
        df = pd.DataFrame(historical_data)
        df.columns = ["timestamp", "open", "high", "low", "close", "volume", "turnover"]
        df['close'] = df['close'].astype(float)
        df['high'] = df['high'].astype(float)
        df['low'] = df['low'].astype(float)
        df.sort_values('timestamp', inplace=True)
        return df

    def determine_trend(self, df):
        """
        Determines the position direction ('long', 'short', or None) based on the trend and MACD value.

        Parameters:
        df (DataFrame): Historical price data.

        Returns:
        str: 'long', 'short', or None.
        """

        # Calculate indicators
        df['EMA_12'] = self.indicators.calculate_ema(df, span=12)
        df['EMA_26'] = self.indicators.calculate_ema(df, span=26)
        df['RSI'] = self.indicators.calculate_rsi(df, period=14)
        macd_line, signal_line, macd_histogram = self.indicators.calculate_macd(df)
        df['MACD_Line'] = macd_line
        df['MACD_Signal'] = signal_line
        df['MACD_Histogram'] = macd_histogram
        df['ADX'] = self.indicators.calculate_adx(df)

        # df['EMA_200'] = self.indicators.calculate_ema(df, span=200)
        df['EMA_70'] = self.indicators.calculate_ema(df, span=70)
        df['Bollinger_upper'], df['Bollinger_middle'], df['Bollinger_lower'] = self.indicators.calculate_bollinger_bands(df)

        # Remove rows with missing values
        df.dropna(inplace=True)

        if df.empty:
            print("Not enough data after calculating indicators.")
            return None

        # Get the latest indicator values
        latest = df.iloc[-1]
        previous = df.iloc[-2]
        pre_previous = df.iloc[-3]

        trade_decision = None

        # Determine trend based on Bollinger Bands middle and EMA 70
        if latest['Bollinger_middle'] > latest['EMA_70'] and latest['MACD_Histogram'] <= -15 and previous['MACD_Histogram'] < latest['MACD_Histogram']:
            trade_decision = 'long'
        elif latest['Bollinger_middle'] < latest['EMA_70'] and latest['MACD_Histogram'] >= 15 and previous['MACD_Histogram'] > latest['MACD_Histogram']:
            trade_decision = 'short'
        else:
            trade_decision = None

        # Output the indicator values and trend
        print(f"EMA_12: {latest['EMA_12']:.2f}")
        print(f"EMA_26: {latest['EMA_26']:.2f}")
        print(f"RSI: {latest['RSI']:.2f}")
        print(f"MACD Line: {latest['MACD_Line']:.2f}")
        print(f"MACD Signal: {latest['MACD_Signal']:.2f}")
        print(f"MACD Histogram: {latest['MACD_Histogram']:.2f}")

        print(f"latest['Bollinger_middle'] > latest['EMA_70']: {latest['Bollinger_middle'] > latest['EMA_70']}")
        print(f"latest['Bollinger_middle'] < latest['EMA_70']: {latest['Bollinger_middle'] < latest['EMA_70']}")

        print(f"latest['MACD_Histogram'] <= -15: {latest['MACD_Histogram'] <= -15}")
        print(f"latest['MACD_Histogram'] >= 15: {latest['MACD_Histogram'] >= 15}")

        print(f"previous['MACD_Histogram'] < latest['MACD_Histogram']: {previous['MACD_Histogram'] < latest['MACD_Histogram']}")
        print(f"previous['MACD_Histogram'] > latest['MACD_Histogram']: {previous['MACD_Histogram'] > latest['MACD_Histogram']}")

        print(f"ADX: {latest['ADX']:.2f}")
        print(f"EMA_70: {latest['EMA_70']:.2f}")
        print(f"Bollinger_middle: {latest['Bollinger_middle']:.2f}")

        print(f"Determined trend: {trade_decision}")

        if trade_decision:
            print(f"Trade decision: Open {trade_decision.upper()} position")
        else:
            print("Trade decision: Do not open a position")

        return trade_decision
