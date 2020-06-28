import numpy as np, itertools
import pandas as pd

np.random.seed(42)
FreqItems = dict()
support = dict()


def eclat(prefix, items, dict_id):
    while items:
        i, itids = items.pop()
        isupp = len(itids)
        if isupp >= minsup:

            FreqItems[frozenset(prefix + [i])] = isupp
            suffix = []
            for j, ojtids in items:
                jtids = itids & ojtids
                if len(jtids) >= minsup:
                    suffix.append((j, jtids))

            dict_id += 1
            eclat(prefix + [i], sorted(suffix, key=lambda item: len(item[1]), reverse=True), dict_id)


def rules(FreqItems, confidence):
    Rules = []
    cnt = 0

    for items, support in FreqItems.items():
        if (len(items) > 1):
            all_perms = list(itertools.permutations(items, len(items)))
            for lst in all_perms:
                antecedent = lst[:len(lst) - 1]
                consequent = lst[-1:]

                conf = float(FreqItems[frozenset(items)] / FreqItems[frozenset(antecedent)] * 100)
                if (conf >= confidence):
                    cnt += 1
                    lift = float(conf / FreqItems[frozenset(consequent)])
                    if lift >= 1:
                        Rules.append((antecedent, consequent, support, conf, lift))
    return Rules
