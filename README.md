# Statistical Arbitrage Strategy

This repository contains a Python-based statistical arbitrage strategy designed for trading on Binance Futures. The strategy employs quantitative methods to identify and exploit pricing inefficiencies between pairs of cryptocurrencies.

## Strategy Components

1. **StrategyConfig**
   - **Purpose:** Provides configuration parameters such as API keys, trading symbols, risk management settings, and other strategy-specific constants.
   - **Usage:** Accesses configuration parameters through class methods for consistency across the strategy modules.

2. **DataCollector**
   - **Purpose:** Fetches historical price data for specified trading symbols from Binance using their API.
   - **Usage:** Collects and prepares data for correlation analysis and strategy building.

3. **CorrelationHunter**
   - **Purpose:** Identifies highly correlated pairs of cryptocurrencies based on historical price data.
   - **Usage:** Calculates correlation coefficients and filters pairs that meet specified criteria for trading.

4. **StrategyBuilder**
   - **Purpose:** Constructs trading signals based on statistical models (e.g., OLS regression) applied to pairs of correlated cryptocurrencies.
   - **Usage:** Calculates spreads, z-scores, and other statistical indicators to determine entry and exit points for trades.

5. **TradeRatios**
   - **Purpose:** Monitors recent trade volumes and ratios on Binance Futures to gauge market sentiment and adjust trading decisions.
   - **Usage:** Calculates buy/sell trade ratios and adapts trading strategies based on market activity.

6. **RiskManager**
   - **Purpose:** Implements risk management protocols to control position sizing, set stop losses, and manage overall portfolio risk.
   - **Usage:** Ensures trades adhere to predefined risk limits and adjusts position sizes dynamically based on market conditions.

7. **Main**
   - **Purpose:** Coordinates the execution of the strategy by initializing components, running the strategy loop, and managing overall workflow.
   - **Usage:** Instantiates strategy components, executes setup routines, and orchestrates the trading strategy based on collected data and configured parameters.
