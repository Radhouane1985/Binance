class RiskManager:
    def __init__(self):
        self.positions = {}

    def update_position(self, pair, position):
        self.positions[pair] = position

    def get_position(self, pair):
        return self.positions.get(pair)

    def close_position(self, pair):
        if pair in self.positions:
            del self.positions[pair]

    def manage_positions(self, pair, action):
        if action == "short":
            self.update_position(pair, 'short')
            print('Short')
            # Add logic for shorting symbol1 and buying symbol2
        elif action == "long":
            self.update_position(pair, 'long')
            print('Long')
            # Add logic for buying symbol1 and shorting symbol2
        elif action is None:
            self.close_position(pair)
            # Add logic for closing the position of both symbols
