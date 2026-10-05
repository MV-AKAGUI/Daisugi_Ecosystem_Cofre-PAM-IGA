# 📜 Protocolo de Gestão de Mudanças (RFC) & Diretório Sagrado de Auditoria Imutável
**Daisugi Ecosystem Cofre-PAM-IGA**  
**Versão:** 2.0.0 — Enterprise Governance, Compliance & Transparency  
**Aplicabilidade:** DAI (Smart Reception), KAN-SA (Quarentena), HUDSON e Microserviços

---

## 1. Visão Geral e Princípios Fundamentais

Para elevar a governança e o compliance ao mais alto nível corporativo (atendendo auditorias internacionais **SOX, ISO 27001, LGPD e NIST**), a Daisugi adota duas salvaguardas inegociáveis:

1. **Transparência Radical com Trilha Sagrada de Auditoria:** O cliente tem acesso em tempo real ao registro auditável e matematicamente inviolável de tudo o que foi acessado, perguntado, respondido ou deliberado pela IA e pelos usuários dentro do seu ambiente.
2. **Protocolo Rigoroso de Gestão de Mudanças (RFC):** Nenhuma alteração estrutural que afete a segurança, o compliance ou as regras de negócio do cliente é aplicada sem rito formal e dupla aprovação.

---

## 2. O Diretório Sagrado de Auditoria Imutável (The Sacred Audit Ledger)

O banco de dados do **Cofre-PAM-IGA** mantém um diretório/schema sagrado de dados (em produção mapeado para `daisugi_vault_audit.sacred_ledger`), operando sob uma estrutura de **Hash Encadeado SHA-256 (Merkle Chained Ledger)**:

```
+---------------------------------------------------------------------------------------------------+
|                              DIRETÓRIO SAGRADO DE AUDITORIA (COFRE-PAM-IGA)                       |
+---------------------------------------------------------------------------------------------------+
|                                                                                                   |
|  [ EVENTO 01 ]                [ EVENTO 02 ]                    [ EVENTO 03 ]                      |
|  • Timestamp: T0              • Timestamp: T1                  • Timestamp: T2                    |
|  • Tenant: sugoi_sa           • Tenant: sugoi_sa               • Tenant: sugoi_sa                 |
|  • Sub: comprador@...         • Sub: controller@...            • Sub: qa.sandbox@daisugi          |
|  • Ação: Pergunta DAI         • Ação: Aprovação Quarentena     • Ação: Teste Homologado           |
|  • PrevHash: 000...000        • PrevHash: SHA256(Evento 01)    • PrevHash: SHA256(Evento 02)      |
|  • Hash: SHA256(...)          • Hash: SHA256(...)              • Hash: SHA256(...)                |
|               └────────────────────────►└───────────────────────────────►                         |
+---------------------------------------------------------------------------------------------------+
```

### 🔍 O que é Registrado no Diretório Sagrado:
* **Acessos e Autenticações:** Sucessos, tentativas com senha incorreta, bloqueios por falta de cadeira.
* **Perguntas e Sinapses Clínicas na DAI:** A queixa enviada pelo usuário, a sala clínica consultada (Dr. Taylor, Fiscal, Jurídico) e a intenção capturada.
* **Respostas dadas pela IA:** Resposta final consolidada, distância vetorial do RAG, modelo utilizado e tempo de resposta.
* **Quarentena e Deliberações SoD:** Solicitações de Maker, aprovações/rejeições de Checker e justificativas.
* **Identificação de Sessões:** Se o evento foi executado por um colaborador real ou pelo usuário de teste (`qa.sandbox`).

### 🛡️ Demonstração Matemática de Não-Adulteração:
* O endpoint `GET /api/v1/audit/verify-integrity` reprocessa todo o encadeamento dos blocos de log. Se qualquer administrador, hacker ou intervenção manual tentar alterar uma única vírgula ou excluir um evento passado, a cadeia quebra e o sistema acusa corrupção criptográfica instantaneamente.
* O cliente pode solicitar a extração ou consultar via API: `GET /api/v1/audit/tenant-report/{tenant_id}`.

---

## 3. Cadeira Oficial de Teste Homologado da Daisugi (`qa.sandbox`)

Para evitar o uso de credenciais arbitrárias ou confusão com contas de produção:

* **Cadeira Canônica:** `qa.sandbox@daisugi.com.br`
* **Nome de Registro:** `Daisugi QA & Compliance Sandbox`
* **Tenant Nativo:** `daisugi_sandbox` (com permissão para atuar em modo homologação demarcada)
* **Regras de Compliance do Sandbox:**
  1. **Marca d'Água Obrigatória:** Toda interação gerada por este usuário recebe a flag `"is_sandbox": true` no Diretório Sagrado de Auditoria.
  2. **Isolamento de Métricas:** Os testes realizados não distorcem os KPIs de negócio e os relatórios financeiros do cliente.
  3. **Segurança Soberana:** Possui permissão de teste ampla em salas clínicas, mas não pode executar aprovações SoD definitivas de contratos reais sem a presença de uma Cadeira Checker do cliente.

---

## 4. Protocolo de Gestão de Mudanças (RFC - Request For Change)

Toda e qualquer intervenção nos ambientes compartilhados ou dedicados deve obedecer à **Matriz de Classificação de Mudanças**:

