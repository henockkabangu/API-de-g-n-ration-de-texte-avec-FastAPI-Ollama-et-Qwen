
# Assistant intelligent lexical bilingue Tshiluba–Français

Ce projet consiste à développer un assistant intelligent lexical bilingue Tshiluba–Français permettant de rechercher un mot en français pour obtenir son équivalent en Tshiluba, ou inversement. Le système peut également fournir les informations linguistiques disponibles dans le corpus, expliquer un terme et générer un exemple lorsque cela est pertinent.

Le fonctionnement repose sur une combinaison entre **recherche lexicale et modèle de langage. Le corpus constitue la principale source d'informations linguistiques : il contient notamment les colonnes `CILUBA`, `FRANCAIS`, `SCORE`, `SENTIMENT` et `NATURE`. Après nettoyage, le corpus est passé de 2 982 lignes à 2 388 paires uniques, après identification de 592 doublons.

L'architecture n'est donc pas simplement `Utilisateur → Qwen → Réponse`. La requête est d'abord traitée par l'application et recherchée dans le corpus. Lorsque cela est nécessaire, Qwen2.5:0.5B, exécuté localement avec Ollama, intervient pour comprendre la demande, expliquer une information, reformuler un résultat ou générer un exemple. Cette approche permet de limiter les réponses non fondées et le risque d'hallucination du modèle.

L'API du système est développée avec Python et FastAPI, tandis que l'accès aux fonctionnalités est exposé à travers une API REST. Lorsque l'authentification est activée, JWT permet de sécuriser l'accès aux ressources protégées.

Le système vise principalement les fonctionnalités suivantes :

-  Recherche Français → Tshiluba ;
- Recherche Tshiluba → Français ;
-  Recherche d'un terme dans le corpus ;
- Consultation des informations linguistiques disponibles ;
-  Explication d'un terme ;
-  Génération d'exemples lorsque les données disponibles le permettent ;
- Signalement d'un terme absent du corpus au lieu d'inventer une traduction.

> Important :le système actuel est principalement un assistant lexical bilingue et non un système complet de traduction automatique neuronale de phrases. Ses capacités dépendent directement de la couverture et de la qualité du corpus.

À terme, le projet pourra être amélioré par l'enrichissement du corpus avec des phrases et expressions, la validation linguistique par des locuteurs compétents, la recherche sémantique, l'intégration d'une approche RAG, l'adaptation d'un modèle par LoRA/Fine-tuning, ainsi que l'ajout de fonctionnalités vocales et d'une interface web ou mobile.
