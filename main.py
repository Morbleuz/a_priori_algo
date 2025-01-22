import csv
from itertools import combinations

def read_csv(file_path):
    """
    Lire un fichier CSV séparé par des virgules.
    """
    transactions = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            transactions.append(set(row))
    return transactions

def calculate_support(transactions, itemset):
    """Calcule le support"""
    count = sum(1 for transaction in transactions if itemset.issubset(transaction))
    return count / len(transactions)

def generate_candidates(itemsets, length):
    """
    Generate candidate itemsets of a given length.
    """
    all_items = set()
    for itemset in itemsets:
        all_items.update(itemset)  # Collect all items from the itemsets
    return [set(combination) for combination in combinations(all_items, length)]

def apriori(transactions, min_support):
    """
    Apriori algorithm to generate frequent itemsets.
    Returns frequent itemsets with their supports.
    """
    itemsets = [set([item]) for transaction in transactions for item in transaction]
    itemsets = list(map(set, set(map(tuple, itemsets))))  # Unique 1-itemsets
    frequent_itemsets = []
    
    k = 1
    while itemsets:
        itemset_support = {}
        for itemset in itemsets:
            support = calculate_support(transactions, itemset)
            if support >= min_support:
                itemset_support[frozenset(itemset)] = support
        
        frequent_itemsets.extend(itemset_support.items())
        k += 1
        itemsets = generate_candidates(list(itemset_support.keys()), k)

    return frequent_itemsets

def generate_rules(frequent_itemsets, transactions, min_confidence):
    """
    Generate confidence rules from frequent itemsets.
    """
    rules = []
    for itemset, support in frequent_itemsets:
        subsets = [set(x) for i in range(1, len(itemset)) for x in combinations(itemset, i)]
        for subset in subsets:
            remaining = itemset - subset
            if remaining:
                confidence = calculate_support(transactions, itemset) / calculate_support(transactions, subset)
                if confidence >= min_confidence:
                    rules.append((subset, remaining, confidence))
    return rules

def main():
    file_path = 'exemple1.csv'
    min_support = 0.5
    min_confidence = 1.0

    transactions = read_csv(file_path)

    frequent_itemsets = apriori(transactions, min_support)

    rules = generate_rules(frequent_itemsets, transactions, min_confidence)

    print("Rules:")
    for antecedent, consequent, confidence in rules:
        print(f"{set(antecedent)} => {set(consequent)} (Confidence: {confidence * 100:.2f}%)")

if __name__ == "__main__":
    main()