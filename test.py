import requests

from rag import search_corpus, build_context
from model import generate_response


# ============================================================
# TEST 1 : RECHERCHE DANS LE CORPUS
# ============================================================

def test_rag():

    print("\n")
    print("=" * 60)
    print("TEST 1 : RECHERCHE DANS LE CORPUS")
    print("=" * 60)

    query = input(
        "Entrez un mot à rechercher : "
    )

    results = search_corpus(query)

    if not results:

        print(
            "\n❌ Aucune correspondance trouvée."
        )

        return

    print(
        f"\n✅ {len(results)} résultat(s) trouvé(s)\n"
    )

    for result in results:

        print(
            f"Tshiluba : {result['ciluba']}"
        )

        print(
            f"Français : {result['francais']}"
        )

        if "nature" in result:
            print(
                f"Nature : {result['nature']}"
            )

        print("-" * 40)


# ============================================================
# TEST 2 : QWEN
# ============================================================

def test_qwen():

    print("\n")
    print("=" * 60)
    print("TEST 2 : QWEN")
    print("=" * 60)

    question = input(
        "Posez une question : "
    )

    # Recherche préalable
    results = search_corpus(question)

    if not results:

        print(
            "\n⚠️ Aucun résultat dans le corpus."
        )

        print(
            "Qwen ne sera pas utilisé pour inventer "
            "une traduction."
        )

        return

    # Construction du contexte
    context = build_context(results)

    print("\nContexte récupéré :")
    print(context)

    print("\n⏳ Interrogation de Qwen...")

    response = generate_response(
        question,
        context
    )

    print("\n🤖 Réponse de Qwen :")
    print(response)


# ============================================================
# TEST 3 : OLLAMA DIRECT
# ============================================================

def test_ollama():

    print("\n")
    print("=" * 60)
    print("TEST 3 : CONNEXION OLLAMA")
    print("=" * 60)

    url = (
        "http://host.docker.internal:11434/api/tags"
    )

    try:

        response = requests.get(
            url,
            timeout=10
        )

        print(
            f"Status HTTP : {response.status_code}"
        )

        if response.status_code == 200:

            print(
                "✅ Ollama est accessible."
            )

            print(
                response.json()
            )

        else:

            print(
                "❌ Ollama a retourné une erreur."
            )

    except Exception as e:

        print(
            f"❌ Impossible de contacter Ollama : {e}"
        )


# ============================================================
# TEST 4 : API FASTAPI
# ============================================================

def test_api():

    print("\n")
    print("=" * 60)
    print("TEST 4 : API FASTAPI")
    print("=" * 60)

    url = "http://127.0.0.1:8000/"

    try:

        response = requests.get(
            url,
            timeout=10
        )

        print(
            f"Status HTTP : {response.status_code}"
        )

        print(
            "Réponse :"
        )

        print(
            response.json()
        )

    except Exception as e:

        print(
            f"❌ API inaccessible : {e}"
        )


# ============================================================
# MENU PRINCIPAL
# ============================================================

if __name__ == "__main__":

    print("\n")
    print("=" * 60)
    print(" ASSISTANT TSHILUBA - FRANÇAIS")
    print("=" * 60)

    print("""
1 - Tester la recherche dans le corpus
2 - Tester Qwen avec le contexte du corpus
3 - Tester la connexion Ollama
4 - Tester l'API FastAPI
5 - Tout tester
0 - Quitter
""")

    choix = input(
        "Votre choix : "
    )

    if choix == "1":

        test_rag()

    elif choix == "2":

        test_qwen()

    elif choix == "3":

        test_ollama()

    elif choix == "4":

        test_api()

    elif choix == "5":

        test_rag()
        test_qwen()
        test_ollama()
        test_api()

    elif choix == "0":

        print("Programme terminé.")

    else:

        print("Choix invalide.")
