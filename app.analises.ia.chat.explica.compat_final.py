import streamlit as st
import requests
import pandas as pd
import os
from datetime import datetime
from openai import OpenAI

st.set_page_config(page_title="Diagnóstico site do parceiro Appmax", layout="centered")

st.title("📋 Diagnóstico site do parceiro Appmax")
st.markdown("🧠 Esta análise utiliza inteligência da OpenAI para maior assertividade.")

with st.expander("ℹ️ Como usar esta ferramenta", expanded=False):
    st.markdown("""
Esta aplicação permite diagnosticar elementos de checkout em sites de e-commerce.  
Você pode:

- Inserir uma URL com `view-source:` para escanear  
- Verifique se há **checkouts** detectados  
- Detectar **gateways de pagamento** e **meios de pagamento**  
- Ver quais meios estão associados a cada gateway  
- Exportar os dados em **CSV**  
- Filtrar análises por domínio  

👉 Após inserir a URL, clique no botão 🚀 **Analisar** abaixo.
    """)

url = st.text_input("🔗 Cole aqui o link do código-fonte do site (com ou sem 'view-source:')")

def analisar_checkout(url):
    try:
        if url.startswith('view-source:'):
            url = url.replace('view-source:', '')
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        html = response.text.lower()

        checkouts = {'Appmax': ['window.appmax', 'data-appmax', 'appmax.checkout']}
        gateways = {'PagSeguro': ['pagseguro', 'pagseguro.uol']}
        formas_pagamento = {'Pix': ['pix'], 'Cartão': ['visa', 'mastercard'], 'Boleto': ['boleto']}

        resultado = {
            'Checkout Detectado': [],
            'Gateways Detectados': [],
            'Formas de Pagamento': [],
            'Possível Associação': {}
        }

        for nome, sinais in checkouts.items():
            if any(s in html for s in sinais):
                resultado['Checkout Detectado'].append(nome)

        for nome, sinais in gateways.items():
            if any(s in html for s in sinais):
                resultado['Gateways Detectados'].append(nome)

        for nome, sinais in formas_pagamento.items():
            if any(s in html for s in sinais):
                resultado['Formas de Pagamento'].append(nome)

        for forma in resultado['Formas de Pagamento']:
            resultado['Possível Associação'][forma] = 'PagSeguro' if 'pagseguro' in html else 'Não identificado'

        return resultado
    except Exception as e:
        return {"erro": str(e)}

if url:
    resultado = analisar_checkout(url)
    if "erro" in resultado:
        st.error("❌ Erro ao analisar o checkout:")
        st.code(resultado["erro"])
    else:
        st.success("✅ Diagnóstico realizado com sucesso!")
        st.json(resultado)

        st.markdown("💬 **Pergunte algo sobre o diagnóstico acima:**")
        pergunta = st.text_input("Ex: Por que não foi detectado Appmax?")

        if pergunta:
            try:
                client = OpenAI()

                contexto = f"Diagnóstico do site:\nCheckout: {resultado['Checkout Detectado']}\n" \
                           f"Gateways: {resultado['Gateways Detectados']}\n" \
                           f"Formas de Pagamento: {resultado['Formas de Pagamento']}\n" \
                           f"Associação: {resultado['Possível Associação']}"
                prompt = f"Contexto:\n{contexto}\n\nPergunta: {pergunta}\n\nSe alguma informação não for detectada, explique por que isso pode ter ocorrido."

                resposta = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}]
                )

                st.success("🧠 Resposta da IA:")
                st.write(resposta.choices[0].message.content.strip())

            except Exception as e:
                st.error("❌ Erro ao consultar a OpenAI:")
                st.code(str(e))