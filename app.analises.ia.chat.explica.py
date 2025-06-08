
import streamlit as st
import requests
import pandas as pd
import os
import json
from datetime import datetime
st.write("🔍 OPENAI_API_KEY:", repr(os.getenv("OPENAI_API_KEY")))
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


st.markdown("Digite a URL do site (pode ser com ou sem 'view-source:') e clique em Analisar para ver os resultados abaixo.")
url = st.text_input("🔗 Cole aqui o link do código-fonte do site")
analisar = st.button("🚀 Analisar")

historico_path = "historico_analises_appmax.json"
if not os.path.exists(historico_path):
    with open(historico_path, "w") as f:
        json.dump([], f)

def analisar_checkout(url):
    try:
        if url.startswith('view-source:'):
            url = url.replace('view-source:', '')

        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        html = response.text.lower()

        checkouts = {
            'Appmax': ['window.appmax', 'data-appmax', 'appmax.checkout'],
            'Yampi': ['yampi.checkout', 'data-store', 'yampi-token'],
            'Cartpanda': ['panda-checkout', 'cartpanda.checkout', 'window.cartpanda'],
            'Nuvemshop': ['window.__nuvem__', 'nuvem-checkout', 'nuvemshop.cart'],
            'Shopify': ['shopify.checkout', 'shopify-features', 'cdn.shopify.com'],
            'Kiwify': ['kiwify.checkout', 'window.kiwify', 'data-kiwify'],
            'Hotmart': ['hotmart.marketplace', 'window.hotmart', 'data-hotmart'],
        }

        gateways = {
            'Appmax Gateway': ['gateway.appmax.com.br', 'appmax.gateway'],
            'Pagar.me': ['api.pagar.me', 'pagarme.js'],
            'Mercado Pago': ['mercadopago.js', 'secure.mlstatic.com'],
            'PagSeguro': ['pagseguro.uol.com.br', 'pagseguro.directpayment'],
            'Yampi Gateway': ['yampi.gateway'],
            'Stripe': ['checkout.stripe.com', 'js.stripe.com'],
        }

        formas_pagamento = {
            'Pix': ['pix', 'pagamento via pix'],
            'Cartão': ['cartao', 'cartão', 'visa', 'mastercard', 'credito'],
            'Boleto': ['boleto', 'boleto bancário']
        }

        resultado = {
            'Checkout Detectado': [],
            'Gateways Detectados': [],
            'Formas de Pagamento': [],
            'Possível Associação': {}
        }

        for nome, sinais in checkouts.items():
            if any(p in html for p in sinais):
                resultado['Checkout Detectado'].append(nome)

        for nome, sinais in gateways.items():
            if any(p in html for p in sinais):
                resultado['Gateways Detectados'].append(nome)

        for metodo, sinais in formas_pagamento.items():
            if any(p in html for p in sinais):
                resultado['Formas de Pagamento'].append(metodo)

        for metodo in resultado['Formas de Pagamento']:
            associado = None
            for gateway, sinais in gateways.items():
                for s in sinais:
                    if metodo.lower() in s or (s in html and metodo.lower() in html):
                        associado = gateway
                        break
                if associado:
                    break
            resultado['Possível Associação'][metodo] = associado if associado else 'Não identificado'

        return resultado

    except Exception as e:
        return {'Erro': str(e)}

