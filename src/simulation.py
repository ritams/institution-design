import random
from .agent import Agent
from .game import Game

class Simulation:
    def __init__(self, N, f_cultural, theta_list, beta, max_steps):
        self.N = N
        self.f_cultural = f_cultural
        self.theta_list = theta_list
        self.beta = beta
        self.max_steps = max_steps
        self.population = [Agent(random.random() < f_cultural) for _ in range(N)]
        self.equilibria = {}  # theta: fraction_T

    def initialize_for_theta(self, theta):
        if not self.equilibria:
            for agent in self.population:
                agent.strategy = random.choice(['T', 'I'])
        else:
            prev_thetas = list(self.equilibria.keys())
            closest_theta = min(prev_thetas, key=lambda t: abs(t - theta))
            frac_t = self.equilibria[closest_theta]
            for agent in self.population:
                if agent.cultural_sway:
                    agent.strategy = 'T' if random.random() < frac_t else 'I'
                else:
                    agent.strategy = random.choice(['T', 'I'])

    def run_simulation(self):
        for theta in self.theta_list:
            self.initialize_for_theta(theta)
            game = Game(theta, self.beta, self.max_steps, self.population)
            frac_t = game.run()
            self.equilibria[theta] = frac_t
        return self.equilibria
