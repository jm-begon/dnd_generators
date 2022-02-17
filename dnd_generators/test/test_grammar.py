from dnd_generators import CFGrammar
from dnd_generators import BaseDisplayer


def make_grammar():
    G = CFGrammar(seed=None)
    s = "dungeon"
    G.add_generative_rule(
        "dungeon",
        ["dungeon_location", "dungeon_creator",
         "dungeon_purpose", "dungeon_history"],
    ).add_rules(
        "dungeon_location",
        (4, ["A building in a city"]),
        (4, ["Catacombs or sewers beneath a city"]),
        (5, ["dungeon_location_exotic"]),
    ).add_rules(
        "dungeon_location_exotic",
        (1, ["Among the branches of a tree"]),
        (1, ["On a cloud"])
    ).add_rules(
        "dungeon_creator",
        (1, ["No creator (natural place)"]),
        (4, ["Dwarves"]),
        (3, ["cultist_creator"])
    ).add_rules(
        "cultist_creator",
        (2, ["Elemental water cultists"]),
        (5, ["Worshipers of an evil god"])
    ).add_rules(
        "dungeon_purpose",
        (3, ["Death trap"]),
        (1, ["Treasure vault"]),
        (3, ["Mine"])
    ).add_rules(
        "dungeon_history",
        (4, ["Abandoned by creators"]),
        (1, ["Destroyed by a discovery made within the site"])
    )

    return s, G


def test_grammar_repr():
    _, G = make_grammar()
    displayer = BaseDisplayer()
    displayer(G)


def test_tree():
    s, G = make_grammar()

    tree = G.generate(s)

    displayer = BaseDisplayer()
    displayer(tree)


if __name__ == '__main__':
    # TODO real tests
    test_grammar_repr()
    test_tree()
