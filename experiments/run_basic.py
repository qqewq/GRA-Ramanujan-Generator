import sys
sys.path.append('..')
from gra_ramanujan.universe import GRAUniverse
from gra_ramanujan.constants import CONSTANTS
from gra_ramanujan.utils import init_logs
from gra_ramanujan.visualization.plots import plot_evolution, plot_heatmap

if __name__ == '__main__':
    init_logs()
    config = {
        'lambda0': 1.0,
        'lambda1': 0.5,
        'lambda2': 0.2,
        'death_threshold': 0.2,
        'mutation_rate': 0.1,
        'max_depth': 5,
        'const_range': (-10,10),
        'beauty_alpha': 0.5
    }
    universe = GRAUniverse(num_agents=10, config=config, constants=CONSTANTS)
    for gen in range(50):
        universe.step()
        if gen % 10 == 0:
            print(f'Поколение {gen}, J = {universe.history[-1]:.4f}')
    print('Эволюция завершена. Строим графики...')
    plot_evolution()
    plot_heatmap()