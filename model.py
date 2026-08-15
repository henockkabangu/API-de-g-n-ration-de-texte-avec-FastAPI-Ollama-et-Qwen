import requests


# ============================================================
# CONFIGURATION OLLAMA / QWEN
# ============================================================

OLLAMA_URL = "http://host.docker.internal:11434/api/generate"

MODEL_NAME = "qwen2.5:0.5b"


# ============================================================
# FONCTION PRINCIPALE
# ============================================================

def generate_response(question: str, context: str = "") -> str:
    """
    Génère une réponse avec Qwen à partir de la question
    et des informations récupérées dans le corpus.
    """

    prompt = f"""
Tu es un assistant lexical bilingue Tshiluba-Français.

Ta tâche est d'aider l'utilisateur à comprendre les termes
Tshiluba et Français.

IMPORTANT :
- Le contexte fourni provient de notre corpus linguistique.
- Utilise prioritairement ces informations.
- Ne crée pas une traduction qui n'est pas présente dans
  le contexte.
- Si l'information demandée n'est pas disponible dans le
  contexte, indique clairement que le corpus ne contient
  pas cette information.
- Tu peux expliquer ou reformuler une information trouvée.
- Réponds en français, de manière claire et concise.

========================
CONTEXTE DU CORPUS
========================

{context}

========================
QUESTION DE L'UTILISATEUR
========================

{question}

========================
RÉPONSE
========================
"""

    try:

        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False
            },
            timeout=120
        )

        response.raise_for_status()

        data = response.json()

        return data.get(
            "response",
            "Qwen n'a retourné aucune réponse."
        ).strip()

    except requests.exceptions.ConnectionError:

        return (
            "Impossible de contacter Ollama. "
            "Vérifiez que Ollama est démarré et que "
            "le modèle qwen2.5:0.5b est disponible."
        )

    except requests.exceptions.Timeout:

        return (
            "Le délai d'attente de Qwen a été dépassé."
        )

    except requests.exceptions.RequestException as e:

        return (
            f"Erreur lors de la communication avec Ollama : {e}"
        )


# ============================================================
# TEST DIRECT DU MODÈLE
# ============================================================

if __name__ == "__main__":

    question = "Explique simplement le terme maison."

    context = """
Tshiluba : nzubu
Français : maison
"""

    response = generate_response(
        question,
        context
    )

    print("\nQUESTION :")
    print(question)

    print("\nRÉPONSE DE QWEN :")
    print(response)
