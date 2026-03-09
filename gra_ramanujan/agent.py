import random
import numpy as np
from .generation import generate_random_expression, mutate_expression
from .evaluation import evaluate_accuracy, evaluate_complexity, evaluate_beauty
from .constants import CONSTANTS_DICT

class RamanujanAgent:
    def __init__(self, agent_id, config):
        self.id = agent_id
        self.config = config
        self.best_formulas = {c: None for c in CONSTANTS_DICT}
        self.formulas_history = {c: [] for c in CONSTANTS_DICT}
        self.weights = {c: 1.0 for c in CONSTANTS_DICT}
        self.vitality = 1.0
        self.age = 0

    def choose_constant(self):
        names = list(self.weights.keys())
        probs = np.array([self.weights[n] for n in names])
        probs = probs / probs.sum()
        return np.random.choice(names, p=probs)

    def generate_formula(self, constant_name):
        tree = generate_random_expression(
            max_depth=self.config.get('max_depth', 5),
            const_range=self.config.get('const_range', (-10,10))
        )
        return {
            'tree': tree,
            'constant': constant_name,
            'generation': self.age
        }

    def evaluate_formula(self, formula, constant):
        try:
            val = formula['tree'].evaluate()
        except:
            val = float('inf')
        accuracy = evaluate_accuracy(val, constant.value())
        complexity = evaluate_complexity(formula['tree'])
        beauty = evaluate_beauty(accuracy, complexity,
                                 alpha=self.config.get('beauty_alpha', 0.5))
        formula.update({
            'value': val,
            'accuracy': accuracy,
            'complexity': complexity,
            'beauty': beauty
        })
        return formula

    def update_best(self, formula):
        const = formula['constant']
        if (self.best_formulas[const] is None or
            formula['beauty'] > self.best_formulas[const]['beauty']):
            self.best_formulas[const] = formula
            self.weights[const] = 0.1 + formula['beauty']
        self.formulas_history[const].append(formula)

    def step(self):
        const_name = self.choose_constant()
        constant = CONSTANTS_DICT[const_name]
        formula = self.generate_formula(const_name)
        formula = self.evaluate_formula(formula, constant)
        self.update_best(formula)
        self.age += 1
        return formula

    def mutate(self, mutation_rate):
        """Мутирует лучшие формулы (для потомков)."""
        for const, form in self.best_formulas.items():
            if form and random.random() < mutation_rate:
                new_tree = mutate_expression(form['tree'], mutation_rate)
                new_form = form.copy()
                new_form['tree'] = new_tree
                self.best_formulas[const] = new_form