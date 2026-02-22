import streamlit as st
from agents.orchestrator import run_pipeline
from exports.pdf_generator import generate_pdf
from reportlab.lib import colors
import os
import requests
import uuid


def convert_currency(amount, from_currency="USD", to_currency="GBP"):
    try:
        url = "https://api.exchangerate.host/convert"
        params = {
            "from": from_currency,
            "to": to_currency,
            "amount": amount
        }
        response = requests.get(url, params=params, timeout=5)
        data = response.json()

        if "result" in data and data["result"] is not None:
            return data["result"]
        else:
            return amount  
    except Exception:
        return amount  



st.set_page_config(page_title="Project Scoping Assistant", layout="wide")

st.title("🚀 AI Multi-Agent Startup Scoping System")


st.sidebar.header("Branding & Financial Settings")

company_name = st.sidebar.text_input(
    "Company Name",
    value="Project Scoping Assistant"
)

country = st.sidebar.selectbox(
    "Development Country",
    ["US", "UK", "Germany", "India", "Canada", "Australia", "UAE"]
)

currency = st.sidebar.selectbox(
    "Display Currency",
    ["USD", "GBP", "EUR", "INR", "AUD", "CAD"]
)

logo_file = st.sidebar.file_uploader(
    "Upload Company Logo (PNG or JPG)",
    type=["png", "jpg", "jpeg"]
)

primary_color_hex = st.sidebar.color_picker(
    "Primary Accent Color",
    "#1F4E79"
)


logo_path = None
if logo_file:
    os.makedirs("temp_uploads", exist_ok=True)

    logo_path = None

    if logo_file:
        os.makedirs("temp_uploads", exist_ok=True)

        file_extension = logo_file.name.split(".")[-1]
        unique_name = f"{uuid.uuid4()}.{file_extension}"

        logo_path = os.path.join("temp_uploads", unique_name)

        with open(logo_path, "wb") as f:
            f.write(logo_file.getbuffer())


idea = st.text_area("Describe your startup idea")


if st.button("Generate Full Plan"):

    if not idea.strip():
        st.warning("Please enter a startup idea.")
        st.stop()

    with st.spinner("Running multi-agent pipeline..."):
        result = run_pipeline(idea, country=country)

    if "error" in result:
        st.error(result["error"])
        st.stop()

    analysis = result["analysis"]
    report = result["investor_report"]

    
    cost_data = analysis["estimated_cost"]

    low_usd = cost_data["low_usd"]
    high_usd = cost_data["high_usd"]

    if currency != "USD":
        low_local = convert_currency(low_usd, "USD", currency)
        high_local = convert_currency(high_usd, "USD", currency)
    else:
        low_local = low_usd
        high_local = high_usd

    
    analysis["estimated_cost"]["display_currency"] = currency
    analysis["estimated_cost"]["display_low"] = int(low_local)
    analysis["estimated_cost"]["display_high"] = int(high_local)

 
    st.subheader("📦 MVP Scope")
    st.json(analysis["mvp"])

    st.subheader("🛠 Tech Stack")
    st.json(analysis["tech_stack"])

    st.subheader("⚠ Risks")
    st.json(analysis["risks"])

    st.subheader("📊 Summary")
    st.write("Complexity:", analysis["complexity"])
    st.write("Timeline:", analysis["timeline"])
    st.write(
        f"Estimated Cost: {currency} {int(low_local):,} - {currency} {int(high_local):,}"
    )

    st.subheader("📄 Investor Summary")
    st.write(report["executive_summary"])

    st.metric(
        "Investor Readiness Score",
        f"{report['investor_readiness_score']}/10"
    )

    
    pdf_filename = "startup_project_report.pdf"

    generate_pdf(
        result,
        filename=pdf_filename,
        logo_path=logo_path,
        company_name=company_name,
        primary_color=colors.HexColor(primary_color_hex)
    )

    with open(pdf_filename, "rb") as f:
        st.download_button(
            label="📥 Download Investor PDF",
            data=f,
            file_name=pdf_filename,
            mime="application/pdf"
        )