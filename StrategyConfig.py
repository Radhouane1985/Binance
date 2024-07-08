class StrategyConfig:
    # Binance Futures API Keys (fapi)
    API_KEY = 'your_binance_fapi_key'
    API_SECRET = 'your_binance_fapi_secret'

    # Trading Symbols, we can add way more symbols to track
    symbols = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'ADAUSDT', 'XRPUSDT', 'BCHUSDT', 'LTCUSDT', 'TRXUSDT', 'DASHUSDT']

    # Other Strategy Parameters
    # Add any other parameters specific to your strategy here