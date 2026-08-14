import requests


# =========================
# CONFIGURATION
# =========================

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5:0.5b"


# =========================
# APPEL À QWEN
# =========================

def generate_text(prompt: str) -> str:
    """
    Envoie une demande à Qwen via Ollama
    et retourne le texte généré.
    """

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=120
        )

        response.raise_for_status()

        data = response.json()

        return data.get("response", "").strip()

    except requests.exceptions.ConnectionError:
        return "Erreur : Ollama n'est pas accessible."

    except requests.exceptions.Timeout:
        return "Erreur : Qwen a mis trop de temps à répondre."

    except requests.exceptions.RequestException as e:
        return f"Erreur lors de la communication avec Ollama : {e}"


# =========================
# RÉSUMÉ
# =========================

def summarize_text(text: str) -> str:

    prompt = f"""
Tu es un assistant spécialisé dans le traitement de texte.

Résume le texte suivant de manière claire et concise.

Consignes :
- conserve uniquement les informations importantes ;
- ne change pas le sens ;
- utilise des phrases simples ;
- produis un résumé en français.

Texte :
{text}

Résumé :
"""

    return generate_text(prompt)


# =========================
# REFORMULATION
# =========================

def reformulate_text(text: str) -> str:

    prompt = f"""
Tu es un assistant spécialisé dans la reformulation de textes.

Reformule le texte suivant dans un français clair, naturel et professionnel.

Ne change pas le sens du texte.

Texte :
{text}

Texte reformulé :
"""

    return generate_text(prompt)


# =========================
# CORRECTION
# =========================

def correct_text(text: str) -> str:

    prompt = f"""
Tu es un assistant de correction linguistique.

Corrige les fautes d'orthographe, de grammaire,
de conjugaison et de syntaxe du texte suivant.

Conserve le sens original.

Texte :
{text}

Texte corrigé :
"""

    return generate_text(prompt)


# =========================
# EXTRACTION DES IDÉES
# =========================

def extract_ideas(text: str) -> str:

    prompt = f"""
Analyse le texte suivant et extrait les idées principales.

Présente les résultats sous forme de liste numérotée.

Texte :
{text}

Idées principales :
"""

    return generate_text(prompt)


# =========================
# EXPLICATION
# =========================

def explain_text(text: str) -> str:

    prompt = f"""
Explique le texte suivant de manière simple
et compréhensible pour un étudiant.

Identifie :
1. le sujet principal ;
2. les concepts importants ;
3. l'idée générale.

Texte :
{text}

Explication :
"""

    return generate_text(prompt)


# =========================
# MODE INTERACTIF
# =========================

def main():

    print("=" * 60)
    print(" ASSISTANT INTELLIGENT DE TRAITEMENT DE TEXTE")
    print(" Modèle :", MODEL_NAME)
    print("=" * 60)

    while True:

        print("\nChoisissez une opération :")

        print("1 - Résumer")
        print("2 - Reformuler")
        print("3 - Corriger")
        print("4 - Extraire les idées principales")
        print("5 - Expliquer")
        print("6 - Génération libre")
        print("0 - Quitter")

        choice = input("\nVotre choix : ").strip()

        if choice == "0":
            print("\nProgramme terminé.")
            break

        if choice not in ["1", "2", "3", "4", "5", "6"]:
            print("Choix invalide.")
            continue

        print("\nEntrez votre texte.")
        print("(Tapez FIN sur une nouvelle ligne pour terminer.)")

        lines = []

        while True:
            line = input()

            if line.strip().upper() == "FIN":
                break

            lines.append(line)

        text = "\n".join(lines).strip()

        if not text:
            print("Aucun texte fourni.")
            continue

        print("\nTraitement en cours...\n")

        if choice == "1":
            result = summarize_text(text)

        elif choice == "2":
            result = reformulate_text(text)

        elif choice == "3":
            result = correct_text(text)

        elif choice == "4":
            result = extract_ideas(text)

        elif choice == "5":
            result = explain_text(text)

        else:
            result = generate_text(text)

        print("=" * 60)
        print("RÉSULTAT")
        print("=" * 60)
        print(result)
        print("=" * 60)


# =========================
# LANCEMENT
# =========================

if __name__ == "__main__":
    main()