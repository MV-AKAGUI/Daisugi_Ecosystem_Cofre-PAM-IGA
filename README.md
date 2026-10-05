# 🏛️ Daisugi Ecosystem Cofre-PAM-IGA
**Autoridade Central de Identidade, Governança, Cofre de Segredos e Gestão de Privilégios**  
*Ecossistema Soberano DAISUGI — Plataforma Multi-Tenant Enterprise*

---

## 1. Visão Geral e Propósito

O **`Daisugi_Ecosystem_Cofre-PAM-IGA`** é o núcleo central de segurança, conformidade e custódia de credenciais da **Daisugi Tecnologias**. Ele opera sob o modelo arquitetural *Hub & Spoke*, atuando como o único Provedor de Identidade (IdP), Cofre de Segredos (Secret Vault) e Orquestrador de Governança para todas as aplicações do ecossistema:

* **DAI (Smart Reception Framework):** Recepção inteligente, triagem e roteamento de atendimentos.
* **KAN-SA (Audit & Passive Engine):** Auditoria contábil, pericial e quarentena de contratos/CCBs.
* **HUDSON (Event Hub & DDL Orchestrator):** Barramento assíncrono de eventos e orquestração pesada.
* **Aplicações Futuras da Daisugi:** Qualquer novo produto herda imediatamente esta blindagem.

---

## 2. A Separação Sagrada: PAM vs. IGA

Para garantir compliance com auditorias internacionais (SOX, ISO 27001, LGPD e NIST), o sistema desacopla estritamente **Operação** de **Política**:

```
+---------------------------------------------------------------------------------------------------+
|                            DAISUGI ECOSYSTEM COFRE-PAM-IGA                                        |
+---------------------------------------------------------------------------------------------------+
|                                                                                                   |
|   [ IGA: A POLÍTICA E O COMPLIANCE ]               [ PAM: A OPERAÇÃO E A EXECUÇÃO ]               |
|   • Catálogo de Cadeiras Corporativas             • Cofre de Segredos (Secrets Vault AES-256)     |
|   • Atribuição Cadeira Funcional vs. Nominal      • Emissão de Tokens JWT Criptografados          |
|   • Matriz SoD (Segregation of Duties)            • Rotação Dinâmica de Chaves Assíncronas        |
|   • Alçadas Financeiras e Limites de Risco        • Elevação Just-in-Time (JIT Access)            |
|   • Trilha Imutável de Auditoria RACI             • Travas Maker/Checker na Quarentena            |
|                                                                                                   |
+---------------------------------------------------------------------------------------------------+
```

1. **PAM (Privileged Access Management) — A Operação e a Execução:**
   * Custódia segura de senhas, chaves de API externas (Gemini, Ollama, Serpro, Cartórios).
   * Rotação automatizada de credenciais de bancos de dados.
   * Concessão de privilégios temporários (*Break-Glass*) para incidentes críticos.
   * Validação em tempo real do princípio **Maker ≠ Checker** (quem gera documento não aprova despesa).

2. **IGA (Identity Governance and Administration) — A Política e o Compliance:**
   * Definição formal de quem pode ocupar qual cadeira.
   * Gestão do ciclo de vida das identidades (Admissão, Mudança de Cargo e Desligamento).
   * Prevenção e detecção de conflitos de Segregação de Funções (SoD) antes da atribuição.
   * Campanhas periódicas de recertificação de acessos para a Diretoria e Auditoria.

---

## 3. Trava Soberana de Desenvolvedor (Core Dev Lock)

O sistema implementa uma blindagem matemática rigorosa: **nenhum cliente contratante (como a SUGOI ou outros) tem, terá ou poderá adquirir acesso a código-fonte, branches ou administração do núcleo da plataforma.**

