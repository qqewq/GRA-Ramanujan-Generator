import copy
import numpy as np
from .agent import RamanujanAgent
from .foam import compute_foam_level0, compute_foam_level1, compute_foam_level2
from .communication import share_best_formulas
from .utils import log_conjecture, log_machine

class GRAUniverse:
    def __init__(self, num_agents, config, constants, known_identities=None):
        self.num_agents = num_agents
        self.config = config
        self.constants = constants
        self.known_identities = known_identities or []
        self.agents = [RamanujanAgent(i, config) for i in range(num_agents)]
        self.generation = 0
        self.history = []

    def step(self):
        for agent in self.agents:
            formula = agent.step()
            log_conjecture(self.generation, agent.id, formula)

        foam0 = compute_foam_level0(self.agents, self.constants)
        foam1 = compute_foam_level1(self.agents, self.constants, self.known_identities)
        foam2 = compute_foam_level2(self.agents)

        J = (self.config.get('lambda0', 1.0) * foam0 +
             self.config.get('lambda1', 0.5) * foam1 +
             self.config.get('lambda2', 0.2) * foam2)
        self.history.append(J)

        self.update_vitality(foam2)
        self.selection()
        share_best_formulas(self.agents)

        self.generation += 1
        for agent in self.agents:
            log_machine(self.generation, agent)

    def update_vitality(self, foam2):
        for agent in self.agents:
            mean_beauty = np.mean([f['beauty'] for f in agent.best_formulas.values() if f])
            # Простейшая модель
            agent.vitality = 0.9 * agent.vitality + 0.1 * mean_beauty
            agent.vitality = max(0.0, min(1.0, agent.vitality))

    def selection(self):
        self.agents = [a for a in self.agents if a.vitality > self.config.get('death_threshold', 0.2)]
        while len(self.agents) < self.num_agents:
            parent = np.random.choice(self.agents)
            child = copy.deepcopy(parent)
            child.id = max(a.id for a in self.agents) + 1
            child.vitality = 1.0
            child.age = 0
            child.mutate(self.config.get('mutation_rate', 0.1))
            self.agents.append(child)