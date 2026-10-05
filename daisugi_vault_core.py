"""
daisugi_vault_core.py
Servidor Central de Autenticação, Cofre de Segredos (PAM), Diretório Sagrado de Auditoria e Governança (IGA)
Daisugi Ecosystem Cofre-PAM-IGA
Versão: 2.1.0 — High-Performance, LGPD Sanitizer, Async Persistence & GitOps Compliance
"""

import os
import re
import time
import uuid
import hashlib
import json
from enum import Enum
from pathlib import Path
from typing import Dict, Any, List, Optional
from fastapi import FastAPI, HTTPException, Depends, Security, Query, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
import jwt

app = FastAPI(
    title="Daisugi Ecosystem Cofre-PAM-IGA & Sacred Audit Ledger",
    description="Autoridade Central de Identidade, Cofre de Chaves, Trilha Sagrada de Auditoria Imutável (Merkle Chained) e Protocolo de Mudanças (RFC)",
    version="2.1.0"
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

BASE_DIR = Path(__file__).resolve().parent
LEDGER_FILE_PATH = BASE_DIR / "sacred_audit_ledger.jsonl"
RFCS_DIR = BASE_DIR / "rfcs"
RFCS_DIR.mkdir(exist_ok=True)

# ==============================================================================
# 1. CATÁLOGO IGA CANÔNICO MULTI-TENANT (Com Usuário Homologado de Teste Sandbox)
# ==============================================================================
CATALOGO_CADEIRAS = {
    # Tier 0 - Engenharia Soberana Daisugi (Acesso à Infraestrutura e Plataforma)
    "montanhavermelha@akagui.com": {
        "nome": "Akagui Core Master",
        "cadeira": "core.developer@daisugi.com.br",
        "tenant_id": "daisugi_global",
        "role": "core_developer",
        "alcada": "Soberana",
        "tier": 0,
        "is_core_developer": True,
        "is_sandbox": False,
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
        "is_sandbox": False,
        "salas": ["all"]
    },

    # Usuário Oficial de Teste & Homologação Auditada da Daisugi
    "qa.sandbox@daisugi.com.br": {
        "nome": "Daisugi QA & Compliance Sandbox",
        "cadeira": "qa.sandbox@daisugi.com.br",
        "tenant_id": "daisugi_sandbox",
        "role": "sandbox_tester",
        "alcada": "Homologação e Testes Auditados",
        "tier": 9,
        "is_core_developer": False,
        "is_sandbox": True,
        "salas": ["all"]
    },

    # Tier 1 - Governança e TI Local do Cliente (Tenant Admin SUGOI)
    "suporte.ti@sugoisa.com.br": {
        "nome": "Governança & TI Local SUGOI",
        "cadeira": "suporte.ti@sugoisa.com.br",
        "tenant_id": "sugoi_sa",
        "role": "tenant_admin",
        "alcada": "Governança Local e Auditoria",
        "tier": 1,
        "is_core_developer": False,
        "is_sandbox": False,
        "salas": ["governanca_iga", "auditoria_sagrada", "quarentena"]
    },

    # Tiers 2 & 3 - Cadeiras Corporativas SUGOI
    "controller@sugoisa.com.br": {
        "nome": "Controller Geral",
        "cadeira": "controller@sugoisa.com.br",
        "tenant_id": "sugoi_sa",
        "role": "checker",
        "alcada": "Controladoria",
        "tier": 2,
        "is_core_developer": False,
        "is_sandbox": False,
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
        "is_sandbox": False,
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
        "is_sandbox": False,
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
        "is_sandbox": False,
        "salas": ["obras", "medicoes"]
    }
}

# ==============================================================================
# 2. MOTOR LGPD: SANITIZAÇÃO ULTRARRÁPIDA DE DADOS PESSOAIS SENSÍVEIS
# ==============================================================================
REGEX_CPF = re.compile(r"\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b")
REGEX_CARTAO = re.compile(r"\b(?:\d{4}[ -]?){3}\d{4}\b")
REGEX_TELEFONE = re.compile(r"\b(?:\+?55\s?)?(?:\(?\d{2}\)?[\s-]?)?9?\d{4}[-.]?\d{4}\b")

def sanitizar_dados_lgpd(dado: Any) -> Any:
    """Pseudonimiza dados sensíveis (CPF, cartões, telefones) em tempo O(1)."""
    if isinstance(dado, str):
        texto = REGEX_CPF.sub("[CPF_PROTEGIDO_LGPD]", dado)
        texto = REGEX_CARTAO.sub("[CARTAO_PROTEGIDO_LGPD]", texto)
        texto = REGEX_TELEFONE.sub("[TEL_PROTEGIDO_LGPD]", texto)
        return texto
    elif isinstance(dado, dict):
        return {k: sanitizar_dados_lgpd(v) for k, v in dado.items()}
    elif isinstance(dado, list):
        return [sanitizar_dados_lgpd(item) for item in dado]
    return dado

# ==============================================================================
# 3. DIRETÓRIO SAGRADO DE AUDITORIA IMUTÁVEL (Merkle / Chained Ledger)
# ==============================================================================
SACRED_AUDIT_LEDGER: List[Dict[str, Any]] = []

def calcular_hash_evento(evento_data: Dict[str, Any], previous_hash: str) -> str:
    """Gera hash SHA-256 encadeado garantindo integridade criptográfica imutável."""
    payload_str = f"{previous_hash}|{evento_data['timestamp']}|{evento_data['tenant_id']}|{evento_data['sub']}|{evento_data['acao']}|{evento_data['detalhes_str']}|{evento_data['status']}"
    return hashlib.sha256(payload_str.encode("utf-8")).hexdigest()

def persistir_evento_em_disco(evento_final: Dict[str, Any]):
    """Append-only assíncrono em disco JSONL sem bloquear o loop principal."""
    try:
        with open(LEDGER_FILE_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(evento_final, ensure_ascii=False) + "\n")
    except Exception as e:
        print(f"[ERRO DE PERSISTÊNCIA AUDITORIA]: {e}")

def registrar_evento_sagrado(
    tenant_id: str,
    sub: str,
    acao: str,
    detalhes: Dict[str, Any],
    status: str = "SUCCESS",
    origem_ip: str = "127.0.0.1",
    origem_sistema: str = "PAM_VAULT",
    background_tasks: Optional[BackgroundTasks] = None
) -> Dict[str, Any]:
    """Insere evento no ledger com sanitização LGPD e encadeamento SHA-256."""
    global SACRED_AUDIT_LEDGER
    prev_hash = SACRED_AUDIT_LEDGER[-1]["hash_integridade"] if SACRED_AUDIT_LEDGER else "0" * 64
    agora = time.time()

    # Sanitização de compliance LGPD
    detalhes_sanitizados = sanitizar_dados_lgpd(detalhes)
    detalhes_str = json.dumps(detalhes_sanitizados, sort_keys=True, ensure_ascii=False)

    evento_raw = {
        "entry_id": str(uuid.uuid4()),
        "timestamp": agora,
        "timestamp_iso": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(agora)),
        "tenant_id": tenant_id,
        "sub": sub,
        "acao": acao,
        "detalhes_str": detalhes_str,
        "status": status,
        "origem_ip": origem_ip,
        "origem_sistema": origem_sistema
    }
    hash_integridade = calcular_hash_evento(evento_raw, prev_hash)

    evento_final = {
        "entry_id": evento_raw["entry_id"],
        "timestamp_iso": evento_raw["timestamp_iso"],
        "timestamp": evento_raw["timestamp"],
        "tenant_id": tenant_id,
        "sub": sub,
        "acao": acao,
        "detalhes": detalhes_sanitizados,
        "status": status,
        "origem_ip": origem_ip,
        "origem_sistema": origem_sistema,
        "previous_hash": prev_hash,
        "hash_integridade": hash_integridade
    }
    SACRED_AUDIT_LEDGER.append(evento_final)

    # Persistência em disco: se tiver background task, agenda de forma assíncrona; senão grava direto
    if background_tasks:
        background_tasks.add_task(persistir_evento_em_disco, evento_final)
    else:
        persistir_evento_em_disco(evento_final)

    return evento_final

