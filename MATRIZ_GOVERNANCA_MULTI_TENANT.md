# 🏢 Matriz de Governança Multi-Tenant e Catálogo de Cadeiras IGA
**Subsistema:** Daisugi Ecosystem Cofre-PAM-IGA  
**Finalidade:** Gestão de Identidades, Alçadas, Compliance e Segregação de Funções (SoD)

---

## 1. Estrutura Hierárquica Multi-Tenant

O Cofre-PAM-IGA suporta múltiplos inquilinos corporativos de forma totalmente isolada. Cada inquilino possui sua própria árvore de Cadeiras e limites de alçada, herdando o motor central de auditoria:

```
[ DAISUGI ECOSYSTEM COFRE-PAM-IGA ]
  ├── [ TENANT: sugoi_sa ] (SUGOI Construtora S.A.)
  │     ├── Código 1.01: Presidência
  │     ├── Código 1.05: Controladoria & Finanças (Checker)
  │     ├── Código 1.10: Jurídico Imobiliário (Checker)
  │     ├── Código 2.01: Suprimentos & Compras (Maker)
  │     └── Código 2.05: Engenharia & Obras (Maker)
  │
  └── [ TENANT: cliente_futuro_sa ] (Pronto para Expansão)
        ├── Código Setorial Customizado
        └── Catálogo de Cadeiras Parametrizado
```

---

## 2. Catálogo Canônico de Cadeiras (Tenant SUGOI)

| Código | Cadeira Funcional (Principal) | Alçada / Perfil | Papel SoD | Limite de Aprovação (BRL) | Permissões no Ecossistema |
| :---: | :--- | :--- | :--- | :---: | :--- |
| **0.00** | `montanhavermelha@akagui.com`<br>`ronaldoakagui@gmail.com` | **Core Developer (Daisugi Master)** | **Soberano** | **Ilimitado (Plataforma)** | Acesso total a código, infraestrutura, cofre e auditoria de todos os tenants. |
| **0.05** | `qa.sandbox@daisugi.com.br` | **Daisugi QA & Compliance Sandbox** | **Homologação** | **Auditado (Sandbox)** | Testes amplos auditados com marca d'água obrigatória (`is_sandbox: true`). |
| **1.01** | `diretor.presidente@sugoisa.com.br` | Presidência | Super-Checker | R$ 10.000.000,00 | Visão holística de todas as salas da DAI, métricas financeiras e auditoria geral. |
| **1.02** | `diretor.operacoes@sugoisa.com.br` | Diretoria de Operações | Checker Máximo | R$ 500.000,00 | Aprovação final de quarentenas de alto impacto e liberações de medição. |
| **1.05** | `controller@sugoisa.com.br` | Controladoria Geral | Checker Quarentena | R$ 100.000,00 | Validação de Hashes de CCB, quitação de notas, travas ERP e SoD. |
| **1.10** | `advogado.imobiliario@sugoisa.com.br` | Jurídico Imobiliário | Checker Legal | N/A (Parecer) | Emissão de pareceres técnicos, análise de minutas e ônus imobiliários. |
| **1.15** | `suporte.ti@sugoisa.com.br`<br>`ciso@sugoisa.com.br` | Governança & TI Local SUGOI | Tenant Admin | N/A (Governança) | Atribuição de usuários às cadeiras da SUGOI, auditoria de logs, extração de relatórios e aprovação de RFCs Tipo B. |
| **2.01** | `comprador@sugoisa.com.br` | Suprimentos | Maker Solicitante | R$ 0,00 | Abertura de chamados, envio de propostas e consultas de procedimentos. |
| **2.05** | `engenheiro.obra@sugoisa.com.br` | Engenharia / Obras | Maker Solicitante | R$ 0,00 | Submissão de relatórios de medição física e consultas técnicas na DAI. |

---

## 3. Matriz de Conflitos Tóxicos de SoD (Segregation of Duties)

O motor IGA avalia preventivamente e bloqueia em tempo real qualquer tentativa de acúmulo de funções conflitantes:

| Tentativa de Conflito | Cadeira A | Cadeira B | Veredito IGA | Ação Automática do Cofre |
| :--- | :--- | :--- | :---: | :--- |
| **Conflito 1: Auto-Aprovação** | Maker (Comprador/Engenheiro) | Checker (Controller/Diretor) | ⛔ **TÓXICO** | Bloqueio imediato. O Maker nunca aprova o próprio documento. |
| **Conflito 2: Blindagem de Código** | Tenant Admin (CISO do Cliente) | Core Developer (Daisugi) | ⛔ **PROIBIDO** | Rejeição de emissão de chave. Acesso restrito aos e-mails da Akagui. |
| **Conflito 3: Fechamento Contábil** | Operador de Lançamento | Auditor de Balancete | ⛔ **TÓXICO** | Exige aprovação de cadeira independente (Checker). |

---

## 4. Diretório Sagrado de Auditoria & Protocolo de Mudanças (RFC)

Para assegurar conformidade total com LGPD, SOX e ISO 27001:
1. **Diretório Sagrado de Auditoria Imutável:** Todas as ações, acessos e respostas de IA são assinadas com SHA-256 encadeado e disponibilizadas para o cliente via relatório de transparência.
2. **Classificação de Mudanças (RFC):**
   - **Tipo A (Operacional / UI / Performance):** Não afetam segurança e compliance do cliente; gerenciadas com agilidade pela Engenharia da Daisugi.
   - **Tipo B (Estrutural / Governança do Cliente):** Alterações de dados, alçadas ou regras SoD exigem protocolo formal de RFC aprovado pelo Tenant Admin (`suporte.ti@sugoisa.com.br`).
3. Para mais detalhes, consulte o documento normativo: [`PROTOCOLO_MUDANCAS_E_AUDITORIA_SAGRADA.md`](file:///c:/Users/Ronaldo%20Akagui.SUG00245/DAISUGI_TECNOLOGIAS/Daisugi_Ecosystem_Cofre-PAM-IGA/PROTOCOLO_MUDANCAS_E_AUDITORIA_SAGRADA.md).

