from dnd_generators import Dice, D20, CSVParser, BaseDisplayer
from dnd_generators.parser import parse_dice


def test_dice_parsing():
    t1 = 12 * Dice(6) + 25
    t2 = D20()
    t3 = D20() + 2*Dice(6)

    for t in t1, t2, t3:
        print(repr(t))
        print(str(t))
        r = parse_dice(str(t))
        print(repr(r))
        print()


def test_csv_parsing():
    fpath = "../adventure/dungeon.csv"
    displayer = BaseDisplayer()

    G = CSVParser().load(fpath)
    print(type(G))

    displayer(G)


if __name__ == '__main__':
    test_dice_parsing()
    test_csv_parsing()
