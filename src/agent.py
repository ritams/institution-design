class Agent:
    def __init__(self, cultural_sway):
        self.strategy = None  # 'T' or 'I'
        self.payoff = 0.0
        self.cultural_sway = cultural_sway
        self.history = []  
        self.payoff_history = []
