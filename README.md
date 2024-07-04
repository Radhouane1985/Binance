# OrderBookPatterns Class

The `OrderBookPatterns` class monitors trading patterns and identifies significant trades on Binance using WebSocket. It calculates order speeds, interprets market movements, tracks big trades, and identifies support and resistance levels.

## Methods

### `__init__(symbol, long_term_window_size, short_term_window_size, min_trade_volume)`

- **Description**: Initializes the `OrderBookPatterns` object with essential parameters.
- **Parameters**:
  - `symbol`: Symbol for the trading pair (e.g., "btcusdt").
  - `long_term_window_size`: Size of the long-term window for storing trade timestamps.
  - `short_term_window_size`: Size of the short-term window for storing trade timestamps.
  - `min_trade_volume`: Minimum volume threshold for considering a trade as big.

### `start()`

- **Description**: Starts the WebSocket connection to Binance's WebSocket server to receive trade data.
- **Usage**: Call this method after initializing an `OrderBookPatterns` object to begin monitoring trades.

### `on_message(ws, message)`

- **Description**: Callback function called whenever a new trade message (`aggTrade`) is received.
- **Parameters**:
  - `ws`: WebSocket object.
  - `message`: Message received from WebSocket.
- **Usage**: Processes the incoming trade data and updates internal data structures.

### `get_order_speeds()`

- **Description**: Calculates the order speeds for both buy and sell orders in both short-term and long-term windows.
- **Returns**: Four floats representing long-term buy speed, short-term buy speed, long-term sell speed, and short-term sell speed.

### `interpret_speeds(long_term_speed, short_term_speed)`

- **Description**: Interprets the order speed data to determine market acceleration or deceleration.
- **Parameters**:
  - `long_term_speed`: Long-term order speed (buy or sell).
  - `short_term_speed`: Short-term order speed (buy or sell).
- **Returns**: String indicating "acceleration" or "deceleration" based on the comparison between short-term and long-term speeds.

### `get_big_trades()`

- **Description**: Retrieves the most recent big buy and sell trades.
- **Returns**: Two deques containing tuples of trade information (timestamp, price, volume) for big buy and sell trades.

### `track_support_and_resistance(price, trade_type)`

- **Description**: Tracks support and resistance levels based on significant trades.
- **Parameters**:
  - `price`: Price of the trade.
  - `trade_type`: Type of the trade ('buy' or 'sell').
- **Usage**: Internal method called from `process_trade` to update support and resistance levels.

### `get_support_and_resistance_levels()`

- **Description**: Retrieves the current support and resistance levels identified by the class.
- **Returns**: Two lists containing support and resistance prices respectively.

### `on_error(ws, error, exception=None)`

- **Description**: Error handling function called on WebSocket errors.
- **Parameters**:
  - `ws`: WebSocket object.
  - `error`: Error message.
  - `exception`: Optional exception object.
- **Usage**: Prints the error message to the console.

### `on_close(ws, close_status_code, close_msg)`

- **Description**: Callback function called when the WebSocket connection is closed.
- **Parameters**:
  - `ws`: WebSocket object.
  - `close_status_code`: Status code indicating the reason for closure.
  - `close_msg`: Message indicating the reason for closure.
- **Usage**: Prints a message indicating WebSocket closure.
