import numpy as np

def compute_foam_level0(agents, constants):
    total_error = 0.0
    count = 0
    for agent in agents:
        for const in constants:
            best = agent.best_formulas.get(const.name)
            if best:
                error = 1 - best.get('accuracy', 0)
                total_error += error
                count += 1
    return total_error / count if count else 0

def compute_foam_level1(agents, constants, known_identities):
    if not known_identities:
        return 0.0
    total = 0.0
    for agent in agents:
        for id_func in known_identities:
            total += id_func(agent.best_formulas)
    return total / len(agents) if agents else 0

def compute_foam_level2(agents):
    mean_beauties = []
    for agent in agents:
        vals = [f['beauty'] for f in agent.best_formulas.values() if f]
        if vals:
            mean_beauties.append(np.mean(vals))
    return np.var(mean_beauties) if mean_beauties else 0