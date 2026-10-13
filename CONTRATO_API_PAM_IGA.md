# 📜 Contrato Canônico de API e Federação de Identidades: Daisugi Ecosystem Cofre-PAM-IGA
**Versão:** 2.0.0 (Multi-Cadeiras, Federação IGA SUGOI & SSO Unificado)  
**Status:** HOMOLOGADO E PROTOCOLADO  
**Padrão:** RESTful / JSON / OAuth2 Bearer JWT / RFC-002  
**Host Central do Cofre:** `https://auth.daisugi.com.br` (Porta 8100 sob TLS)  
**Aplicações Integradas:** 
* **DAI** (Smart Reception & Clínicas de IA)
* **KAN-SA** (Auditoria, Inspeção & Medições de Obra)
* **KIGYOU** (Governança ERP, Contratos & Suprimentos)
* **HDC** (Hudson Data Collector / Ingestão de Documentos)
* **HDW** (Hudson Data Worker / Processamento, OCR & RAG)

---

## 1. Princípios de Arquitetura e Homeostase O(1)

1. **Validação Criptográfica Desacoplada O(1):**
   * Nenhum microserviço frontend ou backend consulta o Cofre PAM a cada clique ou mensagem de chat.
   * O microserviço consome a chave pública na inicialização (`/api/v1/auth/public-key`) e valida o token JWT localmente em memória (< 1ms).
2. **Identidade Baseada no E-mail Corporativo Nominal:**
   * O identificador único de acesso (`sub`) é o **e-mail corporativo nominal** do usuário (ex: `fabiana.tonini@sugoisa.com.br`, `vivian.berti@sugoisa.com.br`).
3. **Multi-Cadeiras por Design (Compatibilidade SUGOI):**
   * O usuário pode acumular **múltiplas cadeiras funcionais**, especialmente em perfis de liderança e PMO (ex: Fabiana = Operações + CRM; Vivian = Incorporação + Jurídico Imobiliário; Cintia = G&G; Flávia = Administrativo-Financeiro).
   * O token JWT carrega as claims `cadeira_principal` e a lista completa `cadeiras: [...]`.
4. **Respeito Estrito à Segregação de Funções (SoD - Segregation of Duties):**
   * Maker não pode ser Checker no mesmo fluxo (auto-aprovação estritamente bloqueada).
   * Ações que ultrapassam a alçada financeira do usuário exigem Checker ou dupla assinatura.

---

## 2. Estrutura Canônica do Token JWT (Payload v2.0)

Emitido pelo Cofre-PAM-IGA no handshake e compartilhado unissonamente entre DAI, KAN-SA, KIGYOU, HDC e HDW:

```json
{
  "iss": "https://auth.daisugi.com.br",
  "sub": "fabiana.tonini@sugoisa.com.br",
  "nome": "Fabiana Tonini",
  "tenant_id": "sugoi_sa",
  "tenant_nome": "SUGOI Construtora S.A.",
  "cadeira_principal": "pmo.operacoes@sugoisa.com.br",
  "cadeiras": [
    "pmo.operacoes@sugoisa.com.br",
    "pmo.crm@sugoisa.com.br"
  ],
  "codigos_hierarquicos": ["3", "10.2.2"],
  "alcada": "PMO",
  "perfil": "Operações & CRM",
  "tier": 2,
  "role": "checker",
  "salas_liberadas": [
    "all",
    "quarentena",
    "operacoes",
    "crm",
    "pdca"
  ],
  "sistemas_autorizados": {
    "dai": true,
    "kansa": true,
    "kigyou": true,
    "hdc": true,
    "hdw": true
  },
  "sod_rules": {
    "is_maker": false,
    "can_approve_quarantine": true,
    "max_approval_limit_brl": 50000.00
  },
  "is_core_developer": false,
  "is_sandbox": false,
  "iat": 1791168497,
  "exp": 1791197297
}
```

> **Trava Inegociável:** A claim `"is_core_developer": true` e `"tier": 0` **SÓ PODE** ser emitida se o `"sub"` for estritamente `montanhavermelha@akagui.com` ou `ronaldoakagui@gmail.com`.

---

## 3. Especificação dos Endpoints REST de Federação

### 3.1. `POST /api/v1/auth/handshake` (Login / Onboarding Unificado)
Autentica o usuário pelo e-mail nominal e senha cadastrada no primeiro acesso, cruzando com as cadeiras selecionadas e as travas de SoD.

