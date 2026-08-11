# API de génération de texte avec FastAPI, Ollama et Qwen

## 1. Description du projet

Ce projet consiste à développer une API REST de génération de texte basée sur un modèle de langage (LLM).

L'API est développée avec **FastAPI** et communique avec **Ollama**, qui assure l'exécution locale du modèle **Qwen2.5 0.5B**.

L'objectif principal est de mettre en place une architecture simple permettant à une application cliente d'envoyer un prompt à l'API et de recevoir une réponse générée automatiquement par le modèle de langage.

Le projet utilise également **Docker** afin d'isoler et d'exécuter l'API dans un conteneur.

### Fonctionnement général

Le fonctionnement est le suivant :

Client
↓
FastAPI
↓
model.py
↓
Ollama API
↓
Qwen2.5 0.5B
↓
Réponse générée
↓
FastAPI
↓
Client

---

## 2. Objectifs du projet

Les objectifs sont :

- Concevoir une API REST avec FastAPI.
- Mettre en place un endpoint d'authentification.
- Mettre en place un endpoint de génération de texte.
- Intégrer un modèle de langage local.
- Utiliser Ollama pour exécuter le modèle Qwen.
- Conteneuriser l'API avec Docker.
- Permettre la communication entre le conteneur Docker et Ollama exécuté dans WSL.
- Tester l'API à travers Swagger UI.
- Retourner les réponses générées au format JSON.

---

## 3. Technologies utilisées

| Technologie | Rôle |
|---|---|
| Python 3.11 | Langage de programmation |
| FastAPI     | Framework pour développer l'API REST |
| Uvicorn     | Serveur ASGI utilisé pour exécuter FastAPI |
| Docker      | Conteneurisation de l'API |
| Ollama      | Serveur local d'exécution du LLM |
| Qwen2.5 0.5B | Modèle de langage utilisé |
| Requests    | Communication entre FastAPI et Ollama |
| WSL2        | Environnement Linux utilisé pour Ollama |
| Swagger UI  | Documentation et test de l'API |

---

## 4. Architecture du projet

L'architecture est composée de deux parties principales.

### 4.1. Conteneur Docker

L'API FastAPI fonctionne dans un conteneur Docker :

```text
Docker
└── llm_api
    ├── FastAPI
    ├── Uvicorn
    ├── app.py
    └── model.py