import math
from mpmath import mp, zeta, catalan, euler, pi, e, phi

mp.dps = 50

class Constant:
    def __init__(self, name, category, value_func, latex=None):
        self.name = name
        self.category = category
        self.value_func = value_func
        self.latex = latex or name

    def value(self, dps=None):
        if dps is not None:
            with mp.workdps(dps):
                return self.value_func()
        return self.value_func()

CONSTANTS = [
    Constant('pi', 'math', lambda: mp.pi, r'\pi'),
    Constant('e', 'math', lambda: mp.e, r'e'),
    Constant('phi', 'math', lambda: mp.phi, r'\phi'),
    Constant('gamma', 'math', lambda: mp.euler, r'\gamma'),
    Constant('zeta2', 'math', lambda: zeta(2), r'\zeta(2)'),
    Constant('zeta3', 'math', lambda: zeta(3), r'\zeta(3)'),
    Constant('catalan', 'math', lambda: catalan, r'G'),
]

CONSTANTS_DICT = {c.name: c for c in CONSTANTS}