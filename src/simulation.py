import random
import os
import logging
import pickle
import yaml
from datetime import datetime
import numpy as np
from .agent import Agent
from .game import Game

class Simulation:
    def __init__(self, N, f_cultural, theta_list, beta, max_steps, ensemble_size):
        self.N = N
        self.f_cultural = f_cultural
        self.theta_list = theta_list
        self.beta = beta
        self.max_steps = max_steps
        self.ensemble_size = ensemble_size
        self.population = [Agent(random.random() < f_cultural) for _ in range(N)]
        self.equilibria = {}  # theta: averaged fractions
        logging.info(f"Initialized simulation with N={N}, f_cultural={f_cultural}, theta_list={theta_list}, beta={beta}, max_steps={max_steps}, ensemble_size={ensemble_size}")

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

    def average_fractions(self, frac_list):
        if not frac_list:
            return {}
        keys = frac_list[0].keys()
        avg = {}
        for k in keys:
            avg[k] = sum(f[k] for f in frac_list) / len(frac_list)
        return avg

    def run_simulation(self):
        os.makedirs('results', exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        run_dir = f'results/run_{timestamp}'
        os.makedirs(run_dir, exist_ok=True)
        self.data = {}
        logging.info("Starting full simulation run")
        for theta in self.theta_list:
            logging.info(f"Processing theta {theta}")
            self.initialize_for_theta(theta)
            initial_strategies = [a.strategy for a in self.population]
            ensemble_fractions = []
            self.data[theta] = {}
            for i in range(self.ensemble_size):
                # Reset strategies to initial
                for a, s in zip(self.population, initial_strategies):
                    a.strategy = s
                game = Game(theta, self.beta, self.max_steps, self.population)
                game.strategies = np.array([0 if a.strategy == 'T' else 1 for a in self.population])
                fractions = game.run()
                ensemble_fractions.append(fractions)
                # Collect strategies and payoffs
                strategies = [agent.history for agent in self.population]
                payoffs = [agent.payoff_history for agent in self.population]
                self.data[theta][i] = {'strategies': strategies, 'payoffs': payoffs}
            # Average fractions
            averaged_fractions = self.average_fractions(ensemble_fractions)
            self.equilibria[theta] = averaged_fractions
            logging.info(f"Completed theta {theta}, averaged final fractions: {averaged_fractions}")
        logging.info(f"Simulation completed. Equilibria: {self.equilibria}")
        # Save data to pickle
        with open(f'{run_dir}/simulation_data.pkl', 'wb') as f:
            pickle.dump(self.data, f)
        # Save metadata to YAML
        metadata = {
            'N': self.N,
            'f_cultural': self.f_cultural,
            'theta_list': self.theta_list,
            'beta': self.beta,
            'max_steps': self.max_steps,
            'ensemble_size': self.ensemble_size,
            'equilibria': [{'theta': theta, **self.equilibria[theta]} for theta in self.theta_list],
            'timestamp': timestamp,
            'run_dir': run_dir
        }
        with open(f'{run_dir}/simulation_metadata.yaml', 'w') as f:
            yaml.dump(metadata, f)
        return self.equilibria