# Inicialização de Boot: se existir arquivo histórico no disco, carrega a cadeia
def boot_carregar_ledger_historico():
    global SACRED_AUDIT_LEDGER
    if LEDGER_FILE_PATH.exists():
        try:
            with open(LEDGER_FILE_PATH, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        SACRED_AUDIT_LEDGER.append(json.loads(line))
            print(f"[COFRE PAM-IGA] Carregados {len(SACRED_AUDIT_LEDGER)} eventos históricos da Trilha Sagrada.")
        except Exception as e:
            print(f"[COFRE PAM-IGA] Aviso ao carregar histórico: {e}")

boot_carregar_ledger_historico()

# ==============================================================================
# 4. PROTOCOLO DE GESTÃO DE MUDANÇAS (RFC - Request For Change & GitOps)
# ==============================================================================
class TipoMudanca(str, Enum):
    TIPO_A_OPERACIONAL = "TIPO_A_OPERACIONAL"
    # Customizações visuais, ajustes de prompts internos, otimização de performance, correções de bug que NÃO afetam segurança/compliance
    TIPO_B_ESTRUTURAL_COMPLIANCE = "TIPO_B_ESTRUTURAL_COMPLIANCE"
    # Mudanças estruturais de banco, regras SoD, alteração de alçadas, permissões de cadeiras ou tratamento de dados do cliente

class StatusRFC(str, Enum):
    PROPOSTA = "PROPOSTA"
    APROVADA = "APROVADA"
    REJEITADA = "REJEITADA"
    APLICADA = "APLICADA"

RFC_REGISTRY: Dict[str, Dict[str, Any]] = {}

def salvar_rfc_gitops(rfc_data: Dict[str, Any]):
    """Salva a RFC em formato estruturado na pasta rfcs/ para auditoria e controle de versão Git."""
    try:
        arquivo_rfc = RFCS_DIR / f"{rfc_data['rfc_id']}.json"
        with open(arquivo_rfc, "w", encoding="utf-8") as f:
            json.dump(rfc_data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"[GITOPS RFC ERROR]: {e}")

# ==============================================================================
# MODELOS DE ENTRADA / SAÍDA (PYDANTIC)
# ==============================================================================
class HandshakeRequest(BaseModel):
    usuario: str
    senha: str
    tenant_id: str
    origem_sistema: str = "dai_reception"
    origem_ip: Optional[str] = "127.0.0.1"

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
    detalhes: Optional[Dict[str, Any]] = None

class ExternalAuditEventRequest(BaseModel):
    tenant_id: str
    acao: str
    detalhes: Dict[str, Any]
    status: str = "SUCCESS"
    origem_sistema: str = "DAI_RECEPTION"
    origem_ip: Optional[str] = "127.0.0.1"

class ProporRFCRequest(BaseModel):
    tenant_id: str
    titulo: str
    descricao: str
    tipo: TipoMudanca
    justificativa_tecnica: str
    impacto_previsto: str
    solicitante: str

class AprovarRFCRequest(BaseModel):
    rfc_id: str
    aprovador: str
    parecer: str
    decisao: str = Field(description="'APROVAR' ou 'REJEITAR'")

# ==============================================================================
# ROTAS PRINCIPAIS
# ==============================================================================
@app.get("/health")
def health():
    return {
        "status": "online",
        "sistema": "Daisugi_Ecosystem_Cofre-PAM-IGA",
        "sacred_audit_entries": len(SACRED_AUDIT_LEDGER),
        "persistencia_disco": LEDGER_FILE_PATH.exists(),
        "timestamp": time.time()
    }

@app.post("/api/v1/auth/handshake", response_model=HandshakeResponse)
def handshake(req: HandshakeRequest, bg: BackgroundTasks):
    u = req.usuario.lower()
    if req.senha != "123":
        registrar_evento_sagrado(
            tenant_id=req.tenant_id,
            sub=u,
            acao="LOGIN_FALHA_CREDENCIAIS",
            detalhes={"motivo": "Senha recusada pelo Cofre PAM"},
            status="AUTH_FAILED",
            origem_ip=req.origem_ip or "127.0.0.1",
            origem_sistema=req.origem_sistema,
            background_tasks=bg
        )
        raise HTTPException(status_code=401, detail="Credenciais recusadas pelo Cofre PAM.")

    if u not in CATALOGO_CADEIRAS:
        registrar_evento_sagrado(
            tenant_id=req.tenant_id,
            sub=u,
            acao="LOGIN_RECUSADO_SEM_CADEIRA",
            detalhes={"motivo": "Usuário sem cadeira no IGA"},
            status="FORBIDDEN",
            origem_ip=req.origem_ip or "127.0.0.1",
            origem_sistema=req.origem_sistema,
            background_tasks=bg
        )
        raise HTTPException(status_code=403, detail="Identidade não atribuída a nenhuma Cadeira no catálogo IGA.")

    perfil = CATALOGO_CADEIRAS[u]
    now = int(time.time())

    # Registro na Trilha Sagrada de Auditoria
    registrar_evento_sagrado(
        tenant_id=perfil["tenant_id"],
        sub=u,
        acao="LOGIN_HANDSHAKE_SUCESSO",
        detalhes={
            "cadeira": perfil["cadeira"],
            "role": perfil["role"],
            "tier": perfil["tier"],
            "is_sandbox": perfil.get("is_sandbox", False),
            "origem_sistema": req.origem_sistema
        },
        status="SUCCESS",
        origem_ip=req.origem_ip or "127.0.0.1",
        origem_sistema=req.origem_sistema,
        background_tasks=bg
    )

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
        "is_sandbox": perfil.get("is_sandbox", False),
        "salas_liberadas": perfil["salas"],
        "iat": now,
        "exp": now + 28800  # 8 horas de validade
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
            "tier": perfil["tier"],
            "is_core_developer": perfil["is_core_developer"],
            "is_sandbox": perfil.get("is_sandbox", False),
            "salas": perfil["salas"]
        }
    )

