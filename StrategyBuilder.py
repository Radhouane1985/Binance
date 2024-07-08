import numpy as np
from scipy.stats import zscore
import statsmodels.api as sm
import pandas as pd

class StrategyBuilder:
    def __init__(self, symbol1_data, symbol2_data):
        self.symbol1_data = symbol1_data
        self.symbol2_data = symbol2_data
        self.spread_data = None
        self.bands = {}
    
    def calculate_spread(self):
        if not isinstance(self.symbol1_data, pd.DataFrame) or not isinstance(self.symbol2_data, pd.DataFrame):
            raise ValueError("Both symbol1_data and symbol2_data must be pandas DataFrames")

        if len(self.symbol1_data) != len(self.symbol2_data):
            raise ValueError("symbol1_data and symbol2_data must have the same length")

        # Ensure dataframes have the same index
        self.symbol1_data = self.symbol1_data.set_index(self.symbol2_data.index)

        spread = self.symbol1_data['close'] - self.symbol2_data['close']
        X = sm.add_constant(self.symbol2_data['close'])
        
        # Ensure X has the same index as self.symbol2_data
        X = X.reindex(self.symbol2_data.index)

        model = sm.OLS(self.symbol1_data['close'], X).fit()
        residuals = model.resid
        z_scores = zscore(residuals)

        self.spread_data = {
            'spread': spread,
            'residuals': residuals,
            'zscore': z_scores
        }

    def set_bands(self):
        self.bands['upper'] = np.percentile(self.spread_data['zscore'], 95)
        self.bands['lower'] = np.percentile(self.spread_data['zscore'], 5)
        self.bands['upper_medium'] = np.percentile(self.spread_data['zscore'], 75)
        self.bands['lower_medium'] = np.percentile(self.spread_data['zscore'], 25)

    def check_entry_signal(self):
        score = self.spread_data['zscore'][-1]
        print('score of pair :', score)
        if score > self.bands['upper']:
            return "Short Spread"
        elif score < self.bands['lower']:
            return "Buy Spread"
        return None

    def check_exit_signal(self):
        score = self.spread_data['zscore'][-1]
        if self.bands['lower_medium'] < score < self.bands['upper_medium']:
            return True
        return False
