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

if st.button("Analyze"):
    try:
        language = client.detect_language(documents=[text])[0]
        st.success(language.primary_language.name)

        entities = client.recognize_entities(documents=[text])[0].entities
        for e in entities:
            st.write(e.text, "-", e.category)

        pii = client.recognize_pii_entities(documents=[text])[0]
        st.write("Redacted:", pii.redacted_text)

    except Exception as e:
        st.error(e)