# Base de Conhecimento

> [!TIP]
> **Prompt usado para esta etapa:**
> 
> Organize a base de conhecimento do agente "Ben" usando os 5 arquivos da pasta `data/`. Explique para que serve cada arquivo no contexto de um planejador financeiro que estrutura metas, calcula prazos e sugere métodos de economia (sem recomendar investimentos específicos). Monte um exemplo de contexto formatado que será enviado pro LLM.

## Dados Utilizados

| Arquivo | Formato | Para que serve no Ben? |
|---------|---------|---------------------|
| `perfil_investidor.json` | JSON | Fornecer a realidade financeira do usuário (renda, patrimônio atual, metas ativas e apetite a risco) para basear os cálculos de viabilidade. |
| `metas.csv` | CSV | [cite_start]Servir como o "motor de regras" do Ben, indicando prazos estimados e sugerindo métodos organizacionais, como a Regra 50-30-20 e a estratégia de Pague-se Primeiro[cite: 2]. |
| `transacoes.csv` | CSV | [cite_start]Mapear o fluxo de caixa real do usuário, permitindo que o Ben calcule o valor exato das entradas (ex: Salário de 5000.00) e saídas (ex: Aluguel de 1200.00)[cite: 1]. Isso ajuda a encontrar "espaço" no orçamento para as metas. |
| `produtos_financeiros.json` | JSON | Usar as taxas de rentabilidade reais (ex: 100% da Selic, 102% do CDI) apenas como parâmetros matemáticos para projetar cenários de juros compostos, sem fazer recomendações de compra. |
| `historico_atendimento.csv` | CSV | [cite_start]Dar continuidade estratégica ao planejamento, lembrando se o cliente já perguntou sobre CDB, Tesouro Selic ou acompanhou o progresso de suas metas financeiras[cite: 3]. |

---

## Adaptações nos Dados

> Você modificou ou expandiu os dados mockados? Descreva aqui.

Adicionamos o arquivo exclusivo `metas.csv` para dar ao Ben um repertório tático. [cite_start]Em vez de apenas dizer "economize", o Ben agora pode cruzar o objetivo do usuário com estratégias validadas, como sugerir a "Bola de Neve" para quem tem dívidas ou a "Regra 70-30" para independência financeira[cite: 2]. Os produtos financeiros são usados estritamente para simulação matemática de cenários.

---

## Estratégia de Integração

### Como os dados são carregados?
> Descreva como seu agente acessa a base de conhecimento.

Os dados são carregados dinamicamente via código no backend da aplicação em Streamlit, criando um DataFrame unificado para as transações e dicionários para o perfil e metas.

```python
import pandas as pd
import json

perfil = json.load(open('./data/perfil_investidor.json'))
produtos = json.load(open('./data/produtos_financeiros.json'))

# Bases em CSV com indexação para buscas rápidas
transacoes = pd.read_csv('./data/transacoes.csv')
historico = pd.read_csv('./data/historico_atendimento.csv')
metas = pd.read_csv('./data/metas.csv')
```

### Como os dados são usados no prompt?
> Os dados vão no system prompt? São consultados dinamicamente?

Os dados brutos são processados pelo backend Python e injetados no *System Prompt* na forma de um "Dossiê Financeiro". Isso economiza tokens e garante que o LLM foque no planejamento, recebendo os cálculos mastigados.

```text
DOSSIÊ FINANCEIRO DO CLIENTE (Base: perfil_investidor.json):
- Nome: João Silva
- Renda Mensal Declarada: R$ 5.000,00
- Meta Principal Ativa: Completar reserva de emergência (Faltam R$ 5.000,00 para bater R$ 15.000,00)
- Prazo Alvo: 2026-06

FLUXO DE CAIXA ATUAL (Base: transacoes.csv):
- [cite_start]Receitas Totais: R$ 5000.00 [cite: 1]
- [cite_start]Despesas Fixas (Moradia/Saúde): R$ 1468.00 [cite: 1]
- [cite_start]Despesas Variáveis (Alimentação/Transporte/Lazer): R$ 920.90 [cite: 1]
- Capacidade de Poupança Mapeada: R$ 2.611,10

ESTRATÉGIAS E MÉTODOS DISPONÍVEIS (Base: metas.csv):
- [cite_start]Para Reserva de Emergência: Sugerir a Regra 50-30-20 e estimar prazo de 06-12 meses[cite: 2].
- [cite_start]Estratégia de Aporte: Pague-se Primeiro[cite: 2].

PARÂMETROS PARA PROJEÇÃO MATEMÁTICA (Base: produtos_financeiros.json):
- Conservador/Reserva: Utilizar taxa de "100% da Selic" (Tesouro Selic) ou "102% do CDI" (CDB).

HISTÓRICO RECENTE (Base: historico_atendimento.csv):
- [cite_start]Cliente já acompanhou o progresso da reserva de emergência no dia 2025-10-12[cite: 3].
- [cite_start]Cliente atualizou dados cadastrais (e-mail e telefone) em 2025-10-25[cite: 3].
```

---

## Exemplo de Contexto Montado

> Mostre um exemplo de como os dados são formatados para o agente gerar a resposta.

Quando o usuário pergunta: *"Como organizo meu salário para terminar minha reserva até o meio de 2026?"*, o Ben recebe este bloco de contexto resumido para gerar o plano:

```
[CONTEXTO PARA O BEN]
O usuário João Silva tem renda de R$ 5.000 e precisa juntar mais R$ 5.000 até junho de 2026 (aprox. 8 meses). 
Sua capacidade de poupança atual é alta (sobra mais de R$ 2.500/mês).
[cite_start]Ação exigida: Sugira um plano mensal de aportes usando o método "Pague-se Primeiro" e a "Regra 50-30-20"[cite: 2].
Use uma rentabilidade simulada de 100% da Selic para mostrar que o esforço real de poupança será um pouco menor que R$ 625/mês devido aos juros. Não recomende corretoras.
```