if analisar and url:
    resultado = analisar_checkout(url)

    if "Erro" in resultado:
        st.error(f"❌ Erro ao processar: {resultado['Erro']}")
    else:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 🧾 Checkout Detectado")
            st.success(", ".join(resultado['Checkout Detectado']) if resultado['Checkout Detectado'] else "Não identificado")

        with col2:
            st.markdown("### 🛠️ Gateways Detectados")
            st.info(", ".join(resultado['Gateways Detectados']) if resultado['Gateways Detectados'] else "Não identificado")

        st.markdown("---")
        st.markdown("### 💳 Formas de Pagamento Detectadas")
        for forma in resultado['Formas de Pagamento']:
            gateway_associado = resultado['Possível Associação'].get(forma, "Não identificado")
            st.write(f"**{forma}** ➝ Gateway: `{gateway_associado}`")
        html = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}).text.lower()

        st.markdown("## 📌 Diagnóstico do Site Analisado")
        st.markdown(f"- 🔗 **URL** : [{url}]({url})")
        st.markdown(f"- ✅ **Checkout Detectado** : {'Sim' if resultado['Checkout Detectado'] else 'Não'}")
        st.markdown(f"- 🧠 **Appmax Detectado** : {'Sim' if 'Appmax' in resultado['Checkout Detectado'] else 'Não'}")

        plataforma = 'Não identificado'
        for nome in ['cartpanda', 'yampi', 'nuvemshop', 'shopify', 'kiwify', 'hotmart', 'bandeja']:
            if nome in url.lower():
                plataforma = nome
                break
        st.markdown(f"- 🛠 **Plataforma** : {plataforma}")

        antifraudes = ['clearsale', 'konduto', 'fraudmarc']
        antifraude_detectado = 'Não identificado'
        for termo in antifraudes:
            if termo in html:
                antifraude_detectado = termo
                break
        st.markdown(f"- 🛡 **Antifraude** : {antifraude_detectado}")
        st.markdown(f"- 📅 **Dados da Análise** : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


        with open(historico_path, "r") as f:
            historico = json.load(f)

        for forma in resultado['Formas de Pagamento']:
            historico.append({
                "Data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "URL": url,
                "Checkout": ", ".join(resultado['Checkout Detectado']),
                "Forma de Pagamento": forma,
                "Gateway Associado": resultado['Possível Associação'].get(forma, "Não identificado")
            })

        with open(historico_path, "w") as f:
            json.dump(historico, f, indent=2)

        st.markdown("## 📚 Histórico de Análises")
        with open(historico_path, "r") as f:
            historico = json.load(f)

        if historico:
            df = pd.DataFrame(historico)
            st.dataframe(df)

            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("⬇️ Exportar histórico em CSV", csv, "historico_analises.csv", "text/csv")
        else:
            st.info("Nenhuma análise realizada ainda.")
        st.markdown("---")
        st.markdown("### 🧮 Resultado bruto (JSON)")
        st.json(resultado)

        st.markdown("---")
        st.markdown("💬 **Converse com a IA sobre este site**")
        pergunta = st.text_input("Digite sua pergunta sobre o diagnóstico acima:")

        if pergunta:
            with st.spinner("Consultando a IA..."):
                contexto = f"Diagnóstico do site:\nCheckout: {', '.join(resultado['Checkout Detectado'])}\n" \
                           f"Gateways: {', '.join(resultado['Gateways Detectados'])}\n" \
                           f"Formas de Pagamento: {', '.join(resultado['Formas de Pagamento'])}\n" \
                           f"Associação: {resultado['Possível Associação']}\n" \
                           f"Scripts de análise: {', '.join(resultado.get('Scripts de Análise', []))}"
                contexto = f"Diagnóstico do site:\nCheckout: {', '.join(resultado['Checkout Detectado'])}\n" \
                           f"Gateways: {', '.join(resultado['Gateways Detectados'])}\n" \
                           f"Formas de Pagamento: {', '.join(resultado['Formas de Pagamento'])}\n" \
                           f"Associação: {resultado['Possível Associação']}\n" \
                           f"Scripts de análise: {', '.join(resultado.get('Scripts de Análise', []))}"
                prompt = f"Contexto:\n{contexto}\n\nPergunta: {pergunta}\n\nSe alguma informação não for detectada, explique por que isso pode ter ocorrido (ex: carregamento por JavaScript, obfuscação ou ausência no código-fonte)."

                try:
                    resposta = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=[{"role": "user", "content": prompt}],
                        temperature=0.5,
                        max_tokens=500
                    )
                    st.success(resposta.choices[0].message.content.strip())
                except Exception as e:
                    st.error(f"Erro ao consultar a IA: {e}")


