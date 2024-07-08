import pandas as pd
import requests

class DataCollector:
    def __init__(self, interval='1m', limit=1000):
        self.interval = interval
        self.limit = limit
        self.base_url = "https://fapi.binance.com/fapi/v1/klines"

    def fetch_historical_data(self, symbol):
        url = f"{self.base_url}?symbol={symbol}&interval={self.interval}&limit={self.limit}"
        response = requests.get(url)
        data = response.json()
        df = pd.DataFrame(data, columns=[
            'timestamp', 'open', 'high', 'low', 'close', 'volume',
            'close_time', 'quote_asset_volume', 'number_of_trades',
            'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
        ])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)
        df['close'] = df['close'].astype(float)
        df['volume'] = df['volume'].astype(float)
        return df

    def fetch_data(self, symbols):
        data = {}
        for symbol in symbols:
            data[symbol] = self.fetch_historical_data(symbol)
        return data
