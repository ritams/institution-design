import random
import math
import logging

def payoff_matrix(theta, strat1, strat2):
    if strat1 == 'T' and strat2 == 'T':
        p = 16 - theta
    elif strat1 == 'I' and strat2 == 'I':
        p = theta
    else:
        p = 4
    return p, p  # symmetric

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
        logging.info(f"Initialized game for theta {theta}, beta {beta}, max_steps {max_steps}, population size {len(population)}")

    def interact(self):
        random.shuffle(self.population)
        for i in range(0, len(self.population), 2):
            agent1 = self.population[i]
            agent2 = self.population[i + 1] if i + 1 < len(self.population) else None
            if agent2:
                p1, p2 = payoff_matrix(self.theta, agent1.strategy, agent2.strategy)
                agent1.payoff = p1
                agent2.payoff = p2
        # Record payoff history
        for agent in self.population:
            agent.payoff_history.append((agent.payoff, self.theta))

    def update_strategies(self):
        new_strategies = []
        for agent in self.population:
            j = random.choice([a for a in self.population if a != agent])
            prob = 1 / (1 + math.exp(-self.beta * (j.payoff - agent.payoff)))
            new_strategy = j.strategy if random.random() < prob else agent.strategy
            new_strategies.append(new_strategy)
        for a, ns in zip(self.population, new_strategies):
            a.strategy = ns

    def run(self):
        logging.info(f"Starting evolution for {self.max_steps} steps")
        for step in range(self.max_steps):
            self.interact()
            self.update_strategies()
            # Record history after each evolution step
            for agent in self.population:
                agent.history.append((agent.strategy, self.theta))
        logging.info(f"Evolution completed for theta {self.theta}")
        # Return equilibrium: fractions T and I
        t_count = sum(1 for a in self.population if a.strategy == 'T')
        i_count = len(self.population) - t_count
        frac_t = t_count / len(self.population)
        frac_i = i_count / len(self.population)
        fractions = {'T': frac_t, 'I': frac_i}
        logging.info(f"Final fractions: {fractions}")
        return fractions