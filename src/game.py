import random
import math

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
            agent.game_index = theta

    def interact(self):
        for agent in self.population:
            partner = random.choice(self.population)
            p_agent, p_partner = payoff_matrix(self.theta, agent.strategy, partner.strategy)
            agent.payoff += p_agent
            partner.payoff += p_partner

    def update_strategies(self):
        new_strategies = []
        for agent in self.population:
            j = random.choice([a for a in self.population if a != agent])
            prob = 1 / (1 + math.exp(-self.beta * (j.payoff - agent.payoff)))
            new_strategy = j.strategy if random.random() < prob else agent.strategy
            new_strategies.append(new_strategy)
        changed = any(ns != a.strategy for ns, a in zip(new_strategies, self.population))
        for a, ns in zip(self.population, new_strategies):
            a.strategy = ns
        return changed

    def run(self):
        steps = 0
        while steps < self.max_steps:
            self.interact()
            changed = self.update_strategies()
            if not changed:
                break
            steps += 1
        # Record history
        for agent in self.population:
            agent.history.append(agent.strategy)
        # Return equilibrium: fraction T
        t_count = sum(1 for a in self.population if a.strategy == 'T')
        return t_count / len(self.population)
