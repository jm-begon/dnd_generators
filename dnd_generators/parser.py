import re
from random import Random

from .dice import Dice, D20, Add
from .grammar import CFGrammar

RE_DICE = re.compile(r"(\d*)d(\d+)|(\d+)")


def parse_dice(s, seed=None):
    terms = []
    for part in s.split("+"):
        part = part.strip()
        ans = RE_DICE.match(part)
        if ans is not None:
            mult, n_faces, add = ans.groups()
            if n_faces is None:
                terms.append(int(add))
                continue
            n_faces = int(n_faces)
            term = Dice(n_faces, seed) if n_faces != 20 else D20(seed)
            if mult is not None and len(mult) > 0:
                term = int(mult) * term
            if add is not None:
                term = term + int(add)

            terms.append(term)

    if len(terms) == 1:
        return terms[0]

    return Add(*terms)


class CSVParser:
    def __init__(self, sep=";", symbol_sep="&&", seed=None):
        self.sep = sep
        self.symbol_sep = symbol_sep
        self.rng = seed if isinstance(seed, Random) else Random(seed)

    def load(self, fpath, grammar=None):
        if grammar is None:
            grammar = CFGrammar(self.rng)

        with open(fpath) as file:
            for i, line in enumerate(file):
                if i == 0 or len(line) == 0:
                    continue  # Skip header
                lhs, weight, rhs = [x.strip() for x in line.split(self.sep)]

                weight = 1 if len(weight) == 0 else float(weight)

                rhs_ls = []
                for symbol in rhs.split(self.symbol_sep):
                    symbol = symbol.strip()
                    if symbol.startswith("dice_"):
                        symbol = parse_dice(symbol[5:], self.rng)
                    rhs_ls.append(symbol)

                grammar.add_generative_rule(lhs, rhs_ls, weight)

        return grammar

    def dump(self, fpath, grammar):
        with open(fpath, "w") as hdl:
            def writeln(*stuff):
                line = self.sep.join(stuff)
                hdl.write(f"{line}\n")

            writeln("Generative symbol", "Weight", "Generated symbols")

            for lhs, symbols, weight in grammar:
                writeln(lhs, weight, " ".join(symbols))
                # Should take care of dice as well



