# ARQUITETURA DE FEDERAÇÃO DE CADEIRAS & MATRIZ DE ACESSO SUGOI
## Integração de Identidades IGA / PAM entre SUGOI S.A. e Ecossistema DAISUGI (Dai, Kan-sa, Kigyou)

**Data de Emissão:** 13 de Outubro de 2026  
**Autor Técnico:** Dr. Tylor (Engenheiro-Chefe de Segurança e Arquitetura de Sistemas)  
**Coordenação:** PMO de TI & Programação Daisugi  
**Referência Canônica SUGOI:** `H:\Drives compartilhados\APLICAÇÕES - SUGOI-SA\01_SUGOI_CADEIA_DE_VALOR\06_PROCESSOS` (`SUGOI_Modelo_Gestao_PAM_R03.xlsx`)  
**Status:** Especificação Arquitetural e Contrato de Governança Homologado

---

## 1. Diretriz Estratégica & Decisão de Escopo

1. **Supressão do Path `/sugoi`:**
   * Fica revogada qualquer segmentação via sufixo de rota (`/sugoi`). O ecossistema Daisugi (`dai.daisugi.com.br`, `kansa.daisugi.com.br`, `kigyou.daisugi.com.br`) opera nativamente preparado para a estrutura organizacional da **SUGOI S.A.**
2. **Identificador Primário de Acesso (Login):**
   * O **E-mail Corporativo Nominal** (`nome.sobrenome@sugoisa.com.br`) é a chave de identidade universal (Subject `sub`).
3. **Mecanismo de Onboarding / Primeiro Acesso:**
   * No primeiro acesso, o usuário autentica-se/cadastra sua credencial e seleciona as **Cadeiras Funcionais** que ocupa na SUGOI.
   * **Multi-Cadeira por Design:** Perfis de liderança e PMO possuem permissão formal para selecionar e acumular cadeiras operacionais e comitês de acordo com o catálogo da SUGOI (ex: Fabiana Tonini = Operações + CRM; Vivian Berti = Incorporação + Jurídico Imobiliário; Cintia Godinho = Gente, Cultura & Gestão).
4. **Respeito Estrito à Segregação de Funções (SoD - Segregation of Duties):**
   * Nenhuma concessão de cadeiras poderá violar os conflitos tóxicos de SoD catalogados (ex: Maker de Contas a Pagar não pode ser Checker/Aprovador do mesmo fluxo financeiro).

---

## 2. Topografia de Identidades: Quem é Quem na Estrutura SUGOI

Baseado no Catálogo de Cadeiras e E-mails Corporativos da SUGOI (`SUGOI_Modelo_Gestao_PAM_R03.xlsx`):

| Identidade Nominal | E-mail Corporativo Nominal | Cadeira Principal | Código Hierárquico | Alçada / Perfil | Escopo no Ecossistema Daisugi |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Ronaldo Akagui** | `ronaldo.akagui@sugoisa.com.br` | Presidência | `1` | Diretor Presidente | Acesso Soberano / Decisão Estratégica / Auditoria Global em todos os sistemas |
| **Renato Barroso** | `renato.barroso@sugoisa.com.br` | Operações | `3` | Diretor de Operações | Visão Executiva Obras, Produção, Planejamento e Performance |
| **Luiz Perez** | `luiz.perez@sugoisa.com.br` | Engenharia | `12` | Diretor de Engenharia | Aprovação Técnica Global, Projetos e Baseline |
| **Cintia Godinho** | `cintia.godinho@sugoisa.com.br` | Gente, Cultura e Gestão | `2` | PMO G&G | Gestão de Identidades JML, Ciclo de Vida de Colaboradores e RH |
| **Fabiana Tonini** | `fabiana.tonini@sugoisa.com.br` | Operações & CRM | `3` / `10.2.2` | PMO Operações / CRM | Gestão Operacional, Monitoramento PDCA, Relacionamento e Atendimento |
| **Vivian Berti** | `vivian.berti@sugoisa.com.br` | Incorporação & Jurídico Imobiliário | `11` / `10` | PMO Incorporação / Imob | Gestão de Licenciamento, Legalizações, Terrenos e GED Imobiliário |
| **Pedro Junior** | `pedro.junior@sugoisa.com.br` | Engenharia | `12` | PMO Engenharia | Coordenação de Engenharia, Orçamentos, Planejamento e Obras |
| **Fernando Brasil** | `fernando.brasil@sugoisa.com.br` | Controladoria | `5` | PMO Controladoria | Governança Contábil/Fiscal, Auditoria Independente e Fechamento |
| **Flávia Akagui** | `flavia.akagui@sugoisa.com.br` | Administrativo Financeiro | `6` | PMO Financeiro | Gestão Financeira, Contas a Pagar/Receber, Tesouraria e Facilities |
| **Weslley Coradini** | `weslley.coradini@sugoisa.com.br` | Tecnologia da Informação | `3.2` | Especialista TI | Administração de Sistemas, Conectores, Infraestrutura e IGA |
| **Simone Furquim** | `simone.furquim@sugoisa.com.br` | Suprimentos | `13` | Especialista Suprimentos | Cotações, Compras, Gestão de Contratos de Suprimentos |
| **Lukas Kostakis** | `lukas.kostakis@sugoisa.com.br` | Produção de Obras | `12.4` | Especialista Produção | Coordenação de Obras, Medições e Engenharia de Campo |
| **Engenheiros de Obra** (Igor Santos, Wilson Freitas, Leonardo Figueiredo, André Carvalho, Larissa Nunes) | `engenheiro.[obra]@sugoisa.com.br` | Produção de Obras Local | `12.4` | Engenheiro Residente | Lançamento de Medições, Diário de Obra, Apontamentos de Campo |
| **Grazielli Nascimento** | `grazielli.nascimento@sugoisa.com.br` | Contas a Pagar | `6.2.2` | Auxiliar Contas a Pagar | Lançador Operacional (Maker) de Títulos e Programações |
| **Nathália Rodrigues** | `nathalia.rodrigues@sugoisa.com.br` | Contas a Receber | `6.2.1` | Analista Contas a Receber | Lançamento e Baixas de Recebíveis, Extrato e Cobrança |
| **Denise Segatelli** | `denise.segatelli@sugoisa.com.br` | Facilities | `6.1.1` | Assistente Facilities | Requisições Administrativas, Chamados e Infraestrutura |
| **Paola Alencar** | `paola.alencar@sugoisa.com.br` | Jurídico Empresarial | `7` | Especialista Jurídico | Pareceres Jurídicos, Contratos Societários e Contencioso |

