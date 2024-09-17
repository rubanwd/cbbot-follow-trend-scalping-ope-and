import pandas as pd
from indicators import Indicators  # Добавьте этот импорт

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
        Определяет направление позиции ('long', 'short' или None) на основе тренда и значения MACD.

        Параметры:
        df (DataFrame): Данные исторических цен.

        Возвращает:
        str: 'long', 'short' или None.
        """

        # Вычисляем индикаторы
        df['EMA_12'] = self.indicators.calculate_ema(df, span=12)
        df['EMA_26'] = self.indicators.calculate_ema(df, span=26)
        df['RSI'] = self.indicators.calculate_rsi(df, period=14)
        macd_line, signal_line, macd_histogram = self.indicators.calculate_macd(df)
        df['MACD_Line'] = macd_line
        df['MACD_Signal'] = signal_line
        df['MACD_Histogram'] = macd_histogram
        df['ADX'] = self.indicators.calculate_adx(df)

        # Удаляем строки с отсутствующими значениями
        df.dropna(inplace=True)

        if df.empty:
            print("Недостаточно данных после вычисления индикаторов.")
            return None

        # Получаем последние значения индикаторов
        latest = df.iloc[-1]

        # Логика определения тренда
        bullish_signals = 0
        bearish_signals = 0

        # EMA пересечения
        if latest['EMA_12'] > latest['EMA_26']:
            bullish_signals += 1
        else:
            bearish_signals += 1

        # MACD пересечение с сигнальной линией
        if latest['MACD_Line'] > latest['MACD_Signal']:
            bullish_signals += 1
        else:
            bearish_signals += 1

        # RSI уровни
        if latest['RSI'] > 60:
            bullish_signals += 1
        elif latest['RSI'] < 40:
            bearish_signals += 1

        # ADX для определения силы тренда
        if latest['ADX'] < 20:
            trend = "Консолидация"
        else:
            if bullish_signals > bearish_signals:
                trend = "Бычий тренд"
            elif bearish_signals > bullish_signals:
                trend = "Медвежий тренд"
            else:
                trend = "Консолидация"

        # Дополнительная логика на основе значения MACD Line
        trade_decision = None
        macd_hist_value = latest['MACD_Histogram']

        if trend == "Медвежий тренд" and macd_hist_value >= 15:
            trade_decision = 'short'
        elif trend == "Бычий тренд" and macd_hist_value <= -15:
            trade_decision = 'long'

        # Выводим значения индикаторов и тренд
        print(f"EMA_12: {latest['EMA_12']:.2f}")
        print(f"EMA_26: {latest['EMA_26']:.2f}")
        print(f"RSI: {latest['RSI']:.2f}")
        print(f"MACD Line: {latest['MACD_Line']:.2f}")  # Первое значение MACD
        print(f"MACD Signal: {latest['MACD_Signal']:.2f}")
        print(f"MACD Histogram: {latest['MACD_Histogram']:.2f}")
        print(f"ADX: {latest['ADX']:.2f}")
        print(f"Определенный тренд: {trend}")

        if trade_decision:
            print(f"Торговое решение: Открыть позицию {trade_decision.upper()}")
        else:
            print("Торговое решение: Не открывать позицию")

        return trade_decision