```
+---------------------------------------------------------------------------------------------------+
|                                  TIERS DE PRIVILÉGIO DO SISTEMA                                   |
+---------------------------------------------------------------------------------------------------+
|  TIER 0: CORE DEVELOPER (DAISUGI SOBERANA)                                                        |
|  * Identidades Exclusivas: montanhavermelha@akagui.com | ronaldoakagui@gmail.com                   |
|  * Acesso: Git Repos, Servidores OCI/Docker, DDL de Bancos, Algoritmos Neurais e Chaves Mestras   |
|  * O CLIENTE NÃO TEM ACESSO, NÃO TEM SENHA E NÃO EXECUTA ALTERAÇÕES DE CÓDIGO                     |
+---------------------------------------------------------------------------------------------------+
                                                  │
                                                  ▼
+---------------------------------------------------------------------------------------------------+
|  TIER 1: TENANT ADMIN (Ex: CISO / TI do Cliente X)                                                |
|  * Escopo: 100% restrito ao Tenant do cliente (ex: sugoi_sa). Atribui pessoas às cadeiras         |
|  * Limitações: Não enxerga código, não acessa servidor de deploy, não altera rotas Python        |
+---------------------------------------------------------------------------------------------------+
                                                  │
                                                  ▼
+---------------------------------------------------------------------------------------------------+
|  TIER 2 & 3: CADEIRAS DE NEGÓCIO DO CLIENTE (Checkers e Makers)                                   |
|  * Checkers: Controller, Advogado, Diretor (Validam riscos, emitem pareceres e aprovam quarentena) |
|  * Makers: Engenheiro, Comprador, Operador (Submetem dúvidas, notas fiscais e relatórios)        |
+---------------------------------------------------------------------------------------------------+
```

---

## 4. Arquitetura Multi-Tenant White-Label

O `Daisugi_Ecosystem_Cofre-PAM-IGA` foi concebido para atender múltiplos clientes simultâneos com isolamento criptográfico absoluto:
* Cada cliente possui um `tenant_id` exclusivo (ex: `sugoi_sa`, `cliente_alfa_sa`).
* As cadeiras corporativas, limites de alçada e matrizes RACI são parametrizáveis por tenant.
* A infraestrutura do Cofre é hospedada sob controle soberano da Daisugi (na nuvem Oracle ou dedicada), garantindo que um cliente jamais acesse a memória ou o cofre de outro.

---

## 5. Estrutura do Repositório

```
Daisugi_Ecosystem_Cofre-PAM-IGA/
├── README.md                              # Visão geral e princípios do ecossistema
├── PROTOCOLO_MUDANCAS_E_AUDITORIA_SAGRADA.md # Diretório Sagrado de Auditoria & Protocolo de RFC
├── CONTRATO_API_PAM_IGA.md                # Especificação dos endpoints, contratos e JWT
├── MATRIZ_GOVERNANCA_MULTI_TENANT.md      # Mapeamento de Cadeiras, IGA e regras SoD
├── daisugi_vault_core.py                  # Servidor FastAPI do Cofre PAM-IGA & Sacred Ledger
├── daisugi_auth_guard.py                  # SDK / Middleware cliente para DAI e Kan-sa
├── requirements.txt                       # Dependências mínimas de alta performance
└── .gitignore                             # Arquivos ignorados pelo Git
```

---

## 6. Governança, Compliance e Transparência Radical

* **Diretório Sagrado de Auditoria Imutável:** Todas as ações, acessos e respostas de IA contam com encadeamento de integridade SHA-256 e verificação matemática de não-adulteração.
* **Usuário Oficial de Teste Homologado:** A cadeira `qa.sandbox@daisugi.com.br` permite execução de testes e homologação sem poluição dos relatórios do cliente.
* **Protocolo de Gestão de Mudanças (RFC):** Separação estrita entre mudanças operacionais (Tipo A) e mudanças estruturais de compliance do cliente (Tipo B, exigindo aprovação formal do Tenant Admin).
* **Mantenedor Principal:** Daisugi Tecnologias
* **Autoridade Primária:** `montanhavermelha@akagui.com`
* **Engenharia de Plataforma:** `ronaldoakagui@gmail.com`

