import json
import pandas as pd
import requests
import streamlit as st
import numpy_financial as npf

# ============ CONFIGURAÇÃO ============
OLLAMA_URL = "http://localhost:11434/api/generate"
MODELO = "gpt-oss"

# ============ CARREGAR DADOS ============
perfil = json.load(open('./data/perfil_investidor.json'))
transacoes = pd.read_csv('./data/transacoes.csv')
historico = pd.read_csv('./data/historico_atendimento.csv')
produtos = json.load(open('./data/produtos_financeiros.json'))
metas = pd.read_csv('./data/metas.csv')

# ============ CÁLCULOS FINANCEIROS ============
# Somando o fluxo de caixa para evitar alucinações do LLM
receitas = transacoes[transacoes['tipo'] == 'entrada']['valor'].sum()
despesas = transacoes[transacoes['tipo'] == 'saida']['valor'].sum()
saldo_livre = receitas - despesas

# Calculando uma simulação de meta padrão (ex: completar a reserva em 12 meses)
valor_faltante = perfil['metas'][0]['valor_necessario'] - perfil['reserva_emergencia_atual']
taxa_mensal = 0.008 # 0.8% ao mês
meses = 12
aporte_necessario = npf.pmt(rate=taxa_mensal, nper=meses, pv=0, fv=-valor_faltante)

# ============ MONTAR CONTEXTO ============
contexto = f"""
DOSSIÊ DO CLIENTE:
- Nome: {perfil['nome']}, {perfil['idade']} anos
- Meta Principal: {perfil['objetivo_principal']} (Faltam R$ {valor_faltante:.2f})

FLUXO DE CAIXA:
- Receitas: R$ {receitas:.2f}
- Despesas: R$ {despesas:.2f}
- Saldo Livre Atual: R$ {saldo_livre:.2f}

CÁLCULO DO SISTEMA (Viabilidade):
- Para atingir a meta em {meses} meses a 0.8% a.m., o aporte exato é de R$ {aporte_necessario:.2f}/mês.

MÉTODOS E ESTRATÉGIAS DISPONÍVEIS:
{metas.to_string(index=False)}

ATENDIMENTOS ANTERIORES:
{historico.to_string(index=False)}
"""

# ============ SYSTEM PROMPT ============
SYSTEM_PROMPT = """Você é o Ben, um planejador financeiro estratégico e motivador.

OBJETIVO:
Transformar os desejos financeiros do usuário em metas concretas, estruturando planos de ação, calculando prazos e sugerindo ajustes no orçamento.

REGRAS:
- NUNCA recomende a compra ou venda de ativos específicos;
- Baseie suas simulações nos dados calculados no Dossiê do Cliente;
- Sugira ativamente os métodos da base de dados, como a Regra 50-30-20 ou a estratégia Pague-se Primeiro;
- Comunique-se de forma objetiva, trazendo clareza através da matemática, mas mantendo um tom encorajador;
- JAMAIS responda a perguntas fora do escopo de planejamento de metas financeiras;
- Sempre valide com o usuário se o plano sugerido cabe no orçamento;
- Responda de forma lógica: O objetivo, o esforço mensal e o método sugerido.
"""

# ============ CHAMAR OLLAMA ============
def perguntar(msg):
    prompt = f"""
    {SYSTEM_PROMPT}

    {contexto}

    Pergunta: {msg}"""

    r = requests.post(OLLAMA_URL, json={"model": MODELO, "prompt": prompt, "stream": False})
    return r.json()['response']

# ============ INTERFACE ============
st.set_page_config(page_title="Ben - Planejador Financeiro", page_icon="📉")
st.title("📉 Ben, o Planejador Financeiro")

if pergunta := st.chat_input("Ex: Como organizo meu salário para bater minha meta?"):
    st.chat_message("user").write(pergunta)
    with st.spinner("Analisando fluxo de caixa..."):
        st.chat_message("assistant").write(perguntar(pergunta))
