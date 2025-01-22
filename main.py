import csv
from itertools import combinations

def read_csv(file_path):
    """
    Lit un fichier CSV contenant les transactions, séparées par des virgules, 
    et retourne une liste de transactions où chaque transaction est un ensemble d'items.
    
    :param file_path: Chemin vers le fichier CSV.
    :return: Liste de transactions (chaque transaction est un ensemble d'items).
    """
    transactions = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            # Convertir chaque ligne du fichier en un ensemble d'items
            transactions.append(set(row))
    return transactions

def calculate_support(transactions, itemset):
    """
    Calcule le support d'un ensemble d'items (itemset) dans les transactions.
    Le support est la proportion de transactions contenant l'ensemble d'items.

    :param transactions: Liste des transactions.
    :param itemset: Ensemble d'items dont on souhaite calculer le support.
    :return: Support (valeur entre 0 et 1).
    """
    count = sum(1 for transaction in transactions if itemset.issubset(transaction))
    return count / len(transactions)

def generate_candidates(itemsets, length):
    """
    Génère les candidats de taille donnée à partir des ensembles fréquents existants.
    
    :param itemsets: Liste des ensembles fréquents actuels.
    :param length: Taille des ensembles candidats à générer.
    :return: Liste des ensembles candidats.
    """
    all_items = set()
    for itemset in itemsets:
        # Collecte tous les items uniques des ensembles actuels
        all_items.update(itemset)
    # Génère toutes les combinaisons possibles de la taille spécifiée
    return [set(combination) for combination in combinations(all_items, length)]

def apriori(transactions, min_support):
    """
    Implémente l'algorithme Apriori pour extraire les ensembles d'items fréquents 
    et leurs supports à partir d'un ensemble de transactions.

    :param transactions: Liste des transactions.
    :param min_support: Support minimum pour qu'un ensemble soit considéré fréquent.
    :return: Liste des ensembles fréquents avec leurs supports.
    """
    # Génère les ensembles d'items uniques (1-itemsets)
    itemsets = [set([item]) for transaction in transactions for item in transaction]
    # Supprime les doublons en utilisant des tuples pour rendre les ensembles hashables
    itemsets = list(map(set, set(map(tuple, itemsets))))
    frequent_itemsets = []
    
    k = 1
    while itemsets:
        itemset_support = {}
        for itemset in itemsets:
            # Calcule le support de chaque ensemble
            support = calculate_support(transactions, itemset)
            if support >= min_support:
                # Conserve les ensembles fréquents avec leur support
                itemset_support[frozenset(itemset)] = support
        
        frequent_itemsets.extend(itemset_support.items())
        # Génère les candidats pour le prochain niveau
        k += 1
        itemsets = generate_candidates(list(itemset_support.keys()), k)

    return frequent_itemsets

def generate_rules(frequent_itemsets, transactions, min_confidence):
    """
    Génère les règles d'association à partir des ensembles fréquents en calculant la confiance.

    :param frequent_itemsets: Liste des ensembles fréquents avec leurs supports.
    :param transactions: Liste des transactions.
    :param min_confidence: Confiance minimale pour qu'une règle soit acceptée.
    :return: Liste des règles sous forme de tuples (antécédent, conséquent, confiance).
    """
    rules = []
    for itemset, support in frequent_itemsets:
        # Génère tous les sous-ensembles possibles de l'ensemble fréquent
        subsets = [set(x) for i in range(1, len(itemset)) for x in combinations(itemset, i)]
        for subset in subsets:
            # Identifie les items restants
            remaining = itemset - subset
            if remaining:
                # Calcule la confiance de la règle
                confidence = calculate_support(transactions, itemset) / calculate_support(transactions, subset)
                if confidence >= min_confidence:
                    # Ajoute la règle si elle respecte le seuil de confiance
                    rules.append((subset, remaining, confidence))
    return rules

def main():
    """
    Point d'entrée principal du programme. Lit les transactions, applique l'algorithme Apriori 
    et génère les règles d'association.
    """
    file_path = 'exemple1.csv'  # Chemin du fichier CSV contenant les transactions
    min_support = 0.5          # Support minimum pour les ensembles fréquents
    min_confidence = 1.0       # Confiance minimale pour les règles

    # Lit les transactions à partir du fichier CSV
    transactions = read_csv(file_path)

    # Applique l'algorithme Apriori pour trouver les ensembles fréquents
    frequent_itemsets = apriori(transactions, min_support)

    # Génère les règles d'association à partir des ensembles fréquents
    rules = generate_rules(frequent_itemsets, transactions, min_confidence)

    # Affiche les règles générées
    print("Règles d'association :")
    for antecedent, consequent, confidence in rules:
        print(f"{set(antecedent)} => {set(consequent)} (Confiance : {confidence * 100:.2f}%)")

if __name__ == "__main__":
    main()
