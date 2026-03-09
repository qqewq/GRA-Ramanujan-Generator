import random
import numpy as np

class ExpressionNode:
    def __init__(self, op, left=None, right=None, value=None):
        self.op = op  # '+', '-', '*', '/', 'sin', 'cos', 'exp', 'log', или 'const'
        self.left = left
        self.right = right
        self.value = value  # если op == 'const'

    def evaluate(self):
        if self.op == 'const':
            return self.value
        elif self.op == '+':
            return self.left.evaluate() + self.right.evaluate()
        elif self.op == '-':
            return self.left.evaluate() - self.right.evaluate()
        elif self.op == '*':
            return self.left.evaluate() * self.right.evaluate()
        elif self.op == '/':
            r = self.right.evaluate()
            return self.left.evaluate() / r if r != 0 else float('inf')
        elif self.op == 'sin':
            return math.sin(self.left.evaluate())
        elif self.op == 'cos':
            return math.cos(self.left.evaluate())
        elif self.op == 'exp':
            return math.exp(self.left.evaluate())
        elif self.op == 'log':
            arg = self.left.evaluate()
            return math.log(arg) if arg > 0 else float('inf')
        else:
            raise ValueError(f"Unknown op: {self.op}")

    def __str__(self):
        if self.op == 'const':
            return str(self.value)
        elif self.op in ('sin', 'cos', 'exp', 'log'):
            return f"{self.op}({self.left})"
        else:
            return f"({self.left} {self.op} {self.right})"

def generate_random_expression(max_depth=3, const_range=(-10,10), full=False):
    """Генерирует случайное дерево выражения."""
    if max_depth <= 0 or (not full and random.random() < 0.3):
        # Лист – константа или переменная (пока только константы)
        return ExpressionNode('const', value=random.uniform(*const_range))
    op = random.choice(['+', '-', '*', '/', 'sin', 'cos', 'exp', 'log'])
    if op in ('sin', 'cos', 'exp', 'log'):
        left = generate_random_expression(max_depth-1, const_range, full)
        return ExpressionNode(op, left=left)
    else:
        left = generate_random_expression(max_depth-1, const_range, full)
        right = generate_random_expression(max_depth-1, const_range, full)
        return ExpressionNode(op, left=left, right=right)

def mutate_expression(tree, mutation_rate=0.1):
    """Мутирует дерево с заданной вероятностью."""
    if random.random() < mutation_rate:
        return generate_random_expression(max_depth=3)
    if tree.op != 'const':
        tree.left = mutate_expression(tree.left, mutation_rate)
        if tree.right:
            tree.right = mutate_expression(tree.right, mutation_rate)
    return tree

def crossover_expression(parent1, parent2):
    """Кроссинговер – обмен поддеревьями."""
    if random.random() < 0.5:
        return parent1, parent2
    # Простой обмен листьями (можно усложнить)
    def copy_tree(node):
        if node.op == 'const':
            return ExpressionNode('const', value=node.value)
        elif node.op in ('sin','cos','exp','log'):
            return ExpressionNode(node.op, left=copy_tree(node.left))
        else:
            return ExpressionNode(node.op, left=copy_tree(node.left), right=copy_tree(node.right))
    new1 = copy_tree(parent1)
    new2 = copy_tree(parent2)
    # Обмен случайными поддеревьями
    # (здесь упрощённо)
    return new1, new2