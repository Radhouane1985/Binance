import pandas as pd

class CorrelationHunter:
    # Giving a universe of cryptocurrencies, this class help compute realtime correlation matrix then rank cryptos based on that
    def __init__(self, symbols, data_collector):
        self.symbols = symbols
        self.data_collector = data_collector

    def calculate_correlation_matrix(self):
        data = {symbol: self.data_collector.fetch_historical_data(symbol)['close'] for symbol in self.symbols}
        df = pd.DataFrame(data)
        return df.corr()

    def rank_pairs(self, top_n=3):
        correlation_matrix = self.calculate_correlation_matrix()
        pairs = []

        for i, row in correlation_matrix.iterrows():
            for j, corr in row.items():
                if i != j and (j, i) not in [(pair[1][0], pair[1][1]) for pair in pairs]:
                    pairs.append((corr, (i, j)))

        pairs.sort(reverse=True, key=lambda x: x[0])
        return pairs[:top_n]

