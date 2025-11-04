import random
import math
import logging
import numpy as np
from numba import jit

def payoff_matrix(theta, strat1, strat2):
    if strat1 == 'T' and strat2 == 'T':
        p = 16 - theta
    elif strat1 == 'I' and strat2 == 'I':
        p = theta
    else:
        p = 4
    return p, p  # symmetric

@jit(nopython=True)
def update_strategies_jit(strategies, payoffs, beta):
    new_strategies = strategies.copy()
    n = len(strategies)
    for i in range(n):
        j = np.random.randint(0, n)
        while j == i:
            j = np.random.randint(0, n)
        prob = 1 / (1 + np.exp(-beta * (payoffs[j] - payoffs[i])))
        if np.random.random() < prob:
            new_strategies[i] = strategies[j]
    return new_strategies

def payoff_matrix_jit(theta, strat1, strat2):
    if strat1 == 0 and strat2 == 0:
        p = 16 - theta
    elif strat1 == 1 and strat2 == 1:
        p = theta
    else:
        p = 4
    return p, p

class Game:
    def __init__(self, theta, beta, max_steps, population):
        self.theta = theta
        self.beta = beta
        self.max_steps = max_steps
        self.population = population
        for agent in population:
            agent.payoff = 0.0
            agent.history = []
            agent.payoff_history = []
        self.strategies = np.array([0 if a.strategy == 'T' else 1 for a in population])
        self.payoffs = np.zeros(len(population))
        logging.info(f"Initialized game for theta {theta}, beta {beta}, max_steps {max_steps}, population size {len(population)}")

    def update_payoff(self):
        # Compute population fractions
        frac_t = np.mean(self.strategies == 0)
        frac_i = 1 - frac_t
        
        # Calculate average payoff for each agent
        payoff_tt = payoff_matrix_jit(self.theta, 0, 0)[0]
        payoff_ti = payoff_matrix_jit(self.theta, 0, 1)[0]
        payoff_it = payoff_matrix_jit(self.theta, 1, 0)[0]
        payoff_ii = payoff_matrix_jit(self.theta, 1, 1)[0]
        
        self.payoffs = np.where(self.strategies == 0, 
                                frac_t * payoff_tt + frac_i * payoff_ti,
                                frac_t * payoff_it + frac_i * payoff_ii)
        
        # Update agent objects and record history
        for i, agent in enumerate(self.population):
            agent.payoff = self.payoffs[i]
            agent.payoff_history.append(agent.payoff)

    def update_strategies(self):
        self.strategies = update_strategies_jit(self.strategies, self.payoffs, self.beta)
        
        # Update agent objects
        for i, agent in enumerate(self.population):
            agent.strategy = 'T' if self.strategies[i] == 0 else 'I'

    def run(self):
        logging.info(f"Starting evolution for {self.max_steps} steps")
        for step in range(self.max_steps):
            self.update_payoff()
            self.update_strategies()
            # Record history after each evolution step
            for agent in self.population:
                agent.history.append(agent.strategy)
        logging.info(f"Evolution completed for theta {self.theta}")
        # Return equilibrium: fractions T and I
        t_count = sum(1 for a in self.population if a.strategy == 'T')
        i_count = len(self.population) - t_count
        frac_t = t_count / len(self.population)
        frac_i = i_count / len(self.population)
        fractions = {'T': frac_t, 'I': frac_i}
        logging.info(f"Final fractions: {fractions}")
        return fractions