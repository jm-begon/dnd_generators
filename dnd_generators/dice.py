from random import Random


class Intable:
    def __int__(self):
        return 0

    def __radd__(self, other):
        return Add(other, self)

    def __add__(self, other):
        return Add(self, other)

    def __rmul__(self, other):
        return Multiply(other, self)

    def __mul__(self, other):
        return Multiply(self, other)


class RandomNumber(Intable):
    def __init__(self, seed=None):
        self.rng = seed if isinstance(seed, Random) else Random(seed)


class Dice(RandomNumber):
    def __init__(self, sides, seed=None):
        super().__init__(seed)
        self.sides = sides

    def __int__(self):
        return self.rng.randint(1, self.sides)

    def __repr__(self):
        return f"{self.__class__.__name__}({repr(self.sides)}, " \
               f"{repr(self.rng)})"

    def __str__(self):
        return f"d{self.sides}"


class D20(Dice):
    def __init__(self, seed=None):
        super(D20, self).__init__(sides=20, seed=seed)
        # TODO advantage/disavantage

    def __repr__(self):
        return f"{self.__class__.__name__}({repr(self.rng)})"


class Operator(Intable):
    pass


class Add(Operator):
    def __init__(self, *operands):
        self.operands = operands

    def __int__(self):
        return sum(int(x) for x in self.operands)

    def __repr__(self):
        return f"{self.__class__.__name__}(*{repr(self.operands)})"

    def __str__(self):
        return "+".join(str(x) for x in self.operands)


class Multiply(Operator):
    def __init__(self, scalar, intable):
        self.scalar = scalar
        self.intable = intable

    def __int__(self):
        return self.scalar * int(self.intable)

    def __repr__(self):
        return f"{self.__class__.__name__}({repr(self.scalar)}, {repr(self.intable)})"

    def __str__(self):
        return f"{self.scalar}{str(self.intable)}"

