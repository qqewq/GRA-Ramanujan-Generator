#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Скрипт для анализа логов эволюции GRA-Рамануджана.
Читает файлы conjectures.csv и machines.csv, выводит статистику
и строит графики с помощью функций из visualization.plots.
"""

import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
sys.path.append('..')
from gra_ramanujan.visualization.plots import plot_evolution, plot_heatmap, plot_complexity_distribution

def load_and_summarize(conj_path='data/conjectures.csv', mach_path='data/machines.csv'):
    """
    Загружает логи и выводит сводную статистику.
    """
    try:
        df_conj = pd.read_csv(conj_path)
        df_mach = pd.read_csv(mach_path)
    except FileNotFoundError as e:
        print(f"❌ Файл не найден: {e}")
        return None, None

    print("=" * 60)
    print("📊 Анализ логов GRA-Ramanujan-Generator")
    print("=" * 60)

    # Общая статистика по conjectures
    print(f"\n📄 Лог формул (conjectures.csv):")
    print(f"   Всего записей: {len(df_conj)}")
    print(f"   Уникальных агентов: {df_conj['machine_id'].nunique()}")
    print(f"   Константы: {', '.join(df_conj['constant'].unique())}")
    print(f"   Диапазон поколений: {df_conj['generation'].min()} – {df_conj['generation'].max()}")

    # Статистика по красоте, точности, сложности
    print(f"\n📈 Меры качества:")
    print(f"   Красота (beauty): средняя = {df_conj['beauty'].mean():.4f}, "
          f"макс = {df_conj['beauty'].max():.4f}, мин = {df_conj['beauty'].min():.4f}")
    print(f"   Точность (accuracy): средняя = {df_conj['accuracy'].mean():.4f}, "
          f"макс = {df_conj['accuracy'].max():.4f}, мин = {df_conj['accuracy'].min():.4f}")
    print(f"   Сложность (complexity): средняя = {df_conj['complexity'].mean():.2f}, "
          f"макс = {df_conj['complexity'].max()}, мин = {df_conj['complexity'].min()}")

    # Лучшие формулы
    best_idx = df_conj.groupby('constant')['beauty'].idxmax()
    best_formulas = df_conj.loc[best_idx]
    print(f"\n🏆 Лучшая формула для каждой константы:")
    for _, row in best_formulas.iterrows():
        print(f"   {row['constant']}: красота {row['beauty']:.4f}, "
              f"точность {row['accuracy']:.4f}, сложность {row['complexity']}")
        print(f"       {row['expression'][:80]}...")  # обрезаем длинные выражения

    # Статистика по машинам
    print(f"\n🤖 Лог машин (machines.csv):")
    print(f"   Всего записей: {len(df_mach)}")
    print(f"   Уникальных машин: {df_mach['machine_id'].nunique()}")
    last_gen = df_mach['generation'].max()
    last_gen_data = df_mach[df_mach['generation'] == last_gen]
    print(f"   В последнем поколении (gen={last_gen}) живых машин: {len(last_gen_data)}")
    print(f"   Средняя красота в последнем поколении: {last_gen_data['mean_beauty'].mean():.4f}")

    return df_conj, df_mach

def plot_additional_stats(df_conj, df_mach):
    """
    Строит дополнительные графики, не входящие в стандартный набор.
    """
    if df_conj is None or df_mach is None:
        return

    # 1. Динамика средней красоты по поколениям
    plt.figure(figsize=(10,5))
    mean_beauty_per_gen = df_conj.groupby('generation')['beauty'].mean()
    plt.plot(mean_beauty_per_gen.index, mean_beauty_per_gen.values, marker='o', linestyle='-', alpha=0.7)
    plt.xlabel('Поколение')
    plt.ylabel('Средняя красота')
    plt.title('Средняя красота формул по поколениям')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('data/mean_beauty_evolution.png')
    plt.show()

    # 2. Динамика витальности машин (если есть данные)
    if 'vitality' in df_mach.columns:
        plt.figure(figsize=(10,5))
        # Отображаем несколько случайных машин
        sample_ids = np.random.choice(df_mach['machine_id'].unique(), min(5, len(df_mach['machine_id'].unique())), replace=False)
        for mid in sample_ids:
            machine_data = df_mach[df_mach['machine_id'] == mid]
            plt.plot(machine_data['generation'], machine_data['vitality'], label=f'Machine {mid}', alpha=0.7)
        plt.xlabel('Поколение')
        plt.ylabel('Витальность')
        plt.title('Витальность отдельных машин')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.savefig('data/vitality_evolution.png')
        plt.show()

def main():
    df_conj, df_mach = load_and_summarize()
    if df_conj is None:
        return

    print("\n📈 Построение стандартных графиков (эволюция, теплокарта, сложность)...")
    plot_evolution()
    plot_heatmap()
    plot_complexity_distribution()

    print("\n📊 Построение дополнительных графиков...")
    plot_additional_stats(df_conj, df_mach)

    print("\n✅ Анализ завершён. Все графики сохранены в папку 'data/'.")

if __name__ == '__main__':
    main()