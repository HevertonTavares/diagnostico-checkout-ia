# App de Diagnóstico de Checkout para E-commerce

Este aplicativo analisa o código-fonte de sites de e-commerce e retorna:

✅ Checkout detectado  
✅ Gateways de pagamento  
✅ Formas de pagamento disponíveis  
✅ Associação entre formas e gateways  
✅ Scripts de análise instalados (Google Analytics, Tag Manager, Hotjar, Clarity)  
✅ Histórico completo exportável  
✅ Validação tripla dos dados com inteligência da OpenAI para máxima confiabilidade

---

## 🚀 Como rodar localmente

1. Instale as dependências:
```bash
pip install -r requirements.txt
```

2. Defina sua chave da OpenAI:
```bash
export OPENAI_API_KEY="sk-sua-chave-aqui"
```

Ou crie um arquivo `.env` com:
```
OPENAI_API_KEY=sk-sua-chave-aqui
```

3. Rode o app:
```bash
streamlit run app.analises.ia.py
```

---

## 📦 Arquivos importantes

- `app.analises.ia.py`: código principal do app
- `requirements.txt`: dependências
- `.env.example`: exemplo de variável de ambiente
- `README.md`: este guia

---

Criado com 💙 para automatizar o diagnóstico técnico de parceiros e e-commerces.