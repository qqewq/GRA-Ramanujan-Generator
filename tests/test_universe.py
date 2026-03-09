import unittest
import sys
import os
import tempfile
import shutil
sys.path.append('..')
from gra_ramanujan.universe import GRAUniverse
from gra_ramanujan.constants import CONSTANTS, Constant

class TestUniverse(unittest.TestCase):
    def setUp(self):
        # Создаём временную директорию для логов
        self.test_dir = tempfile.mkdtemp()
        # Перенаправляем создание логов во временную папку
        import gra_ramanujan.utils
        original_init_logs = gra_ramanujan.utils.init_logs
        original_log_conjecture = gra_ramanujan.utils.log_conjecture
        original_log_machine = gra_ramanujan.utils.log_machine

        def fake_init_logs():
            # ничего не делаем, файлы не создаём
            pass

        def fake_log_conjecture(*args, **kwargs):
            pass

        def fake_log_machine(*args, **kwargs):
            pass

        gra_ramanujan.utils.init_logs = fake_init_logs
        gra_ramanujan.utils.log_conjecture = fake_log_conjecture
        gra_ramanujan.utils.log_machine = fake_log_machine

        self.addCleanup(setattr, gra_ramanujan.utils, 'init_logs', original_init_logs)
        self.addCleanup(setattr, gra_ramanujan.utils, 'log_conjecture', original_log_conjecture)
        self.addCleanup(setattr, gra_ramanujan.utils, 'log_machine', original_log_machine)

        # Конфигурация для тестов
        self.config = {
            'lambda0': 1.0,
            'lambda1': 0.5,
            'lambda2': 0.2,
            'death_threshold': 0.3,
            'mutation_rate': 0.1,
            'max_depth': 3,
            'const_range': (-5, 5),
            'beauty_alpha': 0.5,
            'share_prob': 0.1
        }
        # Используем только несколько констант для скорости
        self.test_constants = [c for c in CONSTANTS if c.name in ('pi', 'e')]

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_creation(self):
        universe = GRAUniverse(num_agents=5, config=self.config, constants=self.test_constants)
        self.assertEqual(len(universe.agents), 5)
        self.assertEqual(universe.generation, 0)
        self.assertEqual(len(universe.history), 0)
        self.assertEqual(universe.constants, self.test_constants)

    def test_step(self):
        universe = GRAUniverse(num_agents=3, config=self.config, constants=self.test_constants)
        universe.step()
        self.assertEqual(universe.generation, 1)
        self.assertEqual(len(universe.history), 1)
        self.assertIsInstance(universe.history[0], float)

    def test_multiple_steps(self):
        universe = GRAUniverse(num_agents=3, config=self.config, constants=self.test_constants)
        for i in range(5):
            universe.step()
        self.assertEqual(universe.generation, 5)
        self.assertEqual(len(universe.history), 5)

    def test_update_vitality(self):
        universe = GRAUniverse(num_agents=2, config=self.config, constants=self.test_constants)
        # Сохраняем начальную витальность
        initial_vitalities = [a.vitality for a in universe.agents]
        # Вызываем step, который внутри вызывает update_vitality
        universe.step()
        # Проверяем, что витальность изменилась (не обязательно увеличилась, но изменилась)
        new_vitalities = [a.vitality for a in universe.agents]
        for i in range(len(universe.agents)):
            self.assertNotEqual(initial_vitalities[i], new_vitalities[i])

    def test_selection_death(self):
        # Создаём агентов с очень низкой витальностью, чтобы они умерли
        universe = GRAUniverse(num_agents=3, config=self.config, constants=self.test_constants)
        for a in universe.agents:
            a.vitality = 0.1  # ниже death_threshold = 0.3
        universe.selection()
        self.assertEqual(len(universe.agents), 0)

    def test_selection_survival(self):
        # Агенты с высокой витальностью должны выжить
        universe = GRAUniverse(num_agents=3, config=self.config, constants=self.test_constants)
        for a in universe.agents:
            a.vitality = 0.9
        universe.selection()
        self.assertEqual(len(universe.agents), 3)

    def test_selection_reproduction(self):
        # Проверяем, что после удаления популяция восполняется до num_agents
        universe = GRAUniverse(num_agents=3, config=self.config, constants=self.test_constants)
        # Убиваем одного агента
        universe.agents[0].vitality = 0.1
        universe.selection()
        # Должно остаться 2
        self.assertEqual(len(universe.agents), 2)
        # После selection вызывается восполнение внутри step, но мы вызываем только selection
        # Так что population не восстановится. Проверим восстановление через step
        # Сбросим
        universe = GRAUniverse(num_agents=3, config=self.config, constants=self.test_constants)
        universe.agents[0].vitality = 0.1
        universe.step()  # step включает selection и восполнение
        self.assertEqual(len(universe.agents), 3)  # опять 3 агента

    def test_known_identities(self):
        # Проверяем, что можно передать known_identities (пока ничего не делает, но не падает)
        def dummy_identity(formulas_dict):
            return 0.0
        universe = GRAUniverse(num_agents=2, config=self.config, constants=self.test_constants,
                               known_identities=[dummy_identity])
        universe.step()
        self.assertEqual(universe.generation, 1)

if __name__ == '__main__':
    unittest.main()