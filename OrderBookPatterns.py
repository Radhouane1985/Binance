import websocket
import json
import time
from collections import deque
from threading import Thread

class OrderBookPatterns:
    def __init__(self, symbol, long_term_window_size, short_term_window_size, min_trade_volume):
        self.symbol = symbol.lower()
        self.long_term_window_size = long_term_window_size
        self.short_term_window_size = short_term_window_size
        self.min_trade_volume = min_trade_volume
        self.long_term_buy_trades = deque(maxlen=long_term_window_size)
        self.short_term_buy_trades = deque(maxlen=short_term_window_size)
        self.long_term_sell_trades = deque(maxlen=long_term_window_size)
        self.short_term_sell_trades = deque(maxlen=short_term_window_size)
        self.big_buy_trades = deque(maxlen=5)
        self.big_sell_trades = deque(maxlen=5)
        self.support_levels = deque(maxlen=5)
        self.resistance_levels = deque(maxlen=5)
        self.start_time = time.time()

    def on_message(self, ws, message):
        data = json.loads(message)
        if data['e'] == 'aggTrade':
            self.process_trade(data)

    def process_trade(self, data):
        trade_time = data['T'] / 1000.0  # Binance sends timestamps in milliseconds
        trade_volume = float(data['q'])  # Trade volume
        trade_price = float(data['p'])
        if data['m']:  # m is True for a sell (market maker) trade, False for a buy (market taker) trade
            self.long_term_sell_trades.append(trade_time)
            self.short_term_sell_trades.append(trade_time)
            if trade_volume >= self.min_trade_volume:
                self.big_sell_trades.append((trade_time, trade_price, trade_volume))
                self.track_support_and_resistance(trade_price, 'sell')
        else:
            self.long_term_buy_trades.append(trade_time)
            self.short_term_buy_trades.append(trade_time)
            if trade_volume >= self.min_trade_volume:
                self.big_buy_trades.append((trade_time, trade_price, trade_volume))
                self.track_support_and_resistance(trade_price, 'buy')


    def calculate_order_speed(self, trades):
        if len(trades) < 2:
            return 0  # Not enough trades to calculate speed
        time_span = trades[-1] - trades[0]
        speed = time_span / len(trades)
        return speed

    def get_order_speeds(self):
        long_term_buy_speed = self.calculate_order_speed(self.long_term_buy_trades)
        short_term_buy_speed = self.calculate_order_speed(self.short_term_buy_trades)
        long_term_sell_speed = self.calculate_order_speed(self.long_term_sell_trades)
        short_term_sell_speed = self.calculate_order_speed(self.short_term_sell_trades)
        return long_term_buy_speed, short_term_buy_speed, long_term_sell_speed, short_term_sell_speed

    def interpret_speeds(self, long_term_speed, short_term_speed):
        if short_term_speed < long_term_speed:
            return "acceleration"
        else:
            return "deceleration"

    def get_big_trades(self):
        return self.big_buy_trades, self.big_sell_trades

    def track_support_and_resistance(self, price, trade_type):
        if trade_type == 'sell':
            # Check for support level
            if all(price > self.long_term_sell_trades[-1] for _ in range(len(self.long_term_sell_trades))):
                self.support_levels.append(price)
        elif trade_type == 'buy':
            # Check for resistance level
            if all(price < self.long_term_buy_trades[-1] for _ in range(len(self.long_term_buy_trades))):
                self.resistance_levels.append(price)


    def get_support_and_resistance_levels(self):
        return list(self.support_levels), list(self.resistance_levels)

    def on_error(self, ws, error, exception=None):
        print(f"Error: {error}")

    def on_close(self, ws, close_status_code, close_msg):
        print("WebSocket closed")

    def start(self):
        self.ws = websocket.WebSocketApp(
            f"wss://fstream.binance.com/ws/{self.symbol}@aggTrade",
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close
        )
        self.ws_thread = Thread(target=self.ws.run_forever)
        self.ws_thread.start()

if __name__ == "__main__":
    symbol = "btcusdt"
    long_term_window_size = 1000
    short_term_window_size = 100
    min_trade_volume = 10  # Minimum volume to consider as a big trade

    order_book_patterns = OrderBookPatterns(symbol, long_term_window_size, short_term_window_size, min_trade_volume)
    order_book_patterns.start()

    # Example of accessing calculated order speeds, big trades, and support/resistance levels periodically
    while True:
        time.sleep(1)
        long_term_buy_speed, short_term_buy_speed, long_term_sell_speed, short_term_sell_speed = order_book_patterns.get_order_speeds()
        
        buy_interpretation = order_book_patterns.interpret_speeds(long_term_buy_speed, short_term_buy_speed)
        sell_interpretation = order_book_patterns.interpret_speeds(long_term_sell_speed, short_term_sell_speed)
        
        print("Buy Orders Speed Interpretation:", buy_interpretation)
        print("Sell Orders Speed Interpretation:", sell_interpretation)
        
        big_buy_trades, big_sell_trades = order_book_patterns.get_big_trades()
        print("Big Buy Trades:", big_buy_trades)
        print("Big Sell Trades:", big_sell_trades)
        
        support_levels, resistance_levels = order_book_patterns.get_support_and_resistance_levels()
        print("Support Levels:", support_levels)
        print("Resistance Levels:", resistance_levels)
        
        print('-'*50)
