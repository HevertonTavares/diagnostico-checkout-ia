import streamlit as st
import os

st.set_page_config(page_title="🔐 Visualizador da Chave OPENAI_API_KEY")

st.title("🔐 Verificação da variável OPENAI_API_KEY")

# Obter a variável do ambiente
key = os.getenv("OPENAI_API_KEY")

if key:
    st.success("✅ Variável OPENAI_API_KEY foi carregada com sucesso.")
    st.write("🔍 Conteúdo da variável (repr):")
    st.code(repr(key), language="python")
    st.write("📏 Comprimento da chave:", len(key))
else:
    st.error("❌ A variável OPENAI_API_KEY **não está definida**.")
    st.info("Verifique o campo ⚙️ `Secrets` no Streamlit Cloud e clique em Reboot.")
