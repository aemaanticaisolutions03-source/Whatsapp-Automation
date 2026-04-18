import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="WhatsApp Campaign", layout="centered")

st.title("📲 WhatsApp Campaign Dashboard")

# Upload file
uploaded_file = st.file_uploader("Upload Contacts File (CSV or Excel)", type=["csv", "xlsx"])

message = st.text_area("Enter Message")

image_url = st.text_input("Enter Image URL (optional)")

if uploaded_file is not None:

    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file, dtype=str, encoding='latin1')
    else:
        df = pd.read_excel(uploaded_file, dtype=str)

    # ✅ Fix phone
    df["Phone"] = df["Phone"].str.replace(",", "").str.strip()
    df["Phone"] = "whatsapp:+91" + df["Phone"]

    st.write("Preview of Data:")
    st.dataframe(df)

    if st.button("🚀 Send Campaign"):

        webhook_url = "https://n8n-railway-production-1ee8.up.railway.app/webhook/send-campaign"

        data = {
            "contacts": df.to_dict(orient="records"),
            "message": message,
            "image_url": image_url
        }

        response = requests.post(webhook_url, json=data)

        if response.status_code == 200:
            st.success("✅ Campaign Triggered Successfully!")
        else:
            st.error(f"❌ Error: {response.status_code} - {response.text}")