* **Headers:** `Content-Type: application/json`
* **Request Body:**
  ```json
  {
    "usuario": "fabiana.tonini@sugoisa.com.br",
    "senha": "senha_definida_no_cadastro",
    "tenant_id": "sugoi_sa",
    "cadeiras_selecionadas": [
      "pmo.operacoes@sugoisa.com.br",
      "pmo.crm@sugoisa.com.br"
    ],
    "origem_sistema": "dai_reception",
    "origem_ip": "189.x.x.x"
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
      "sub": "fabiana.tonini@sugoisa.com.br",
      "nome": "Fabiana Tonini",
      "cadeira_principal": "pmo.operacoes@sugoisa.com.br",
      "cadeiras": ["pmo.operacoes@sugoisa.com.br", "pmo.crm@sugoisa.com.br"],
      "role": "checker",
      "sistemas": ["dai", "kansa", "kigyou", "hdc", "hdw"]
    }
  }
  ```

---

### 3.2. `GET /api/v1/auth/public-key` (Chave Pública para Validação Local)
Permite que os servidores locais e instâncias de frontend da DAI, KAN-SA, KIGYOU, HDC e HDW obtenham a chave pública oficial.

* **Response (HTTP 200 OK):**
  ```json
  {
    "algorithm": "RS256",
    "public_key_pem": "-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8A...\n-----END PUBLIC KEY-----",
    "kid": "daisugi_vault_key_2026_v2"
  }
  ```

---

### 3.3. `POST /api/v1/governance/sod/validate-action` (Validação de Ação & Quarentena)
Invocado quando qualquer usuário tenta aprovar medição (Kan-sa), emitir ordem de pagamento (Kigyou) ou liberar documento em quarentena (DAI/HDC).

* **Headers:** `Authorization: Bearer <token_jwt>`
* **Request Body:**
  ```json
  {
    "acao": "LIBERACAO_MEDICAO_OBRA",
    "documento_hash": "a1b2c3d4e5f6...",
    "maker_identity": "igor.santos@sugoisa.com.br",
    "valor_brl": 32000.00,
    "sistema_origem": "KAN-SA"
  }
  ```
* **Regras de Decisão:**
  * Se `token.sub == request.maker_identity`: **HTTP 403 Forbidden** (*Violação SoD Tóxica: Maker não pode ser Checker*).
  * Se `token.alcada_limite < request.valor_brl`: **HTTP 403 Forbidden** (*Exige alçada superior ou dupla aprovação*).
  * Se aprovado: **HTTP 200 OK** com registro imediato no Ledger Sagrado de Auditoria e emissão de comprovante criptográfico.

---

### 3.4. `POST /api/v1/audit/log-event` (Trilha Sagrada Imutável - Merkle Chained)
Permite que todos os sistemas gravem ações operacionais com sanitização automática LGPD e encadeamento SHA-256.

* **Headers:** `Authorization: Bearer <token_jwt>`
* **Request Body:**
  ```json
  {
    "tenant_id": "sugoi_sa",
    "acao": "MEDICAO_LANCADA_CAMPO",
    "detalhes": {
      "obra": "São Mateus",
      "engenheiro": "igor.santos@sugoisa.com.br",
      "etapa": "Estrutura 3º Pavimento",
      "valor_estimado": 45000.00
    },
    "status": "SUCCESS",
    "origem_sistema": "KAN-SA"
  }
  ```

---

## 4. Diretrizes Uníssonas para os Frontends

Todos os frontends do ecossistema (**DAI, KAN-SA, KIGYOU, HDC, HDW**) devem aderir aos seguintes requisitos de interface:

1. **Tela de Primeiro Acesso / Cadastro:**
   * Campo de E-mail corporativo nominal (`@sugoisa.com.br`).
   * Campo para criação de senha pessoal segura.
   * **Seletor de Cadeiras Funcionais (Multi-Select com Flags):** O usuário seleciona suas atribuições oficiais com base no Catálogo Canônico da SUGOI.
2. **Identidade Visual e Badge de Cadeira Ativa:**
   * O cabeçalho de todos os sistemas deve exibir o nome do usuário acompanhado da **Cadeira Ativa** e um seletor rápido (caso ele possua múltiplas cadeiras homologadas, ex: alternar entre visão *Operações* e visão *CRM*).
3. **Tratamento de Sessão Transparente (SSO):**
   * Armazenamento padronizado de token em `localStorage` sob a chave `daisugi_access_token` e cookie de domínio compartilhado `.daisugi.com.br`.
   * Ao navegar da DAI para o Kan-sa ou Kigyou, o frontend verifica a presença do token válido e dispensa nova autenticação.
