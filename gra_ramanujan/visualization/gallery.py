import pandas as pd

def generate_latex_gallery(csv_path='data/conjectures.csv', output_file='best_formulas.tex', top_k=5):
    """
    Генерирует LaTeX-файл с лучшими формулами для каждой константы.

    Параметры:
        csv_path (str): путь к файлу с логами conjectures.csv
        output_file (str): имя выходного .tex файла
        top_k (int): сколько лучших формул выводить (по убыванию красоты)
    """
    df = pd.read_csv(csv_path)
    # Группируем по константе и выбираем строку с максимальной красотой для каждой
    best_per_const = df.loc[df.groupby('constant')['beauty'].idxmax()]

    # Сортируем по убыванию красоты и берём top_k
    best_overall = best_per_const.nlargest(top_k, 'beauty')

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(r"\documentclass{article}" + "\n")
        f.write(r"\usepackage{amsmath, amssymb}" + "\n")
        f.write(r"\begin{document}" + "\n")
        f.write(r"\section*{Лучшие найденные формулы}" + "\n")

        for _, row in best_overall.iterrows():
            const = row['constant']
            expr = row['expression']  # предполагается, что это строка с формулой
            acc = row['accuracy']
            comp = row['complexity']
            beauty = row['beauty']

            f.write(r"\paragraph{" + f"{const}" + r"}" + "\n")
            f.write(r"\begin{equation*}" + "\n")
            f.write(f"    {expr}\n")
            f.write(r"\end{equation*}" + "\n")
            f.write(r"\noindent " + f"Точность: {acc:.6f}, "
                    f"Сложность: {comp}, "
                    f"Красота: {beauty:.6f}\n\n")

        f.write(r"\end{document}" + "\n")

    print(f"LaTeX-галерея сохранена в {output_file}")