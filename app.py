from datetime import datetime, timedelta, timezone

from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from pydantic import BaseModel

from model import generate_text


app = FastAPI(
    title="LLM API",
    description="API de génération de texte avec Ollama et authentification JWT",
    version="1.0.0"
)


# =========================
# JWT
# =========================

SECRET_KEY = "cle-secrete-tp-a-remplacer"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# =========================
# UTILISATEUR DE TEST
# =========================

USER = {
    "username": "henock",
    "password": "123456"
}


# =========================
# REQUÊTE GENERATE
# =========================

class GenerateRequest(BaseModel):
    prompt: str


# =========================
# CREATION JWT
# =========================

def create_access_token(username: str):

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": username,
        "exp": expire
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


# =========================
# ROUTE PRINCIPALE
# =========================

@app.get("/")
def root():
    return {
        "message": "LLM API opérationnelle"
    }


# =========================
# HEALTH CHECK
# =========================

@app.get("/health")
def health():
    return {
        "status": "ok"
    }


# =========================
# LOGIN
# =========================

@app.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends()
):

    if (
        form_data.username != USER["username"]
        or form_data.password != USER["password"]
    ):
        raise HTTPException(
            status_code=401,
            detail="Identifiants incorrects"
        )

    token = create_access_token(form_data.username)

    return {
        "access_token": token,
        "token_type": "bearer"
    }


# =========================
# VERIFICATION JWT
# =========================

def verify_token(token: str):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        username = payload.get("sub")

        if username is None:
            raise HTTPException(
                status_code=401,
                detail="Token invalide"
            )

        return username

    except JWTError:

        raise HTTPException(
            status_code=401,
            detail="Token invalide ou expiré"
        )


# =========================
# ROUTE PROTEGEE
# =========================

@app.get("/protected")
def protected(
    token: str = Depends(oauth2_scheme)
):

    username = verify_token(token)

    return {
        "message": f"Bienvenue {username}",
        "authenticated": True
    }


# =========================
# GENERATION AVEC OLLAMA
# =========================

@app.post("/generate")
def generate(
    request: GenerateRequest,
    token: str = Depends(oauth2_scheme)
):

    username = verify_token(token)

    response = generate_text(request.prompt)

    return {
        "user": username,
        "prompt": request.prompt,
        "response": response
    }
    
