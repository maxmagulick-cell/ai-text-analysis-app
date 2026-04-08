import streamlit as st
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

# Force read from Streamlit secrets only
endpoint = st.secrets["FOUNDRY_ENDPOINT"]
key = st.secrets["FOUNDRY_KEY"]

# Create client
credential = AzureKeyCredential(key)
client = TextAnalyticsClient(endpoint=endpoint, credential=credential)

st.set_page_config(page_title="AI Text Analysis App", page_icon="🧠")

st.title("🧠 AI Text Analysis App")
st.write("Analyze text using Azure AI")

text = st.text_area("Enter text")

col1, col2 = st.columns(2)

with col1:
    analyze = st.button("Analyze")

with col2:
    clear = st.button("Clear")

if clear:
    st.rerun()

if analyze:
    try:
        with st.spinner("Analyzing text..."):

            # Language
            language = client.detect_language(documents=[text])[0]
            st.subheader("🌍 Language")
            st.success(language.primary_language.name)

            # Entities
            entities = client.recognize_entities(documents=[text])[0].entities
            st.subheader("🏷️ Entities")

            for e in entities:
                st.write(f"- {e.text} ({e.category})")

            # PII
            pii_result = client.recognize_pii_entities(documents=[text])[0]

            st.subheader("🔒 PII Detection")
            for e in pii_result.entities:
                st.write(f"- {e.text} ({e.category})")

            # Redacted text
            st.subheader("🧹 Redacted Text")
            st.text_area("Redacted Text", pii_result.redacted_text, height=120)

    except Exception as e:
        st.error(e)