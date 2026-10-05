# 📜 Contrato de API e Integração: Daisugi Ecosystem Cofre-PAM-IGA
**Versão:** 1.0.0  
**Padrão:** RESTful / JSON / OAuth2 Bearer JWT  
**Host do Cofre:** `https://auth.daisugi.com.br` (ou IP OCI sob TLS)

---

## 1. Princípios do Contrato e Homeostase O(1)

Para que a **DAI (Smart Reception)** e os demais sistemas não sofram lentidão:
1. **Validação Desacoplada O(1):** A DAI não bate no Cofre a cada mensagem trocada com a IA. A DAI apenas valida a **assinatura criptográfica da chave pública** do token JWT localmente em memória (tempo de execução: < 1ms).
2. **Handshake Pré-Lobby:** A ida ao Cofre ocorre apenas no momento do login na Portaria e na aprovação de Quarentenas Críticas.
3. **Imutabilidade de Cadeiras:** Permissões pertencem à Cadeira Funcional (`cadeira_principal`), e não ao indivíduo arbitrário.

---

## 2. Estrutura Canônica do Token JWT da Daisugi

O token emitido pelo Cofre-PAM-IGA contém todas as claims necessárias para o ecossistema operar:

```json
{
  "iss": "https://auth.daisugi.com.br",
  "sub": "ronaldo.akagui@sugoisa.com.br",
  "nome": "Ronaldo Akagui",
  "tenant_id": "sugoi_sa",
  "tenant_nome": "SUGOI Construtora S.A.",
  "cadeira_principal": "diretor.presidente@sugoisa.com.br",
  "cadeira_nominal": "ronaldo.akagui@sugoisa.com.br",
  "alcada": "Diretoria Executiva",
  "perfil": "Presidência",
  "tier": 2,
  "role": "checker",
  "salas_liberadas": [
    "quarentena_risco",
    "governanca_erp",
    "controladoria",
    "juridico",
    "obras"
  ],
  "sod_rules": {
    "is_maker": false,
    "can_approve_quarantine": true,
    "max_approval_limit_brl": 1000000.00
  },
  "is_core_developer": false,
  "iat": 1791168497,
  "exp": 1791197297
}
```

> **Atenção:** A claim `"is_core_developer": true` e `"tier": 0` **SÓ PODE** ser emitida se o `"sub"` for estritamente `montanhavermelha@akagui.com` ou `ronaldoakagui@gmail.com`. Qualquer tentativa de injeção externa retorna erro imediato de integridade.

---

## 3. Especificação dos Endpoints REST

### 3.1. `POST /api/v1/auth/handshake` (Login Pré-Lobby)
Responsável por autenticar a identidade, cruzar com o Catálogo de Cadeiras do IGA e emitir o Token de Sessão.

* **Headers:** `Content-Type: application/json`
* **Request Body:**
  ```json
  {
    "usuario": "controller@sugoisa.com.br",
    "senha": "hash_ou_segredo_mfa",
    "tenant_id": "sugoi_sa",
    "origem_sistema": "dai_reception"
  }
  ```
* **Response (HTTP 200 OK):**
  ```json
  {
    "autenticado": true,
    "access_token": "eyJhbGciOiJSUzI1NiIs...",
    "token_type": "Bearer",
    "expires_in": 28800,
    "usuario": {
      "nome": "Controller Geral",
      "cadeira_principal": "controller@sugoisa.com.br",
      "role": "checker",
      "salas": [
        {"id": "quarentena", "nome": "Painel de Quarentena", "cor": "#EF4444"},
        {"id": "erp_travas", "nome": "Governança de Travas", "cor": "#3B82F6"}
      ]
    }
  }
  ```
* **Erros Comuns:**
  * `HTTP 401 Unauthorized`: Credenciais inválidas ou conta inativa no IGA.
  * `HTTP 403 Forbidden`: Conflito SoD impeditivo (ex: usuário em cadeira conflitante sem alçada).

---

### 3.2. `GET /api/v1/auth/public-key` (Chave Pública para Validação Local)
Permite que a DAI, o Kan-sa e o Hudson baixem a chave pública da Daisugi na inicialização do container para validar tokens sem consultar o Cofre a todo instante.

