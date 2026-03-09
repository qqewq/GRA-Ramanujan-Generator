import math

def evaluate_accuracy(computed, true, eps=1e-12):
    """Оценка точности (1 – относительная ошибка, ограниченная)."""
    if computed == float('inf') or math.isnan(computed):
        return 0.0
    rel_error = abs((computed - true) / true)
    return max(0.0, 1.0 - min(rel_error, 1.0))

def evaluate_complexity(expr_tree):
    """Сложность – число узлов в дереве."""
    def count_nodes(node):
        if node is None:
            return 0
        if node.op == 'const':
            return 1
        elif node.op in ('sin','cos','exp','log'):
            return 1 + count_nodes(node.left)
        else:
            return 1 + count_nodes(node.left) + count_nodes(node.right)
    return count_nodes(expr_tree)

def evaluate_beauty(accuracy, complexity, alpha=0.5):
    """Красота формулы: взвешенная сумма точности и простоты."""
    simplicity = 1.0 / (1.0 + complexity)  # нормализованная простота
    return alpha * accuracy + (1 - alpha) * simplicity