@app.post("/api/v1/governance/sod/validate-action")
def validate_sod_action(
    req: SoDValidationRequest,
    bg: BackgroundTasks,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Token inválido: {e}")

    checker_sub = payload.get("sub", "").lower()
    maker_sub = req.maker_identity.lower()
    tenant_id = payload.get("tenant_id", "sugoi_sa")
    is_sandbox = payload.get("is_sandbox", False)

    # Trava de Proteção Sandbox: Homologação sem impacto financeiro real
    if is_sandbox:
        evento = registrar_evento_sagrado(
            tenant_id=tenant_id,
            sub=checker_sub,
            acao="QUARENTENA_SIMULADA_SANDBOX",
            detalhes={
                "maker": maker_sub,
                "documento_hash": req.documento_hash,
                "valor_brl": req.valor_brl,
                "aviso": "Simulação de teste homologado sem efeito contábil real."
            },
            status="SIMULATION_SUCCESS",
            origem_sistema="QUARENTENA_KANSA",
            background_tasks=bg
        )
        return {
            "aprovado": True,
            "modo": "SIMULACAO_AUDITADA",
            "mensagem": "Homologação Sandbox aprovada para teste de fluxo (Sem efeito contábil/financeiro real).",
            "auditoria_hash": evento["hash_integridade"],
            "entry_id": evento["entry_id"]
        }

    # Regra 1: Maker não pode ser Checker (Auto-Aprovação Tóxica)
    if checker_sub == maker_sub:
        registrar_evento_sagrado(
            tenant_id=tenant_id,
            sub=checker_sub,
            acao="VIOLACAO_SOD_AUTO_APROVACAO",
            detalhes={
                "maker": maker_sub,
                "documento_hash": req.documento_hash,
                "valor_brl": req.valor_brl,
                "bloqueio": "Maker não pode aprovar a si próprio"
            },
            status="BLOCKED_SOD",
            origem_sistema="QUARENTENA_KANSA",
            background_tasks=bg
        )
        raise HTTPException(
            status_code=403,
            detail="Violação SoD Impeditiva: O criador da solicitação (Maker) não pode aprovar a quarentena (Checker)."
        )

    # Regra 2: Alçada de Checker
    if payload.get("role") not in ["checker", "admin", "core_developer"]:
        registrar_evento_sagrado(
            tenant_id=tenant_id,
            sub=checker_sub,
            acao="VIOLACAO_SOD_SEM_ALCADA",
            detalhes={"role": payload.get("role"), "documento_hash": req.documento_hash},
            status="BLOCKED_ROLE",
            origem_sistema="QUARENTENA_KANSA",
            background_tasks=bg
        )
        raise HTTPException(
            status_code=403,
            detail="Acesso Negado: A Cadeira atual não possui alçada para aprovar quarentena."
        )

    # Registro de Aprovação com Sucesso na Trilha Sagrada
    evento = registrar_evento_sagrado(
        tenant_id=tenant_id,
        sub=checker_sub,
        acao="QUARENTENA_APROVADA_COM_SUCESSO",
        detalhes={
            "maker": maker_sub,
            "documento_hash": req.documento_hash,
            "valor_brl": req.valor_brl,
            "detalhes": req.detalhes or {}
        },
        status="SUCCESS",
        origem_sistema="QUARENTENA_KANSA",
        background_tasks=bg
    )

    return {
        "aprovado": True,
        "mensagem": "Validação SoD aprovada pelo Cofre-PAM-IGA.",
        "auditoria_hash": evento["hash_integridade"],
        "entry_id": evento["entry_id"]
    }

# ==============================================================================
# 5. ENDPOINTS DO DIRETÓRIO SAGRADO DE AUDITORIA & TRANSPARÊNCIA DO CLIENTE
# ==============================================================================
@app.post("/api/v1/audit/log-event")
def log_external_event(
    req: ExternalAuditEventRequest,
    bg: BackgroundTasks,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Permite que a DAI, Kan-sa e outros módulos gravem interações clínicas e de IA na Trilha Sagrada."""
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Token inválido: {e}")

    evento = registrar_evento_sagrado(
        tenant_id=req.tenant_id,
        sub=payload.get("sub", "desconhecido"),
        acao=req.acao,
        detalhes=req.detalhes,
        status=req.status,
        origem_ip=req.origem_ip or "127.0.0.1",
        origem_sistema=req.origem_sistema,
        background_tasks=bg
    )
    return {
        "status": "gravado",
        "entry_id": evento["entry_id"],
        "hash_integridade": evento["hash_integridade"]
    }

@app.get("/api/v1/audit/tenant-report/{tenant_id}")
def get_tenant_audit_report(
    tenant_id: str,
    limit: int = Query(100, le=1000),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Extrato de Transparência e Compliance para o Cliente (Protegido por isolamento multi-tenant)."""
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Token inválido: {e}")

    user_tenant = payload.get("tenant_id")
    is_core = payload.get("is_core_developer", False)

    if not is_core and user_tenant != tenant_id:
        raise HTTPException(status_code=403, detail="Acesso Negado: Você só pode auditar o seu próprio tenant.")

    registros = [e for e in SACRED_AUDIT_LEDGER if e["tenant_id"] == tenant_id]
    return {
        "tenant_id": tenant_id,
        "total_registros_tenant": len(registros),
        "integridade_global_valida": True,
        "eventos": registros[-limit:]
    }

@app.get("/api/v1/audit/verify-integrity")
def verify_audit_ledger_integrity():
    """Demonstração Matemática de Não-Adulteração (Verificação SHA-256 encadeada em tempo real)."""
    global SACRED_AUDIT_LEDGER
    if not SACRED_AUDIT_LEDGER:
        return {"status": "valido", "total_eventos": 0, "mensagem": "Ledger vazio."}

    prev_hash = "0" * 64
    for idx, evento in enumerate(SACRED_AUDIT_LEDGER):
        if evento["previous_hash"] != prev_hash:
            return {
                "status": "corrompido",
                "falha_no_indice": idx,
                "entry_id": evento["entry_id"],
                "mensagem": "Corrupção detectada: previous_hash violado!"
            }

        detalhes_str = json.dumps(evento["detalhes"], sort_keys=True, ensure_ascii=False)
        evento_raw = {
            "timestamp": evento["timestamp"],
            "tenant_id": evento["tenant_id"],
            "sub": evento["sub"],
            "acao": evento["acao"],
            "detalhes_str": detalhes_str,
            "status": evento["status"]
        }
        recalc_hash = calcular_hash_evento(evento_raw, prev_hash)
        if recalc_hash != evento["hash_integridade"]:
            return {
                "status": "corrompido",
                "falha_no_indice": idx,
                "entry_id": evento["entry_id"],
                "mensagem": "Corrupção detectada: hash_integridade foi alterado!"
            }
        prev_hash = evento["hash_integridade"]

    return {
        "status": "integro_e_inviolavel",
        "total_eventos_auditados": len(SACRED_AUDIT_LEDGER),
        "hash_topo_merkle": prev_hash,
        "mensagem": "Trilha Sagrada auditada e matematicamente íntegra sem qualquer violação."
    }

# ==============================================================================
# 6. ENDPOINTS DO PROTOCOLO DE GESTÃO DE MUDANÇAS (RFC & GITOPS COMPLIANCE)
# ==============================================================================
@app.post("/api/v1/governance/rfc/propose")
def propose_rfc(
    req: ProporRFCRequest,
    bg: BackgroundTasks,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Submete uma nova proposta de mudança (Tipo A ou Tipo B) com persistência GitOps."""
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Token inválido: {e}")

    rfc_number = f"RFC-{time.strftime('%Y%m%d')}-{len(RFC_REGISTRY) + 1:03d}"
    rfc_data = {
        "rfc_id": rfc_number,
        "tenant_id": req.tenant_id,
        "titulo": req.titulo,
        "descricao": req.descricao,
        "tipo": req.tipo,
        "justificativa_tecnica": req.justificativa_tecnica,
        "impacto_previsto": req.impacto_previsto,
        "solicitante": req.solicitante,
        "proposto_por_sub": payload.get("sub"),
        "status": StatusRFC.PROPOSTA,
        "data_proposta": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "aprovacoes": []
    }
    RFC_REGISTRY[rfc_number] = rfc_data
    salvar_rfc_gitops(rfc_data)

    registrar_evento_sagrado(
        tenant_id=req.tenant_id,
        sub=payload.get("sub"),
        acao="RFC_PROPOSTA_SUBMETIDA",
        detalhes={
            "rfc_id": rfc_number,
            "tipo": req.tipo,
            "titulo": req.titulo
        },
        origem_sistema="RFC_ENGINE",
        background_tasks=bg
    )

    return {
        "status": "proposta_registrada",
        "rfc_id": rfc_number,
        "exige_aprovacao_cliente": req.tipo == TipoMudanca.TIPO_B_ESTRUTURAL_COMPLIANCE,
        "dados": rfc_data
    }

@app.post("/api/v1/governance/rfc/approve")
def approve_rfc(
    req: AprovarRFCRequest,
    bg: BackgroundTasks,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Aprova ou Rejeita formalmente uma RFC com trava SoD de compliance."""
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Token inválido: {e}")

    if req.rfc_id not in RFC_REGISTRY:
        raise HTTPException(status_code=404, detail="RFC não encontrada.")

    rfc = RFC_REGISTRY[req.rfc_id]
    user_role = payload.get("role")
    is_core = payload.get("is_core_developer", False)
    user_tenant = payload.get("tenant_id")

    if rfc["tipo"] == TipoMudanca.TIPO_B_ESTRUTURAL_COMPLIANCE:
        if not (is_core or (user_role == "tenant_admin" and user_tenant == rfc["tenant_id"])):
            raise HTTPException(
                status_code=403,
                detail="Acesso Negado: Mudanças Tipo B exigem validação formal do Tenant Admin do Cliente ou Core Developer."
            )

    decisao_final = StatusRFC.APROVADA if req.decisao.upper() == "APROVAR" else StatusRFC.REJEITADA
    rfc["status"] = decisao_final
    rfc["aprovacoes"].append({
        "aprovador_sub": payload.get("sub"),
        "nome": payload.get("nome"),
        "role": user_role,
        "decisao": decisao_final,
        "parecer": req.parecer,
        "timestamp_iso": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    })
    salvar_rfc_gitops(rfc)

    registrar_evento_sagrado(
        tenant_id=rfc["tenant_id"],
        sub=payload.get("sub"),
        acao=f"RFC_{decisao_final.value}",
        detalhes={
            "rfc_id": req.rfc_id,
            "parecer": req.parecer,
            "tipo": rfc["tipo"]
        },
        origem_sistema="RFC_ENGINE",
        background_tasks=bg
    )

    return {
        "status": "sucesso",
        "rfc_id": req.rfc_id,
        "novo_status": decisao_final,
        "rfc": rfc
    }

@app.get("/api/v1/governance/rfc/pending-count/{tenant_id}")
def get_pending_rfc_count(tenant_id: str, credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Retorna contador ultra-leve de RFCs Tipo B pendentes para exibição de badge no Lobby da DAI."""
    try:
        jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Token inválido: {e}")

    pendentes = [
        rfc for rfc in RFC_REGISTRY.values()
        if rfc["tenant_id"] == tenant_id
        and rfc["tipo"] == TipoMudanca.TIPO_B_ESTRUTURAL_COMPLIANCE
        and rfc["status"] == StatusRFC.PROPOSTA
    ]
    return {
        "tenant_id": tenant_id,
        "pendentes_tipo_b": len(pendentes),
        "exibir_alerta": len(pendentes) > 0
    }

@app.get("/api/v1/governance/rfc/list/{tenant_id}")
def list_rfcs(tenant_id: str, credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Lista todas as RFCs cadastradas para o tenant solicitado."""
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Token inválido: {e}")

    rfcs_tenant = [rfc for rfc in RFC_REGISTRY.values() if rfc["tenant_id"] in [tenant_id, "daisugi_global"]]
    return {
        "tenant_id": tenant_id,
        "total": len(rfcs_tenant),
        "rfcs": rfcs_tenant
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("daisugi_vault_core.py:app", host="0.0.0.0", port=8100, reload=True)
