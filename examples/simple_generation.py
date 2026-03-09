#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Простой пример генерации случайной математической формулы
с использованием модуля генерации GRA-Ramanujan.
"""

import sys
sys.path.append('..')
from gra_ramanujan.generation import generate_random_expression

def main():
    # Генерируем случайное выражение максимальной глубины 4
    expr = generate_random_expression(max_depth=4, const_range=(-5, 5))
    
    print("Сгенерированное выражение:")
    print(expr)
    
    # Пытаемся вычислить значение
    try:
        value = expr.evaluate()
        print(f"Численное значение: {value}")
    except Exception as e:
        print(f"Ошибка при вычислении: {e}")

if __name__ == "__main__":
    main()