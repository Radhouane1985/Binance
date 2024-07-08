import requests
import pandas as pd
import numpy as np

class TradeRatios:
    #slow and fast window is to compare the pace and the significance of buy side vs. sell side activity
    def __init__(self, symbol, slow_window=1000, fast_window=100):
        self.symbol = symbol
        self.slow_window = slow_window
        self.fast_window = fast_window
        self.trade_data = []

    def fetch_recent_trades(self):
        url = f"https://fapi.binance.com/fapi/v1/trades?symbol={self.symbol}&limit=1000"
        response = requests.get(url)
        if response.status_code == 200:
            trades = response.json()
            for trade in trades:
                trade_record = {
                    'price': float(trade['price']),
                    'quantity': float(trade['qty']),
                    'side': 'buy' if not trade['isBuyerMaker'] else 'sell',
                    'timestamp': trade['time']
                }
                self.trade_data.append(trade_record)

            # Keep only the latest `slow_window` trades to limit memory usage
            self.trade_data = self.trade_data[-self.slow_window:]

    def calculate_ratios(self):
        # This function is to fetch symbol data then calculate the last trades activity (Time and Sales) 
        self.fetch_recent_trades()
        df = pd.DataFrame(self.trade_data)
        df['buy_volume'] = np.where(df['side'] == 'buy', df['quantity'], 0)
        df['sell_volume'] = np.where(df['side'] == 'sell', df['quantity'], 0)

        df['slow_buy_avg'] = df['buy_volume'].rolling(self.slow_window).mean()
        df['fast_buy_avg'] = df['buy_volume'].rolling(self.fast_window).mean()
        df['slow_sell_avg'] = df['sell_volume'].rolling(self.slow_window).mean()
        df['fast_sell_avg'] = df['sell_volume'].rolling(self.fast_window).mean()

        bullish_pressure = (df['fast_buy_avg'].iloc[-1] > df['slow_buy_avg'].iloc[-1]) and (df['fast_buy_avg'].iloc[-1] > df['fast_sell_avg'].iloc[-1])
        bearish_pressure = (df['fast_sell_avg'].iloc[-1] > df['slow_sell_avg'].iloc[-1]) and (df['fast_sell_avg'].iloc[-1] > df['fast_buy_avg'].iloc[-1])

        return bullish_pressure, bearish_pressure
