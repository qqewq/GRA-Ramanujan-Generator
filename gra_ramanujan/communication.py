import random

def share_best_formulas(agents, share_prob=0.1):
    """Агенты обмениваются лучшими формулами."""
    for agent in agents:
        if random.random() < share_prob:
            donor = random.choice(agents)
            if donor.id == agent.id:
                continue
            # Копируем лучшую формулу от донора для какой-то константы
            const = random.choice(list(agent.best_formulas.keys()))
            donor_best = donor.best_formulas.get(const)
            if donor_best and (agent.best_formulas[const] is None or
                               donor_best['beauty'] > agent.best_formulas[const]['beauty']):
                # Копируем дерево
                new_tree = copy_tree(donor_best['tree'])
                agent.best_formulas[const] = {
                    'tree': new_tree,
                    'accuracy': donor_best['accuracy'],
                    'complexity': donor_best['complexity'],
                    'beauty': donor_best['beauty'],
                    'value': donor_best['value'],
                    'constant': const,
                    'generation': donor_best['generation']
                }

def copy_tree(node):
    if node.op == 'const':
        return ExpressionNode('const', value=node.value)
    elif node.op in ('sin','cos','exp','log'):
        return ExpressionNode(node.op, left=copy_tree(node.left))
    else:
        return ExpressionNode(node.op, left=copy_tree(node.left), right=copy_tree(node.right))