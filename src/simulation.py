import random
import os
import logging
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
        logging.info(f"Initialized simulation with N={N}, f_cultural={f_cultural}, theta_list={theta_list}, beta={beta}, max_steps={max_steps}")

    def initialize_for_theta(self, theta):
        if not self.equilibria:
            for agent in self.population:
                agent.strategy = random.choice(['T', 'I'])
            logging.info(f"Initialized strategies randomly for first theta {theta}")
        else:
            prev_thetas = list(self.equilibria.keys())
            closest_theta = min(prev_thetas, key=lambda t: abs(t - theta))
            frac_dict = self.equilibria[closest_theta]
            for agent in self.population:
                if agent.cultural_sway:
                    agent.strategy = 'T' if random.random() < frac_dict['T'] else 'I'
                else:
                    agent.strategy = random.choice(['T', 'I'])
            logging.info(f"Initialized strategies for theta {theta} based on closest previous theta {closest_theta} with T fraction {frac_dict['T']}")

    def run_simulation(self):
        os.makedirs('results', exist_ok=True)
        logging.info("Starting full simulation run")
        for theta in self.theta_list:
            logging.info(f"Processing theta {theta}")
            self.initialize_for_theta(theta)
            game = Game(theta, self.beta, self.max_steps, self.population)
            fractions = game.run()
            self.equilibria[theta] = fractions
            logging.info(f"Completed theta {theta}, final fractions: {fractions}")
            # Save strategies
            with open(f'results/strategy_theta_{theta}.txt', 'w') as f:
                for agent in self.population:
                    strategies = [str(s) for s, t in agent.history]
                    f.write(' '.join(strategies) + '\n')
            # Save payoffs
            with open(f'results/payoff_theta_{theta}.txt', 'w') as f:
                for agent in self.population:
                    payoffs = [str(p) for p, t in agent.payoff_history]
                    f.write(' '.join(payoffs) + '\n')
        logging.info(f"Simulation completed. Equilibria: {self.equilibria}")
        return self.equilibria
