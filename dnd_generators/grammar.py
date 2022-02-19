import os
from collections import defaultdict
from random import Random

from .dice import Intable


class Tree:
    def __init__(self, symbol, parent=None):
        if isinstance(symbol, Intable):
            symbol = int(symbol)
        self.parent = parent
        self.symbol = symbol
        self.children = []

    def add_children(self, *children):
        for child in children:
            child.parent = self
            self.children.append(child)
        return self

    def __repr__(self):
        s = f"{self.__class__.__name__}({self.symbol})"
        if len(self.children) > 0:
            s += f".add_children(*{repr(self.children)})"
        return s

    def __iter__(self):
        return iter(self.children)


class ProductionRule:
    def __init__(self, weight, symbols):
        self.weight = weight
        self.symbols = symbols

    def __iter__(self):
        return iter(self.symbols)

    def __len__(self):
        return len(self.symbols)

    def __repr__(self):
        return f"{self.__class__.__name__}({repr(self.weight)}, {repr(self.symbols)})"


class ProductionSet:
    def __init__(self):
        self.rules = []

    def add_production_rules(self, *rules):
        self.rules.extend(rules)
        return self

    def add_production(self, weight, *symbols):
        rule = ProductionRule(weight, symbols)
        self.add_production_rules(rule)

    def __getitem__(self, flt):
        total_weight = 0
        for rule in self.rules:
            total_weight += rule.weight
        cap = total_weight * flt
        total_weight = 0
        for rule in self.rules:
            total_weight += rule.weight
            if total_weight > cap:
                return rule
        raise ValueError("Input must be in the range [0, 1).")

    def __len__(self):
        return len(self.rules)

    def __iter__(self):
        for rule in self.rules:
            yield rule.weight, tuple(rule)


class CFGrammar:
    def __init__(self, seed=None):
        self.production_sets = defaultdict(ProductionSet)
        self.rng = seed if isinstance(seed, Random) else Random(seed)

    def add_generative_rule(self, lhs, rhs_symbols, weight=1):
        prod_set = self.production_sets[lhs]
        prod_set.add_production(weight, *rhs_symbols)
        return self

    def add_rules(self, lhs, *weight_symbols_pairs):
        for weight, symbols in weight_symbols_pairs:
            self.add_generative_rule(lhs, symbols, weight)
        return self

    def generate(self, start_symbol):
        tree = Tree(start_symbol)

        production_set = self.production_sets[start_symbol]
        if len(production_set) > 0:
            flt = self.rng.random()
            p_rule = production_set[flt]
            for symbol in p_rule:
                tree.add_children(self.generate(symbol))

        return tree

    def __repr__(self):
        s = f"{self.__class__.__name__}({repr(self.rng)})"
        for lhs, prod_set in self.production_sets.items():
            for weight, symbols in prod_set:
                s += f".add_generative_rule({repr(lhs)}, {repr(symbols)}, {repr(weight)})"
        return s

    def __iter__(self):
        for lhs, prod_set in self.production_sets.items():
            for weight, symbols in prod_set:
                yield lhs, symbols, weight