* **Response (HTTP 200 OK):**
  ```json
  {
    "algorithm": "RS256",
    "public_key_pem": "-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8A...\n-----END PUBLIC KEY-----",
    "kid": "daisugi_vault_key_2026_v1"
  }
  ```

---

### 3.3. `POST /api/v1/governance/sod/validate-action` (Validação Maker/Checker)
Invocado pela DAI ou pelo Kan-sa quando um usuário tenta aprovar uma Quarentena Crítica (ex: liberação de medição, contrato imobiliário ou hash CCB).

* **Headers:** `Authorization: Bearer <token_jwt>`
* **Request Body:**
  ```json
  {
    "acao": "APROVACAO_QUARENTENA_CCB",
    "documento_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "maker_identity": "comprador@sugoisa.com.br",
    "valor_brl": 45000.00
  }
  ```
* **Regra de Decisão do Cofre:**
  * Se `token.sub == request.maker_identity` ➔ **BLOQUEIO IMEDIATO (HTTP 403)** com mensagem: *"Violação SoD: O criador do documento (Maker) não pode aprovar a quarentena (Checker)."*
  * Se `token.alcada_limite < request.valor_brl` ➔ **BLOQUEIO POR ALÇADA (HTTP 403)**.
  * Se aprovado ➔ **HTTP 200 OK** com Hash de Assinatura de Auditoria gravado no log imutável.

---

### 3.4. `POST /api/v1/governance/break-glass` (Acesso de Emergência)
Endpoint de ativação de privilégio máximo para contenção de desastres.

* **Requisito Inegociável:** Requer autenticação de dois fatores e identidade estrita de Core Developer (`montanhavermelha@akagui.com` ou `ronaldoakagui@gmail.com`).
* **Ação:** Emite credenciais temporárias de resgate com expiração curta (30 minutos) e dispara alerta criptografado para o comitê de segurança.

---

### 3.5. `POST /api/v1/audit/log-event` (Registro na Trilha Sagrada)
Permite que a DAI, o Kan-sa e outros módulos gravem interações clínicas, perguntas de usuários, respostas geradas pela IA e deliberações com encadeamento SHA-256.

* **Headers:** `Authorization: Bearer <token_jwt>`
* **Request Body:**
  ```json
  {
    "tenant_id": "sugoi_sa",
    "acao": "CONSULTA_CLINICA_DAI",
    "detalhes": {
      "sala": "Dr. Taylor Code",
      "pergunta_resumo": "Verificação de conformidade de contrato de terceirizado",
      "resposta_gerada": "Parecer clínico emitido com similaridade RAG 0.88",
      "tempo_resposta_ms": 420
    },
    "status": "SUCCESS",
    "origem_sistema": "DAI_RECEPTION"
  }
  ```
* **Response (HTTP 200 OK):**
  ```json
  {
    "status": "gravado",
    "entry_id": "f5127025-a13a-44c1-...",
    "hash_integridade": "7c5e2671b..."
  }
  ```

---

### 3.6. `GET /api/v1/audit/tenant-report/{tenant_id}` (Extrato de Transparência do Cliente)
Relatório para o cliente extrair todas as ações ocorridas dentro do seu tenant com integridade comprovada.

* **Headers:** `Authorization: Bearer <token_jwt>`
* **Segurança:** Apenas usuários do próprio `tenant_id` ou Core Developers têm acesso aos seus dados.

---

### 3.7. `GET /api/v1/audit/verify-integrity` (Prova Matemática de Não-Adulteração)
Auditoria algorítmica independente que recalcula todos os hashes da cadeia para garantir que nenhum evento foi adulterado ou deletado.

---

### 3.8. `POST /api/v1/governance/rfc/propose` e `POST /api/v1/governance/rfc/approve` (Protocolo de Gestão de Mudanças)
* **Mudanças Tipo A (Operacionais / UI / Prompts internos):** Registradas e aprovadas com agilidade técnica.
* **Mudanças Tipo B (Estruturais / Compliance do Cliente):** Exigem protocolo formal (`RFC-AAAAMMDD-NNN`) e validação obrigatória do Tenant Admin do cliente (`suporte.ti@sugoisa.com.br`).

