# indicators.py

import pandas as pd  # Добавьте эту строку в начало файла

class Indicators:
    @staticmethod
    def calculate_ema(df, span):
        return df['close'].ewm(span=span, adjust=False).mean()

    @staticmethod
    def calculate_rsi(df, period=14):
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))

    @staticmethod
    def calculate_macd(df):
        """
        Вычисляет MACD Line, Signal Line и Histogram.

        Возвращает:
        macd_line, signal_line, macd_histogram
        """
        short_ema = df['close'].ewm(span=12, adjust=False).mean()
        long_ema = df['close'].ewm(span=26, adjust=False).mean()
        macd_line = short_ema - long_ema
        signal_line = macd_line.ewm(span=9, adjust=False).mean()
        macd_histogram = macd_line - signal_line
        return macd_line, signal_line, macd_histogram

    @staticmethod
    def calculate_adx(df, period=14):
        delta_high = df['high'].diff()
        delta_low = df['low'].diff()
        plus_dm = ((delta_high > delta_low) & (delta_high > 0)) * delta_high
        minus_dm = ((delta_low > delta_high) & (delta_low > 0)) * delta_low
        tr = pd.concat([
            df['high'] - df['low'],
            abs(df['high'] - df['close'].shift()),
            abs(df['low'] - df['close'].shift())
        ], axis=1).max(axis=1)
        atr = tr.rolling(window=period).mean()
        plus_di = 100 * (plus_dm.rolling(window=period).mean() / atr)
        minus_di = 100 * (minus_dm.rolling(window=period).mean() / atr)
        dx = (abs(plus_di - minus_di) / (plus_di + minus_di)) * 100
        adx = dx.rolling(window=period).mean()
        return adx


    @staticmethod
    def calculate_bollinger_bands(df, window=20):
        """
        Вычисляет верхнюю, среднюю и нижнюю линии Боллинджера.

        Параметры:
        df (DataFrame): Данные исторических цен.
        window (int): Период скользящей средней.

        Возвращает:
        tuple: upper_band, middle_band, lower_band
        """
        middle_band = df['close'].rolling(window=window).mean()
        std_dev = df['close'].rolling(window=window).std()
        upper_band = middle_band + (std_dev * 2)
        lower_band = middle_band - (std_dev * 2)
        return upper_band, middle_band, lower_band
