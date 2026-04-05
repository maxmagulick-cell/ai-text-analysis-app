import streamlit as st
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

# Get credentials from Streamlit secrets
endpoint = st.secrets["FOUNDRY_ENDPOINT"]
key = st.secrets["FOUNDRY_KEY"]

# Debug (you can remove later)
st.write("Endpoint:", endpoint)
st.write("Key exists:", key is not None)
st.write("Key length:", len(key))

# Create client
credential = AzureKeyCredential(key)
client = TextAnalyticsClient(endpoint=endpoint, credential=credential)
# ---------------- UI ---------------- #

st.set_page_config(page_title="AI Text Analysis App", page_icon="🧠")

st.title("🧠 AI Text Analysis App")
st.write("Analyze text using Azure AI (Language, Entities, PII Detection)")

# Input box
text = st.text_area("Enter text to analyze:")

if st.button("Analyze"):
    if text.strip() == "":
        st.warning("Please enter some text.")
    else:
        try:
            # -------- Language Detection -------- #
            language = client.detect_language(documents=[text])[0]
            st.subheader("🌍 Language")
            st.success(language.primary_language.name)

            # -------- Entities -------- #
            entities = client.recognize_entities(documents=[text])[0].entities
            st.subheader("🏷️ Entities")
            if len(entities) > 0:
                for entity in entities:
                    st.write(f"- {entity.text} ({entity.category})")
            else:
                st.write("No entities found.")

            # -------- PII Detection -------- #
            pii_result = client.recognize_pii_entities(documents=[text])[0]
            pii_entities = pii_result.entities

            st.subheader("🔒 PII Detection")
            if len(pii_entities) > 0:
                for entity in pii_entities:
                    st.write(f"- {entity.text} ({entity.category})")
            else:
                st.write("No PII detected.")

            # -------- Redacted Text -------- #
            st.subheader("🧹 Redacted Text")
            st.code(pii_result.redacted_text)

        except Exception as e:
            st.error(f"Error: {e}")