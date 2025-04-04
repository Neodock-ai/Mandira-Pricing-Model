import streamlit as st

# Set Streamlit layout and style
st.set_page_config(page_title="Wilmac Pricing Calculator", layout="centered")

st.markdown("<h1 style='font-size:32px; font-weight:600;'>Wilmac Pricing Configurator</h1>", unsafe_allow_html=True)
st.markdown("Configure your estimated annual cost based on tier, usage, and add-ons.")

st.markdown("---")

# --- Tier Configuration ---
tiers = {
    "Basic": {
        "price": 30000,
        "included_records": 10_000_000,
        "included_storage_tb": 5,
        "features": ["Voice archiving", "Basic search", "Purge controls"]
    },
    "Standard": {
        "price": 90000,
        "included_records": 50_000_000,
        "included_storage_tb": 15,
        "features": ["Voice + 2 channels", "Compliance tools", "Standard support"]
    },
    "Enterprise": {
        "price": 180000,
        "included_records": 200_000_000,
        "included_storage_tb": 50,
        "features": ["All channels", "Compliance bundle", "1 Connector", "Priority support"]
    },
    "Enterprise Plus": {
        "price": 250000,
        "included_records": float("inf"),
        "included_storage_tb": float("inf"),
        "features": ["Everything in Enterprise", "Multiple connectors", "Custom SLA", "Analytics"]
    }
}

addons = {
    "Extra Channel (Basic only)": 5000,
    "Compliance Bundle (Basic only)": 15000,
    "Extra Connector": 15000,
    "Transcription ($1/hr)": 1.00,
    "Redaction ($0.01/min)": 0.01,
    "Analytics Module": 60000
}

overage = {
    "record_per_1000": 2.50,
    "storage_per_gb_per_month": 0.03
}

# --- SECTION: Tier Selection ---
st.markdown("### 1. Tier Selection")
col1, col2 = st.columns([1.3, 1.7])
with col1:
    tier_choice = st.radio("", list(tiers.keys()), horizontal=True)
tier = tiers[tier_choice]
st.write(f"**Price**: ${tier['price']:,} per year")
st.write(f"**Included**: {tier['included_records']:,} records, {tier['included_storage_tb']} TB storage")
st.write(f"**Features**: {', '.join(tier['features'])}")

st.markdown("---")

# --- SECTION: Usage Input ---
st.markdown("### 2. Usage Inputs")
col1, col2 = st.columns(2)
with col1:
    records = st.number_input("Annual Records", min_value=0, value=10_000_000, step=1_000_000)
with col2:
    storage_tb = st.number_input("Average Storage (TB)", min_value=0.0, value=5.0, step=0.5)

st.markdown("---")

# --- SECTION: AI Features ---
st.markdown("### 3. AI Services")
col1, col2 = st.columns(2)
with col1:
    transcription_hr = st.number_input("Transcription (hours)", min_value=0, value=0)
with col2:
    redaction_min = st.number_input("Redaction (minutes)", min_value=0, value=0)

st.markdown("---")

# --- SECTION: Add-ons ---
st.markdown("### 4. Add-On Options")
col1, col2 = st.columns(2)
with col1:
    add_connector = st.checkbox("Extra Connector", value=False)
    add_analytics = st.checkbox("Analytics Module", value=False)
with col2:
    add_channel = st.checkbox("Extra Channel (Basic only)", value=False if tier_choice == "Basic" else False, disabled=tier_choice != "Basic")
    add_compliance = st.checkbox("Compliance Bundle (Basic only)", value=False if tier_choice == "Basic" else False, disabled=tier_choice != "Basic")

st.markdown("---")

# --- SECTION: Cost Calculation ---
base_price = tier["price"]
included_records = tier["included_records"]
included_storage_gb = tier["included_storage_tb"] * 1024

# Overage calculations
record_overage_units = max(0, (records - included_records) / 1000)
storage_overage_gb = max(0, (storage_tb * 1024 - included_storage_gb))
record_overage_cost = record_overage_units * overage["record_per_1000"]
storage_overage_cost = storage_overage_gb * overage["storage_per_gb_per_month"] * 12

# Usage-based pricing
transcription_cost = transcription_hr * addons["Transcription ($1/hr)"]
redaction_cost = redaction_min * addons["Redaction ($0.01/min)"]

# Add-on selection
addon_cost = 0
if add_connector:
    addon_cost += addons["Extra Connector"]
if add_analytics:
    addon_cost += addons["Analytics Module"]
if add_channel:
    addon_cost += addons["Extra Channel (Basic only)"]
if add_compliance:
    addon_cost += addons["Compliance Bundle (Basic only)"]

# Final total
total_price = (
    base_price +
    record_overage_cost +
    storage_overage_cost +
    transcription_cost +
    redaction_cost +
    addon_cost
)

# --- SECTION: Summary Output ---
st.markdown("### 5. Pricing Summary")
st.markdown(f"<div style='font-size:24px; font-weight:bold;'>Estimated Annual Price: ${total_price:,.2f}</div>", unsafe_allow_html=True)

with st.expander("See detailed breakdown"):
    st.write(f"Base Tier: ${base_price:,.2f}")
    if record_overage_cost > 0:
        st.write(f"Record Overage: ${record_overage_cost:,.2f}")
    if storage_overage_cost > 0:
        st.write(f"Storage Overage: ${storage_overage_cost:,.2f}")
    if transcription_cost > 0:
        st.write(f"Transcription: ${transcription_cost:,.2f}")
    if redaction_cost > 0:
        st.write(f"Redaction: ${redaction_cost:,.2f}")
    if addon_cost > 0:
        st.write(f"Add-ons Total: ${addon_cost:,.2f}")

st.markdown("<hr>", unsafe_allow_html=True)
st.caption("This pricing model is designed for demo purposes for the Wilmac case competition.")
