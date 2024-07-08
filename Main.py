import time
from DataCollector import DataCollector
from CorrelationHunter import CorrelationHunter
from RiskManager import RiskManager
from StrategyBuilder import StrategyBuilder
from TradeRatios import TradeRatios
from StrategyConfig import StrategyConfig

class Main:
    def __init__(self, symbols):
        self.symbols = symbols
        self.data_collector = DataCollector()
        self.correlation_hunter = CorrelationHunter(symbols, self.data_collector)
        self.risk_manager = RiskManager()
        self.strategy_builders = {}
        self.trade_ratios = {}

    def setup(self):
        # Fetch initial data
        data = self.data_collector.fetch_data(self.symbols)

        # Rank pairs based on correlation
        top_pairs = self.correlation_hunter.rank_pairs()
        print(top_pairs)

        # Set up strategy builders and TradeRatios instances
        for pair in top_pairs:
            symbol1, symbol2 = pair[1]
            symbol1_data = data[symbol1]
            symbol2_data = data[symbol2]
            
            self.strategy_builders[(symbol1, symbol2)] = StrategyBuilder(symbol1_data, symbol2_data)
            self.strategy_builders[(symbol1, symbol2)].calculate_spread()
            self.strategy_builders[(symbol1, symbol2)].set_bands()

            self.trade_ratios[symbol1] = TradeRatios(symbol1)
            self.trade_ratios[symbol2] = TradeRatios(symbol2)

    def run(self):
        while True:
            try:
                self.setup()
                for pair, builder in self.strategy_builders.items():
                    symbol1, symbol2 = pair
                    #print('-' * 50)
                    #print(f'Pair : {pair}')

                    # Check for Signals
                    entry_signal = builder.check_entry_signal()
                    if entry_signal and self.risk_manager.get_position(f"{symbol1}-{symbol2}") is None:
                        bullish_pressure1, bearish_pressure1 = self.trade_ratios[symbol1].calculate_ratios()
                        bullish_pressure2, bearish_pressure2 = self.trade_ratios[symbol2].calculate_ratios()
                        
                        # If Short spread Signal (short symbol1 and long symbol2) 
                        # and if there is a bearish pressure in symbol1 and not bearish pressure in symbol2 in Time&Sales
                        # ---> Short the Spread
                        if entry_signal == "Short Spread" and bearish_pressure1 and not bearish_pressure2:
                            print(f"Execute Short Spread on {symbol1}-{symbol2}")
                            self.risk_manager.manage_positions(f"{symbol1}-{symbol2}", 'short')
                        
                        # If Long spread Signal (long symbol1 and short symbol2) 
                        # and if there is a bullish pressure in symbol1 and not bullish pressure in symbol2 in Time&Sales
                        # ---> Long the Spread
                        elif entry_signal == "Buy Spread" and bullish_pressure1 and not bullish_pressure2:
                            print(f"Execute Buy Spread on {symbol1}-{symbol2}")
                            self.risk_manager.manage_positions(f"{symbol1}-{symbol2}", 'long')
                    
                    # Check for Exit Signals
                    exit_signal = builder.check_exit_signal()
                    if exit_signal and self.risk_manager.get_position(f"{symbol1}-{symbol2}") is not None:
                        print(f"Close Position on {symbol1}-{symbol2}")
                        self.risk_manager.manage_positions(f"{symbol1}-{symbol2}", None)
            except Exception as e:
                print(e)

            time.sleep(2)

if __name__ == "__main__":
    symbols = StrategyConfig.symbols
    main = Main(symbols)
    main.run()
