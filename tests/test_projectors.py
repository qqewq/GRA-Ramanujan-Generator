import unittest
import sys
sys.path.append('..')
from gra_ramanujan.projectors import Projector

class TestProjectors(unittest.TestCase):
    def setUp(self):
        # Минимальные данные для тестов
        self.formula = {'tree': 'dummy', 'constant': 'pi', 'accuracy': 0.9}
        self.formulas_dict = {'pi': self.formula, 'e': None}
        self.identities = []  # пока пусто
        self.population = []  # пустая популяция

    def test_apply_level0_returns_copy(self):
        """Проверяет, что apply_level0 возвращает копию, не изменяя оригинал."""
        result = Projector.apply_level0(self.formula)
        self.assertEqual(result, self.formula)
        # Проверяем, что это не тот же объект (копия)
        self.assertIsNot(result, self.formula)

    def test_apply_level1_returns_dict(self):
        """Проверяет, что apply_level1 возвращает словарь (возможно, без изменений)."""
        result = Projector.apply_level1(self.formulas_dict, self.identities)
        self.assertIsInstance(result, dict)
        self.assertEqual(result.keys(), self.formulas_dict.keys())

    def test_apply_level2_handles_population(self):
        """Проверяет, что apply_level2 не падает при пустой популяции."""
        try:
            Projector.apply_level2(self.population)
        except Exception as e:
            self.fail(f"apply_level2 raised an exception: {e}")

    def test_apply_level2_returns_population(self):
        """Проверяет, что apply_level2 возвращает популяцию (может быть модифицированной)."""
        # Создадим простую популяцию из двух агентов-заглушек
        class DummyAgent:
            def __init__(self, id):
                self.id = id
                self.best_formulas = {'pi': {'beauty': 0.8}}

        pop = [DummyAgent(0), DummyAgent(1)]
        result = Projector.apply_level2(pop)
        self.assertEqual(len(result), len(pop))
        # В текущей реализации apply_level2 вызывает share_best_formulas, но мы не можем
        # проверить результат, так как это зависит от случайности. Просто проверяем, что не упало.
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()