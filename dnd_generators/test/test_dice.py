from random import Random

from dnd_generators import Dice, D20


def test_dice():
    rng = Random(None)
    d6 = Dice(6, rng)
    d20 = D20(rng)

    result = (2 * d6) + (d20 + 4)
    print(result)
    print(int(result))


if __name__ == '__main__':
    test_dice()
