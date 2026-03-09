import sys
import argparse
sys.path.append('..')
from gra_ramanujan.universe import GRAUniverse
from gra_ramanujan.constants import CONSTANTS, CONSTANTS_DICT
from gra_ramanujan.utils import init_logs
from gra_ramanujan.visualization.plots import plot_evolution, plot_heatmap

def main():
    parser = argparse.ArgumentParser(description='Run GRA-Ramanujan evolution with multiple constants.')
    parser.add_argument('--constants', nargs='+', default=['pi', 'e', 'gamma', 'zeta2', 'zeta3', 'catalan'],
                        help='List of constant names to use')
    parser.add_argument('--agents', type=int, default=10, help='Number of agents')
    parser.add_argument('--generations', type=int, default=50, help='Number of generations')
    args = parser.parse_args()

    # Фильтруем константы по именам
    selected_constants = [c for c in CONSTANTS if c.name in args.constants]
    if not selected_constants:
        print("No valid constants selected. Using all.")
        selected_constants = CONSTANTS

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
    universe = GRAUniverse(num_agents=args.agents, config=config, constants=selected_constants)
    for gen in range(args.generations):
        universe.step()
        if gen % 10 == 0:
            print(f'Generation {gen}, J = {universe.history[-1]:.4f}')
    print('Evolution complete. Plotting...')
    plot_evolution()
    plot_heatmap()

if __name__ == '__main__':
    main()