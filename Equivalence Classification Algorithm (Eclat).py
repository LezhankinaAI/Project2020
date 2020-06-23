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


def getantecendent(FreqItems, confidence):
    ant = []
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
                        ant.append((antecedent))
    return ant


def print_Frequent_Itemsets(output_FreqItems, FreqItems):
    file = open(output_FreqItems, 'w+')
    for item, support in FreqItems.items():
        file.write(" {} : {} \n".format(list(item), round(support, 4)))


def print_rules(output_Rules, Rules):
    file = open(output_Rules, 'w+')
    for a, b, supp, conf, lift in sorted(Rules):
        file.write(
            "{} ==> {} support: {} confidence: {} \n".format((a), (b), round(supp, 4), round(conf, 4), round(lift, 4)))
    file.close()


def read_data(filename, delimiter):
    data = {}
    trans = 0
    f = open(filename, 'r', encoding="utf8").read().split('\n')
    for row in f:
        trans += 1
        for item in row.split(delimiter):
            if item not in data:
                data[item] = set()
            data[item].add(trans)
    return data


if __name__ == "__main__":
    minsup = 2
    confidence = 60
    output_FreqItems = 'TID.csv'
    output_Rules = 'RULES.csv'
    dict_id = 0
    data = read_data('input.txt', ' ')  # change the delimiter based on your input file
    eclat([], sorted(data.items(), key=lambda item: len(item[1]), reverse=True), dict_id)
    Rules = rules(FreqItems, confidence)

    print_Frequent_Itemsets(output_FreqItems, FreqItems)
    print_rules(output_Rules, Rules)
    Antecendent = getantecendent(FreqItems, confidence)

    Ant1d = np.hstack(Antecendent)

    count = np.array(Ant1d)
    unique, counts = np.unique(count, return_counts=True)
    dict(zip(unique, counts))
    counted = np.stack((unique, counts), axis=1)
    appendFile = open('candidate.csv', 'w')
    for i in range(0, len(counted)):
        appendFile.write(str(unique[i]) + ";" + str(counts[i]) + "," + "\n")
    appendFile.close()

    df = pd.DataFrame(counted, columns=['word', 'counter'])
    df["counter"] = pd.to_numeric(df["counter"])
    sortcounted = df.sort_values(["counter"], axis=0,
                                 ascending=[False])
    elimcounted = sortcounted.drop(sortcounted[sortcounted['counter'] < 2].index)

    listfrequent = list(elimcounted.iloc[:, 0].values)