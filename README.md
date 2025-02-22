# Apriori

## Description
Ce projet implémente l'algorithme Apriori pour extraire des règles d'association à partir d'un fichier CSV contenant des transactions. Il calcule les itemsets fréquents et génère des règles de confiance basées sur des seuils minimums spécifiés pour le support et la confiance.

## Utilisation
1. **Préparer le fichier CSV** :
   - Créez un fichier CSV contenant vos transactions.
   - Exemple de fichier `transactions.csv` :
     ```csv
     A,B,C
     B,C,E
     A,B,E
     B,E
     A,C,D
     ```

2. **Modifier les paramètres** :
   - Ouvrez le fichier `main.py`.
   - Ajustez les valeurs des paramètres `min_support` et `min_confidence` selon vos besoins dans la fonction `main()` :
     ```python
     min_support = 0.5  # Exemple : support minimum de 50%
     min_confidence = 1.0  # Exemple : confiance minimum de 100%
     ```

3. **Exécuter le script** :
   - Lancez le script à partir du terminal ou de l'IDE :
     ```bash
     python main.py
     ```

4. **Consulter les résultats** :
   - Le script affichera les règles générées avec leurs niveaux de confiance dans la console.

## Exemple de sortie
```text
Rules:
{'B'} => {'E'} (Confidence: 100.00%)
{'E'} => {'B'} (Confidence: 75.00%)
{'B', 'C'} => {'E'} (Confidence: 100.00%)
```

## Notes
- **Seuils** : Les seuils `min_support` et `min_confidence` permettent de filtrer les règles générées. Adaptez-les en fonction de vos besoins pour ajuster les résultats.
- **Format CSV** : Assurez-vous que chaque transaction est représentée par une ligne et que les items sont séparés par des virgules.

