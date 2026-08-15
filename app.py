import time

from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
from pydantic import BaseModel

from rag import search_corpus, build_context
from model import generate_response


# ============================================================
# CONFIGURATION
# ============================================================

APP_NAME = "Assistant intelligent lexical Tshiluba-Français"

SECRET_KEY = "secret-dev-key"
ALGORITHM = "HS256"

USERNAME = "admin"
PASSWORD = "admin"


# ============================================================
# INITIALISATION FASTAPI
# ============================================================

app = FastAPI(
    title=APP_NAME,
    description=(
        "Assistant intelligent lexical bilingue "
        "Tshiluba-Français"
    ),
    version="1.0.0"
)


# ============================================================
# AUTHENTIFICATION JWT
# ============================================================

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/login"
)


def create_token(username: str):

    payload = {
        "sub": username
    }

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token


def verify_token(
    token: str = Depends(oauth2_scheme)
):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        username = payload.get("sub")

        if not username:

            raise HTTPException(
                status_code=401,
                detail="Token invalide"
            )

        return username

    except Exception:

        raise HTTPException(
            status_code=401,
            detail="Token invalide ou expiré"
        )


# ============================================================
# MODÈLES DE REQUÊTES
# ============================================================

class SearchRequest(BaseModel):

    query: str


class GenerateRequest(BaseModel):

    question: str


# ============================================================
# ROUTE PRINCIPALE
# ============================================================

@app.get("/")
def root():

    return {
        "application": APP_NAME,
        "status": "online",
        "message": (
            "API de l'assistant lexical "
            "Tshiluba-Français opérationnelle."
        )
    }


# ============================================================
# LOGIN
# ============================================================

@app.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends()
):

    if (
        form_data.username != USERNAME
        or form_data.password != PASSWORD
    ):

        raise HTTPException(
            status_code=401,
            detail="Nom d'utilisateur ou mot de passe incorrect"
        )

    token = create_token(
        form_data.username
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }


# ============================================================
# RECHERCHE LEXICALE
# ============================================================

@app.post("/search")
def search(
    request: SearchRequest,
    username: str = Depends(verify_token)
):

    start_time = time.time()

    query = request.query.strip()

    if not query:

        raise HTTPException(
            status_code=400,
            detail="La requête ne peut pas être vide."
        )

    # Recherche dans le corpus
    results = search_corpus(query)

    processing_time = (
        time.time() - start_time
    )

    # Aucun résultat
    if not results:

        return {
            "success": True,
            "found": False,
            "query": query,
            "results": [],
            "message": (
                "Aucune correspondance trouvée "
                "dans le corpus."
            ),
            "processing_time": round(
                processing_time,
                4
            )
        }

    # Résultats trouvés
    return {
        "success": True,
        "found": True,
        "query": query,
        "results": results,
        "count": len(results),
        "processing_time": round(
            processing_time,
            4
        )
    }


# ============================================================
# GÉNÉRATION AVEC QWEN
# ============================================================

@app.post("/generate")
def generate(
    request: GenerateRequest,
    username: str = Depends(verify_token)
):

    question = request.question.strip()

    if not question:

        raise HTTPException(
            status_code=400,
            detail="La question ne peut pas être vide."
        )

    start_time = time.time()

    # --------------------------------------------------------
    # ÉTAPE 1 : RECHERCHE DANS LE CORPUS
    # --------------------------------------------------------

    results = search_corpus(question)

    # --------------------------------------------------------
    # ÉTAPE 2 : SI AUCUNE INFORMATION N'EST TROUVÉE
    # --------------------------------------------------------

    if not results:

        return {
            "success": True,
            "found": False,
            "question": question,
            "source": "corpus",
            "response": (
                "Je n'ai trouvé aucune correspondance "
                "dans le corpus. Je ne vais pas inventer "
                "une traduction ou une information."
            ),
            "processing_time": round(
                time.time() - start_time,
                4
            )
        }

    # --------------------------------------------------------
    # ÉTAPE 3 : CONSTRUCTION DU CONTEXTE
    # --------------------------------------------------------

    context = build_context(results)

    # --------------------------------------------------------
    # ÉTAPE 4 : ENVOI DU CONTEXTE À QWEN
    # --------------------------------------------------------

    response = generate_response(
        question=question,
        context=context
    )

    # --------------------------------------------------------
    # ÉTAPE 5 : RÉPONSE FINALE
    # --------------------------------------------------------

    return {
        "success": True,
        "found": True,
        "question": question,
        "source": "corpus + Qwen",
        "corpus_results": results,
        "response": response,
        "processing_time": round(
            time.time() - start_time,
            4
        )
    }


# ============================================================
# INFORMATIONS SUR L'API
# ============================================================

@app.get("/health")
def health():

    return {
        "status": "healthy",
        "application": APP_NAME,
        "services": {
            "api": "online",
            "corpus": "available",
            "qwen": "configured"
        }
    }
