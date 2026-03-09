# API Reference

## Модуль `constants`

### `class Constant`
- `name: str` – имя константы
- `category: str` – категория ('math', 'physics')
- `value(dps=None) -> mpf` – возвращает значение с заданной точностью
- `latex: str` – LaTeX-представление

### `CONSTANTS: List[Constant]` – список предопределённых констант
### `CONSTANTS_DICT: Dict[str, Constant]` – словарь для быстрого доступа

## Модуль `agent`

### `class RamanujanAgent`
- `__init__(agent_id, config)`
- `choose_constant() -> str` – выбирает константу с учётом весов
- `generate_formula(constant_name) -> dict` – генерирует случайную формулу
- `evaluate_formula(formula, constant) -> dict` – оценивает точность, сложность, красоту
- `update_best(formula)` – обновляет лучшую формулу для константы
- `step() -> dict` – один шаг: выбор, генерация, оценка, обновление
- `mutate(mutation_rate)` – мутирует лучшие формулы

Атрибуты:
- `id: int`
- `best_formulas: Dict[str, dict]` – лучшие формулы по константам
- `weights: Dict[str, float]` – веса для выбора констант
- `vitality: float`
- `age: int`

## Модуль `universe`

### `class GRAUniverse`
- `__init__(num_agents, config, constants, known_identities=None)`
- `step()` – один шаг эволюции: шаг всех агентов, вычисление пены, селекция, обмен
- `update_vitality(foam2)` – обновление витальности на основе пены уровня 2
- `selection()` – удаление мёртвых и восполнение популяции

Атрибуты:
- `agents: List[RamanujanAgent]`
- `generation: int`
- `history: List[float]` – история функционала J

## Модуль `projectors`

### `class Projector`
- `apply_level0(formula) -> formula` – проектор на цель уровня 0 (упрощение, подгонка)
- `apply_level1(formulas_dict, identities) -> formulas_dict` – согласование формул по тождествам
- `apply_level2(population) -> population` – обмен лучшими формулами

## Модуль `foam`

### `compute_foam_level0(agents, constants) -> float`
### `compute_foam_level1(agents, constants, known_identities) -> float`
### `compute_foam_level2(agents) -> float`
### `total_j(agents, constants, config) -> float`

## Модуль `generation`

### `generate_random_expression(max_depth=3, const_range=(-10,10), full=False) -> ExpressionNode`
### `mutate_expression(tree, mutation_rate=0.1) -> ExpressionNode`
### `crossover_expression(parent1, parent2) -> (ExpressionNode, ExpressionNode)`

## Модуль `evaluation`

### `evaluate_accuracy(computed, true, eps=1e-12) -> float`
### `evaluate_complexity(expr_tree) -> int`
### `evaluate_beauty(accuracy, complexity, alpha=0.5) -> float`

## Модуль `communication`

### `share_best_formulas(agents, share_prob=0.1)`

## Модуль `visualization.plots`

### `plot_evolution(csv_path='data/conjectures.csv')`
### `plot_heatmap(csv_path='data/conjectures.csv')`
### `plot_complexity_distribution(csv_path='data/conjectures.csv')`

## Модуль `utils`

### `init_logs()`
### `log_conjecture(generation, machine_id, formula)`
### `log_machine(generation, machine)`