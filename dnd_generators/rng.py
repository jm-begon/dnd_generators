# import random; random.seed(42)
from collections import namedtuple
from random import Random


class RNG(Random):
    __instances__ = {}

    @classmethod
    def get(cls, name=None, seed=None):
        inst = cls.__instances__.get(name)
        if inst is None:
            inst = cls(name)
            cls.__instances__[name] = inst
        if seed is not None:
            inst.seed(seed)
        return inst

    def __init__(self, name, seed=None):
        super().__init__(seed)
        self.__class__.__instances__[name] = self


class Stochastic:
    def __init__(self, rng_name="default"):
        self._rng = RNG.get(rng_name)

    @property
    def rng(self):
        return self._rng

    def set_rng(self, rng):
        self._rng = rng
        return self


class RandomNumber(Stochastic):
    def __int__(self):
        return int(float(self))

    def __float__(self):
        return 0.

    def __call__(self, *args, **kwargs):
        return float(self)


class Dice(RandomNumber):
    def __init__(self, sides, rng_name="default"):
        super().__init__(rng_name)
        self.sides = sides

    def __float__(self):
        return self.rng.drawint(1, self.sides)

    def __repr__(self):
        return f"{self.__class__.__name__}({repr(self.sides)}, " \
               f"{repr(self.rng)})"

    def __str__(self):
        return f"d{self.sides}"


class D20(Dice):
    def __init__(self, rng_name="default"):
        super(D20, self).__init__(sides=20, rng_name=rng_name)
        # TODO advantage/disavantage

    def __repr__(self):
        return f"{self.__class__.__name__}({repr(self.rng)})"


class Choice(Stochastic):
    @classmethod
    def from_csv(cls, fpath, name=None, sep=";", rng_name='default', **kwargs):
        import pandas as pd
        df = pd.read_csv(fpath, sep=sep, **kwargs)
        if len(df.columns) == 1:
            return cls(*list(df[df.columns[0]]))
        if name is None:
            import os
            name = os.path.splitext(os.path.basename(fpath))[0]
            name = name.lower().replace("-", "_").capitalize()
        Tuple = namedtuple(name, df.columns)
        return cls(*[map(lambda ir: Tuple(*ir[1]), df)], rng_name=rng_name)

    def __init__(self, *alternatives, rng_name='default'):
        super(Choice, self).__init__(rng_name)
        self.alternatives = list(alternatives)

    def __call__(self, *args, **kwargs):
        return self.rng.choice(self.alternatives)


class Outcome(Stochastic):
    def __init__(self, decorated, rng_name="default"):
        super(Outcome, self).__init__(rng_name)
        self.decorated = decorated
        self.value = None

    def set_value(self, v):
        self.value = v
        return self

    def unset(self):
        self.value = None
        return self

    def __repr__(self):
        s = f"{self.__class__.__name__}({repr(self.decorated)})"
        if self.value is not None:
            s += f".set_value({self.value})"
        return s

    def __str__(self):
        if self.value is None:
            return str(self.decorated)
        return f"{self.value} ({self.decorated})"

    def __getattr__(self, item):
        old = self.decorated.rng
        try:
            self.decorated.set_rng(self.rng)
            ans = getattr(self.decorated, item)
        finally:
            self.decorated.set_rng(old)
        return ans

    def _make_lazy(self, fn_str):
        def lazy(*args, **kwargs):
            if self.value is not None:
                return self.value

            value = getattr(self, fn_str)(*args, **kwargs)
            self.set_value(value)
            return value
        return lazy

    def __int__(self):
        return self._make_lazy("__int__")()

    def __float__(self):
        return self._make_lazy("__float__")()

    def __call__(self, *args, **kwargs):
        return self._make_lazy("__call__")(*args, **kwargs)




