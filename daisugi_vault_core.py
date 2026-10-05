"""
daisugi_vault_core.py
Servidor Central de Autenticação, Cofre de Segredos (PAM) e Governança (IGA)
Daisugi Ecosystem Cofre-PAM-IGA
"""

import os
import time
from typing import Dict, Any, List, Optional
from fastapi import FastAPI, HTTPException, Depends, Security
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import jwt

app = FastAPI(
    title="Daisugi Ecosystem Cofre-PAM-IGA",
    description="Autoridade Central de Identidade, Cofre de Chaves e Governança Multi-Tenant",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SECRET_KEY = os.getenv("DAISUGI_VAULT_SECRET", "daisugi_master_vault_secret_key_2026")
ALGORITHM = "HS256"
security = HTTPBearer()

# Base em memória de Cadeiras Corporativas (Simulação do Catálogo IGA Multi-Tenant)
CATALOGO_CADEIRAS = {
    "montanhavermelha@akagui.com": {
        "nome": "Akagui Core Master",
        "cadeira": "core.developer@daisugi.com.br",
        "tenant_id": "daisugi_global",
        "role": "core_developer",
        "alcada": "Soberana",
        "tier": 0,
        "is_core_developer": True,
        "salas": ["all"]
    },
    "ronaldoakagui@gmail.com": {
        "nome": "Ronaldo Akagui (Engenharia Soberana)",
        "cadeira": "core.developer@daisugi.com.br",
        "tenant_id": "daisugi_global",
        "role": "core_developer",
        "alcada": "Soberana",
        "tier": 0,
        "is_core_developer": True,
        "salas": ["all"]
    },
    "controller@sugoisa.com.br": {
        "nome": "Controller Geral",
        "cadeira": "controller@sugoisa.com.br",
        "tenant_id": "sugoi_sa",
        "role": "checker",
        "alcada": "Controladoria",
        "tier": 2,
        "is_core_developer": False,
        "salas": ["quarentena", "governanca_erp", "controladoria"]
    },
    "advogado.imobiliario@sugoisa.com.br": {
        "nome": "Advogado Imobiliário",
        "cadeira": "advogado.imobiliario@sugoisa.com.br",
        "tenant_id": "sugoi_sa",
        "role": "checker",
        "alcada": "Jurídico",
        "tier": 2,
        "is_core_developer": False,
        "salas": ["quarentena", "juridico"]
    },
    "comprador@sugoisa.com.br": {
        "nome": "Comprador Suprimentos",
        "cadeira": "comprador@sugoisa.com.br",
        "tenant_id": "sugoi_sa",
        "role": "maker",
        "alcada": "Operacional",
        "tier": 3,
        "is_core_developer": False,
        "salas": ["suprimentos", "procedimentos"]
    },
    "engenheiro.obra@sugoisa.com.br": {
        "nome": "Engenheiro de Obra",
        "cadeira": "engenheiro.obra@sugoisa.com.br",
        "tenant_id": "sugoi_sa",
        "role": "maker",
        "alcada": "Operacional",
        "tier": 3,
        "is_core_developer": False,
        "salas": ["obras", "medicoes"]
    }
}

class HandshakeRequest(BaseModel):
    usuario: str
    senha: str
    tenant_id: str
    origem_sistema: str

class HandshakeResponse(BaseModel):
    autenticado: bool
    access_token: str
    token_type: str
    expires_in: int
    usuario: Dict[str, Any]

class SoDValidationRequest(BaseModel):
    acao: str
    documento_hash: str
    maker_identity: str
    valor_brl: float = 0.0

@app.get("/health")
def health():
    return {"status": "online", "sistema": "Daisugi_Ecosystem_Cofre-PAM-IGA", "timestamp": time.time()}

@app.post("/api/v1/auth/handshake", response_model=HandshakeResponse)
def handshake(req: HandshakeRequest):
    u = req.usuario.lower()
    if req.senha != "123":  # Simulação de cofre de senhas PAM
        raise HTTPException(status_code=401, detail="Credenciais recusadas pelo Cofre PAM.")

    if u not in CATALOGO_CADEIRAS:
        raise HTTPException(status_code=403, detail="Identidade não atribuída a nenhuma Cadeira no catálogo IGA.")

    perfil = CATALOGO_CADEIRAS[u]
    now = int(time.time())
    payload = {
        "iss": "https://auth.daisugi.com.br",
        "sub": u,
        "nome": perfil["nome"],
        "tenant_id": perfil["tenant_id"],
        "cadeira_principal": perfil["cadeira"],
        "role": perfil["role"],
        "alcada": perfil["alcada"],
        "tier": perfil["tier"],
        "is_core_developer": perfil["is_core_developer"],
        "salas_liberadas": perfil["salas"],
        "iat": now,
        "exp": now + 28800  # 8 horas
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return HandshakeResponse(
        autenticado=True,
        access_token=token,
        token_type="Bearer",
        expires_in=28800,
        usuario={
            "sub": u,
            "nome": perfil["nome"],
            "cadeira": perfil["cadeira"],
            "role": perfil["role"],
            "is_core_developer": perfil["is_core_developer"],
            "salas": perfil["salas"]
        }
    )

@app.post("/api/v1/governance/sod/validate-action")
def validate_sod_action(req: SoDValidationRequest, credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Token inválido: {e}")

    checker_sub = payload.get("sub", "").lower()
    maker_sub = req.maker_identity.lower()

    if checker_sub == maker_sub:
        raise HTTPException(
            status_code=403,
            detail="Violação SoD Impeditiva: O criador da solicitação (Maker) não pode aprovar a quarentena (Checker)."
        )

    if payload.get("role") not in ["checker", "admin", "core_developer"]:
        raise HTTPException(
            status_code=403,
            detail="Acesso Negado: A Cadeira atual não possui alçada para aprovar quarentena."
        )

    return {
        "aprovado": True,
        "mensagem": "Validação SoD aprovada pelo Cofre-PAM-IGA.",
        "auditoria_hash": f"sod_audit_{int(time.time())}"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("daisugi_vault_core.py:app", host="0.0.0.0", port=8100, reload=True)
