import streamlit as st
import openai
import os

st.title("🔐 Teste da OPENAI_API_KEY")

# Exibir se a variável está presente
api_key = os.getenv("OPENAI_API_KEY")
if api_key:
    st.success("✅ OPENAI_API_KEY foi carregada com sucesso!")
    openai.api_key = api_key

    try:
        # Fazer uma chamada simples de teste
        resposta = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Diga 'API funcionando'."}],
            max_tokens=10
        )
        texto = resposta["choices"][0]["message"]["content"]
        st.code(texto)
    except Exception as e:
        st.error("❌ Erro ao chamar a API:")
        st.exception(e)
else:
    st.error("🚫 Variável OPENAI_API_KEY não foi carregada.")