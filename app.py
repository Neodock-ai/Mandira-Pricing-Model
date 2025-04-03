import streamlit as st

# --- Tier Definitions (Table 3) ---
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

# --- Add-Ons and Overage Pricing (Table 4) ---
addons = {
    "Extra Channel (Basic only)": 5000,
    "Compliance Bundle (Basic only)": 15000,
    "Extra Connector": 15000,
    "Transcription ($1/hr)": 1.00,
    "Redaction ($0.01/min)": 0.01,
    "Analytics Module": 5000 * 12  # $5,000/month × 12
}

overage = {
    "record_per_1000": 2.50,
    "storage_per_gb_per_month": 0.03
}

# --- Streamlit App UI ---
st.set_page_config(page_title="Wilmac Pricing Calculator", layout="centered")
st.title("📊 Wilmac Continuity Replay – Pricing Calculator")

# Tier Selection
tier_choice = st.selectbox("Select a Pricing Tier", list(tiers.keys()))
tier = tiers[tier_choice]
st.markdown(f"**Included Features**: {', '.join(tier['features'])}")
st.markdown(f"**Included Volume**: {tier['included_records']:,} records, {tier['included_storage_tb']} TB storage")

# Record & Storage Input
st.subheader("📦 Usage Inputs")
records = st.number_input("Total Records (annual)", min_value=0, value=10_000_000)
storage_tb = st.number_input("Average Storage (TB)", min_value=0.0, value=5.0, step=0.1)

# Usage-Based Services
st.subheader("🧠 AI Usage-Based Tools")
transcription_hr = st.number_input("Transcription (hours)", min_value=0, value=0)
redaction_min = st.number_input("Redaction (minutes)", min_value=0, value=0)

# Optional Add-ons
st.subheader("🔧 Optional Add-Ons")
add_connector = st.checkbox("Add Extra Connector", value=False)
add_analytics = st.checkbox("Add Analytics Module", value=False)
add_channel = st.checkbox("Add Extra Channel (Basic only)", value=False if tier_choice == "Basic" else False, disabled=tier_choice != "Basic")
add_compliance = st.checkbox("Add Compliance Bundle (Basic only)", value=False if tier_choice == "Basic" else False, disabled=tier_choice != "Basic")

# --- Cost Calculations ---
base_price = tier["price"]
included_records = tier["included_records"]
included_storage_gb = tier["included_storage_tb"] * 1024

# Overage
record_overage = max(0, (records - included_records) / 1000)
storage_overage_gb = max(0, (storage_tb * 1024 - included_storage_gb))
record_overage_cost = record_overage * overage["record_per_1000"]
storage_overage_cost = storage_overage_gb * overage["storage_per_gb_per_month"] * 12  # annualized

# Usage-Based Cost
transcription_cost = transcription_hr * addons["Transcription ($1/hr)"]
redaction_cost = redaction_min * addons["Redaction ($0.01/min)"]

# Add-On Costs
connector_cost = addons["Extra Connector"] if add_connector else 0
analytics_cost = addons["Analytics Module"] if add_analytics else 0
channel_cost = addons["Extra Channel (Basic only)"] if add_channel else 0
compliance_cost = addons["Compliance Bundle (Basic only)"] if add_compliance else 0

# Total
total_cost = sum([
    base_price,
    record_overage_cost,
    storage_overage_cost,
    transcription_cost,
    redaction_cost,
    connector_cost,
    analytics_cost,
    channel_cost,
    compliance_cost
])

# --- Output Summary ---
st.markdown("---")
st.subheader("💵 Estimated Pricing Summary")
st.write(f"**Base Tier Price**: ${base_price:,.2f}")
if record_overage_cost > 0:
    st.write(f"**Record Overage**: ${record_overage_cost:,.2f}")
if storage_overage_cost > 0:
    st.write(f"**Storage Overage**: ${storage_overage_cost:,.2f}")
if transcription_cost > 0:
    st.write(f"**Transcription**: ${transcription_cost:,.2f}")
if redaction_cost > 0:
    st.write(f"**Redaction**: ${redaction_cost:,.2f}")
if connector_cost > 0:
    st.write(f"**Extra Connector**: ${connector_cost:,.2f}")
if analytics_cost > 0:
    st.write(f"**Analytics Module**: ${analytics_cost:,.2f}")
if channel_cost > 0:
    st.write(f"**Extra Channel (Basic)**: ${channel_cost:,.2f}")
if compliance_cost > 0:
    st.write(f"**Compliance Bundle (Basic)**: ${compliance_cost:,.2f}")

st.markdown(f"### ✅ **Total Estimated Price: ${total_cost:,.2f}**")

st.caption("Built for Wilmac by your case competition team – powered by Streamlit 🚀")
