#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Продвинутый пример настройки и запуска эволюции GRA-Ramanujan.
Демонстрирует использование различных параметров, нескольких констант
и вывода результатов.
"""

import sys
sys.path.append('..')

from gra_ramanujan.universe import GRAUniverse
from gra_ramanujan.constants import CONSTANTS
from gra_ramanujan.utils import init_logs
from gra_ramanujan.visualization.plots import plot_evolution, plot_heatmap, plot_complexity_distribution

def main():
    # Инициализация логов
    init_logs()

    # Расширенная конфигурация
    config = {
        # Веса для уровней пены (лямбды)
        'lambda0': 1.2,        # важность точности формул
        'lambda1': 0.8,        # важность согласованности (если есть тождества)
        'lambda2': 0.3,        # важность разнообразия популяции

        # Параметры отбора
        'death_threshold': 0.25,   # порог витальности для удаления агента
        'mutation_rate': 0.15,     # вероятность мутации при создании потомка
        'share_prob': 0.2,         # вероятность обмена формулами между агентами

        # Параметры генерации формул
        'max_depth': 6,             # максимальная глубина дерева выражений
        'const_range': (-20, 20),   # диапазон констант в листьях
        'beauty_alpha': 0.6,        # вес точности в формуле красоты (1-alpha для простоты)

        # Дополнительные параметры (не используются напрямую, но можно передать)
        'seed': 42,                  # для воспроизводимости
    }

    # Выбираем набор констант (можно изменить по желанию)
    selected_constants = [c for c in CONSTANTS if c.name in ('pi', 'e', 'gamma', 'zeta2')]
    print(f"Выбраны константы: {[c.name for c in selected_constants]}")

    # Создаём вселенную с 20 агентами
    universe = GRAUniverse(
        num_agents=20,
        config=config,
        constants=selected_constants,
        known_identities=[]  # здесь можно передать функции проверки тождеств
    )

    # Запускаем эволюцию на 100 поколений
    generations = 100
    print(f"Запуск эволюции на {generations} поколений...")
    for gen in range(generations):
        universe.step()
        if gen % 20 == 0 or gen == generations - 1:
            print(f"Поколение {gen:3d} | J = {universe.history[-1]:.6f} | "
                  f"Агентов: {len(universe.agents)}")

    print("\nЭволюция завершена.")

    # Построение графиков
    print("Построение графиков...")
    plot_evolution()
    plot_heatmap()
    plot_complexity_distribution()

    # Вывод лучших формул
    print("\nЛучшие формулы по каждой константе:")
    for const in selected_constants:
        best = None
        best_beauty = -1
        for agent in universe.agents:
            formula = agent.best_formulas.get(const.name)
            if formula and formula['beauty'] > best_beauty:
                best_beauty = formula['beauty']
                best = formula
        if best:
            print(f"{const.name}: красота {best['beauty']:.4f}, "
                  f"точность {best['accuracy']:.4f}, сложность {best['complexity']}")
            print(f"   {best['tree']}")

if __name__ == '__main__':
    main()