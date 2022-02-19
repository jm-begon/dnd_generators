from .grammar import CFGrammar
from .display import BaseDisplayer
from .dice import Dice, D20
from .parser import CSVParser


def init_grammar(sep=";", symbol_sep="&&", seed=None):
    import os
    folder = os.path.dirname(__file__)

    gram_files = [
        "adventure/dungeon.csv",
    ]

    grammar = None
    parser = CSVParser(sep, symbol_sep, seed)
    for file in gram_files:
        fpath = os.path.join(folder, file)
        grammar = parser.load(fpath, grammar)

    return grammar


__version__ = "0.0.dev"
__all__ = ["CFGrammar", "BaseDisplayer", "Dice", "D20", "CSVParser",
           "init_grammar"]