```
                                    ┌────────────────────────┐
                                    │   PROPOSTA DE MUDANÇA  │
                                    └───────────┬────────────┘
                                                │
                       ┌────────────────────────┴────────────────────────┐
                       ▼                                                 ▼
             [ MUDANÇA TIPO A ]                                [ MUDANÇA TIPO B ]
             (Operacional / UI / Perf)                         (Estrutural / Compliance)
                       │                                                 │
     • Refinamento de prompts internos da IA            • Alterações em tabelas ou schemas
     • Otimização de queries e cache Redis              • Modificação de regras SoD Maker/Checker
     • Melhorias visuais e ergonômicas no Front         • Alteração de limites de alçadas financeiras
     • Hotfixes que não alterem permissões              • Mudanças no catálogo IGA do cliente
                       │                                                 │
                       ▼                                                 ▼
          ┌─────────────────────────┐                      ┌───────────────────────────┐
          │   Aprovação Ágil:       │                      │   Aprovação Obrigatória:  │
          │   Engenharia Daisugi    │                      │   Daisugi + Tenant Admin  │
          │   (Registro em Log)     │                      │   (CISO / TI do Cliente)  │
          └─────────────────────────┘                      └───────────────────────────┘
```

### 4.1. Classificação Detalhada:

| Tipo | Denominação | Escopo e Exemplos | Rito de Aprovação |
| :---: | :--- | :--- | :--- |
| **Tipo A** | **Operacional / Melhoria Contínua** | • Ajustes finos nos prompts de médicos virtuais.<br>• Otimização de tempos de resposta e cache O(1).<br>• Ajustes de layout, cores e responsividade.<br>• Atualização de bibliotecas sem impacto de segurança. | **Aprovação Interna Daisugi**.<br>Aplica-se com registro automático no ledger. |
| **Tipo B** | **Estrutural / Compliance do Cliente** | • Criação ou exclusão de Cadeiras no catálogo do cliente.<br>• Alteração de matriz de Segregação SoD.<br>• Mudança de limites de alçada em BRL.<br>• Modificação no tratamento ou retenção de dados sensíveis.<br>• Alteração de políticas de senha e autenticação. | **Dupla Validação Obrigatória (RFC)**.<br>Proposta técnica formal + Validação pelo Tenant Admin / TI da SUGOI (`suporte.ti@sugoisa.com.br`). |

---

### 4.2. Ciclo de Vida da RFC Tipo B (Passo a Passo)

1. **Submissão da Proposta:**
   * A Daisugi ou o Cliente emite uma requisição via `POST /api/v1/governance/rfc/propose`, gerando um código único (ex: `RFC-20261005-001`).
   * A proposta detalha: Justificativa Técnica, Escopo, Impacto Previsto e Plano de Rollback.
2. **Avaliação pelo Cliente (Tenant Admin / CISO):**
   * O responsável de TI/Compliance do cliente acessa a lista de RFCs pendentes (`GET /api/v1/governance/rfc/list/{tenant_id}`).
3. **Deliberação e Assinatura Digital:**
   * O aprovador envia a decisão via `POST /api/v1/governance/rfc/approve`.
   * A decisão (Aprovado / Rejeitado) e o parecer técnico são gravados com hash criptográfico no **Diretório Sagrado de Auditoria**.
4. **Aplicação Segura:**
   * Somente após a aprovação formal a engenharia aplica a alteração no ambiente.

---

## 5. Resumo dos Endpoints no Cofre-PAM-IGA

| Método | Endpoint | Finalidade |
| :--- | :--- | :--- |
| `POST` | `/api/v1/audit/log-event` | Grava evento na Trilha Sagrada com sanitização LGPD e SHA-256 encadeado (assíncrono em < 1ms via BackgroundTasks). |
| `GET` | `/api/v1/audit/tenant-report/{tenant_id}` | Extrato completo de transparência para o cliente (isolado por tenant). |
| `GET` | `/api/v1/audit/verify-integrity` | Verificador matemático de não-adulteração da base (recalcula toda a cadeia). |
| `POST` | `/api/v1/governance/rfc/propose` | Submissão de RFC Tipo A ou Tipo B com persistência GitOps em `rfcs/`. |
| `POST` | `/api/v1/governance/rfc/approve` | Parecer e aprovação formal de RFC (Gate SoD com trava de tenant admin). |
| `GET` | `/api/v1/governance/rfc/pending-count/{tenant_id}` | Contador leve para renderização de badge de alerta no Lobby da DAI. |
| `GET` | `/api/v1/governance/rfc/list/{tenant_id}` | Consulta de status e histórico completo de mudanças. |

---

## 6. Arquitetura de Performance Leve & LGPD em Tempo Real

1. **Sanitizador LGPD Nativo:** Todas as strings de detalhes passam por regex compiladas em memória antes de entrar no ledger, mascarando CPFs, números de cartões e telefones (`[CPF_PROTEGIDO_LGPD]`), garantindo compliance sem onerar a CPU.
2. **Persistência Assíncrona Leve:** O Cofre responde em microssegundos para a DAI e descarrega a gravação append-only em `sacred_audit_ledger.jsonl` em segundo plano via `BackgroundTasks`.
3. **Resiliência a Reinicializações:** No boot, o Cofre faz a leitura do último registro histórico em tempo $O(1)$, garantindo que a cadeia de hash continue contínua e íntegra mesmo após manutenções ou deploys.
4. **GitOps de Compliance:** Cada RFC proposta ou aprovada gera uma cópia estruturada em `rfcs/RFC-YYYYMMDD-NNN.json`, garantindo dupla trilha de auditoria (na API do Cofre e no histórico do Git).