---

## 3. Matriz de Mapeamento: Cadeira SUGOI ➔ Módulos DAI, KAN-SA e KIGYOU

As permissões operacionais do usuário em cada sistema do ecossistema são derivadas **automaticamente** da composição de suas cadeiras selecionadas:

```
+---------------------------------------------------------------------------------------+
|                                USUÁRIO SUGOI                                          |
|                       (nome.sobrenome@sugoisa.com.br)                                 |
+---------------------------------------------------------------------------------------+
                                        |
                 [Possui 1 ou mais Cadeiras Funcionais Homologadas]
                                        |
       +--------------------------------+-------------------------------+
       |                                |                               |
       v                                v                               v
+--------------+               +------------------+             +-----------------+
|   DAI (AI)   |               |     KAN-SA       |             |     KIGYOU      |
|  Assistente  |               |  Auditoria, Medição |             | Governança ERP, |
|  & Análises  |               |   & Inspeção Obras |             | Suprimentos & Fin|
+--------------+               +------------------+             +-----------------+
```

### 3.1. Sistema DAI (Inteligência & Análise Operacional)
* **PMOs e Diretores:** Acesso ao console de BI preditivo, resumos executivos de atas, alertas de desvio de cronograma e custos por empreendimento.
* **Analistas e Auxiliares Financeiros:** Interações guiadas sobre conciliação bancária, extração de relatórios de títulos em aberto e minutas de e-mail/notificação.
* **Engenharia e Obras:** Consulta a normas de execução, conferência de especificações técnicas de projetos e memorial descritivo.

### 3.2. Sistema KAN-SA (Auditoria, Inspeções & Medições Técnicas)
* **Engenheiros Residentes e Produção (`12.4`):** Lançamento de medições de campo, checklist de avanço físico de obra e registro fotográfico.
* **PMO de Engenharia e Operações (`12`, `3`):** Validação técnica das medições (Checker), liberação de boletins de medição para faturamento.
* **Controladoria e Auditoria (`5`):** Inspeção de conformidade de processos, trilha de auditoria digital e conferência documental.
* **Qualidade e Segurança (`8`):** Fichas de verificação de serviço (FVS), não-conformidades e laudos ambientais/trabalhistas.

### 3.3. Sistema KIGYOU (Gestão Empresarial, Suprimentos & Governança de Contratos)
* **Suprimentos (`13`):** Cotações, mapas de concorrência, emissão de ordens de compra e qualificação de fornecedores.
* **Administrativo Financeiro (`6`):**
  * *Lançador (Grazielli):* Registro de pedidos de pagamento e upload de notas fiscais vinculadas ao SharePoint.
  * *Aprovador (Flávia / Diretor):* Alçada de aprovação financeira com bloqueio inviolável de auto-aprovação (SoD).
* **Incorporação e Jurídico Imobiliário (`10`, `11`):** Acompanhamento de escrituras, contratos de aquisição de terreno, licenças prévias e documentação cartorária.

---

## 4. Integração Operacional com Teams e SharePoint

Conforme exigido pelo rito de processos da SUGOI:
1. **Notificações Automatizadas via Teams (Webhooks / Bot):**
   * Quando o Engenheiro lança a medição no **Kan-sa**, um alerta no canal do Microsoft Teams (`Canal: Obras - Medições`) e um e-mail são disparados para o **Auxiliar/Analista Financeiro** e para o **PMO de Engenharia**.
   * Ao aprovar a medição, a tarefa de programação no contas a pagar é gerada no **Kigyou**.
2. **Repositório Unificado SharePoint:**
   * Nenhum arquivo pesado (NF, contrato assinado, laudo técnico) é armazenado em bancos de dados relacionais soltos.
   * Todos os uploads realizados no Dai, Kan-sa ou Kigyou são organizados na árvore padronizada do **SharePoint da SUGOI** através das APIs do Microsoft Graph, associados ao ID da Cadeira e ao código do Empreendimento.

---

## 5. Implementação no Repositório Daisugi Cofre-PAM-IGA

O SDK `daisugi_auth_guard.py` e o cofre `daisugi_vault_core.py` são estendidos para incorporar:
1. A tabela de cadeiras homologadas da SUGOI (`SUGOI_CHAIRS_CATALOG`).
2. O validador de SoD impeditivo de conflitos no momento do provisionamento.
3. A emissão de Tokens JWT contendo o claim enriquecido `chairs: [...]` e `permissions: [...]`.
