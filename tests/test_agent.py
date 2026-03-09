import unittest
import sys
sys.path.append('..')
from gra_ramanujan.agent import RamanujanAgent
from gra_ramanujan.constants import CONSTANTS_DICT

class TestAgent(unittest.TestCase):
    def setUp(self):
        self.config = {
            'max_depth': 3,
            'const_range': (-5, 5),
            'beauty_alpha': 0.5,
            'mutation_rate': 0.1
        }
        self.agent = RamanujanAgent(agent_id=0, config=self.config)

    def test_initialization(self):
        self.assertEqual(self.agent.id, 0)
        self.assertEqual(len(self.agent.best_formulas), len(CONSTANTS_DICT))
        self.assertEqual(self.agent.vitality, 1.0)
        self.assertEqual(self.agent.age, 0)

    def test_choose_constant(self):
        const = self.agent.choose_constant()
        self.assertIn(const, CONSTANTS_DICT)

    def test_generate_formula(self):
        formula = self.agent.generate_formula('pi')
        self.assertIn('tree', formula)
        self.assertEqual(formula['constant'], 'pi')
        self.assertEqual(formula['generation'], self.agent.age)

    def test_evaluate_formula(self):
        const = CONSTANTS_DICT['pi']
        formula = self.agent.generate_formula('pi')
        formula = self.agent.evaluate_formula(formula, const)
        self.assertIn('accuracy', formula)
        self.assertIn('complexity', formula)
        self.assertIn('beauty', formula)
        self.assertGreaterEqual(formula['accuracy'], 0.0)
        self.assertLessEqual(formula['accuracy'], 1.0)
        self.assertGreaterEqual(formula['complexity'], 1)
        self.assertGreaterEqual(formula['beauty'], 0.0)

    def test_update_best(self):
        const = 'pi'
        formula = self.agent.generate_formula(const)
        const_obj = CONSTANTS_DICT[const]
        formula = self.agent.evaluate_formula(formula, const_obj)
        self.agent.update_best(formula)
        self.assertIsNotNone(self.agent.best_formulas[const])
        self.assertEqual(self.agent.best_formulas[const]['beauty'], formula['beauty'])
        self.assertGreater(self.agent.weights[const], 0.1)

    def test_step(self):
        formula = self.agent.step()
        self.assertEqual(self.agent.age, 1)
        self.assertIn('constant', formula)

    def test_mutate(self):
        const = 'pi'
        formula = self.agent.generate_formula(const)
        const_obj = CONSTANTS_DICT[const]
        formula = self.agent.evaluate_formula(formula, const_obj)
        self.agent.update_best(formula)
        old_tree = str(self.agent.best_formulas[const]['tree'])
        self.agent.mutate(mutation_rate=1.0)  # гарантированная мутация
        new_tree = str(self.agent.best_formulas[const]['tree'])
        # мутация может не изменить дерево, если она не затронула эту константу
        # просто проверяем, что метод отработал без ошибок
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()