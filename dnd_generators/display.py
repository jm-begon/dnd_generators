import sys
import os

from .grammar import CFGrammar, Tree


class BaseDisplayer:
    def __init__(self, indent_size=2, stream=sys.stdout):
        self.stream = stream
        self.indent_format = " "*indent_size

    def __call__(self, stuff):
        if isinstance(stuff, CFGrammar):
            self.stream.write(self.cfgrammar_to_string(stuff))
        elif isinstance(stuff, Tree):
            self.stream.write(self.tree_2_string(stuff))
        else:
            raise ValueError(f"Ignore what to do with {stuff}")

        self.stream.write(os.linesep)

    def cfgrammar_to_string(self, grammar):
        ls = []
        for lhs, prod_set in grammar.production_sets.items():
            pre = f"{lhs} --> "
            for weight, symbols in prod_set:
                s = pre + " ".join(symbols) + f" ({weight})"
                pre = " " * len(pre)
                ls.append(s)

        return os.linesep.join(ls)

    def tree_2_string(self, tree, indent=0):
        children_array = [self.tree_2_string(child, indent + 1) for child in tree]
        if len(children_array) > 0:
            children_array = [""] + children_array
        children_str = os.linesep.join(children_array)
        return self.indent_format * indent + str(tree.symbol) + children_str
