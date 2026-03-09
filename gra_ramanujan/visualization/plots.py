import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

def plot_evolution(csv_path='data/conjectures.csv'):
    df = pd.read_csv(csv_path)
    plt.figure(figsize=(12,6))
    for const in df['constant'].unique():
        subset = df[df['constant'] == const]
        best_per_gen = subset.groupby('generation')['beauty'].max()
        plt.plot(best_per_gen.index, best_per_gen.values, label=const, alpha=0.7)
    plt.xlabel('Поколение')
    plt.ylabel('Максимальная красота')
    plt.title('Эволюция красоты формул')
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_heatmap(csv_path='data/conjectures.csv'):
    df = pd.read_csv(csv_path)
    pivot = df.pivot_table(index='constant', columns='generation', values='beauty', aggfunc='max')
    plt.figure(figsize=(14,8))
    sns.heatmap(pivot, cmap='viridis', cbar_kws={'label': 'max beauty'})
    plt.xlabel('Поколение')
    plt.ylabel('Константа')
    plt.title('Теплокарта максимальной красоты')
    plt.show()

def plot_complexity_distribution(csv_path='data/conjectures.csv'):
    df = pd.read_csv(csv_path)
    plt.figure(figsize=(10,6))
    sns.boxplot(data=df, x='generation', y='complexity')
    plt.xlabel('Поколение')
    plt.ylabel('Сложность')
    plt.title('Распределение сложности формул по поколениям')
    plt.xticks(rotation=45)
    plt.show()