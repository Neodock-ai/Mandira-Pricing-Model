import streamlit as st

# --- Tiered Pricing Definitions ---
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

# --- Add-On Features ---
addons = {
    "Extra Channel (Basic only)": 5000,
    "Compliance Bundle (Basic only)": 15000,
    "Extra Connector": 15000,
    "Transcription ($1/hr)": 1.00,
    "Redaction ($0.01/min)": 0.01,
    "Analytics Module": 60000  # $5,000/month × 12
}

# --- Overage Rates ---
overage = {
    "record_per_1000": 2.50,
    "storage_per_gb_month": 0.03
}

# --- Streamlit UI Setup ---
st.set_page_config("Wilmac Pricing Calculator", layout="centered")
st.title("📊 Wilmac Pricing Calculator")

# Step 1 – Tier Selection
tier_choice = st.selectbox("Select Your Tier", list(tiers.keys()))
tier = tiers[tier_choice]
st.markdown(f"**Included Features**: {', '.join(tier['features'])}")
st.markdown(f"**Included Volume**: {tier['included_records']:,} records, {tier['included_storage_tb']} TB")

# Step 2 – Usage Input
st.subheader("📦 Estimated Usage")
records = st.number_input("Total Annual Records", min_value=0, value=10_000_000)
storage_tb = st.number_input("Average Storage (TB)", min_value=0.0, value=5.0, step=0.5)

# Step 3 – AI Services
st.subheader("🧠 AI Features")
transcription_hr = st.number_input("Transcription (hours)", value=0, min_value=0)
redaction_min = st.number_input("Redaction (minutes)", value=0, min_value=0)

# Step 4 – Optional Add-ons
st.subheader("🔧 Add-On Modules")
extra_connector = st.checkbox("Add Extra Connector", value=False)
analytics_module = st.checkbox("Add Analytics Module", value=False)
extra_channel = st.checkbox("Add Extra Channel (Basic only)", value=False if tier_choice == "Basic" else False, disabled=tier_choice != "Basic")
compliance_bundle = st.checkbox("Add Compliance Bundle (Basic only)", value=False if tier_choice == "Basic" else False, disabled=tier_choice != "Basic")

# --- Pricing Logic ---
base_price = tier["price"]
included_records = tier["included_records"]
included_storage_gb = tier["included_storage_tb"] * 1024

# Overages
record_overage_units = max(0, (records - included_records) / 1000)
storage_overage_gb = max(0, (storage_tb * 1024 - included_storage_gb))
record_overage_cost = record_overage_units * overage["record_per_1000"]
storage_overage_cost = storage_overage_gb * overage["storage_per_gb_month"] * 12  # Annual

# Usage charges
transcription_cost = transcription_hr * addons["Transcription ($1/hr)"]
redaction_cost = redaction_min * addons["Redaction ($0.01/min)"]

# Optional add-ons
addon_cost = 0
if extra_connector:
    addon_cost += addons["Extra Connector"]
if analytics_module:
    addon_cost += addons["Analytics Module"]
if extra_channel:
    addon_cost += addons["Extra Channel (Basic only)"]
if compliance_bundle:
    addon_cost += addons["Compliance Bundle (Basic only)"]

# Total
total_price = (
    base_price +
    record_overage_cost +
    storage_overage_cost +
    transcription_cost +
    redaction_cost +
    addon_cost
)

# --- Pricing Summary ---
st.markdown("---")
st.subheader("💰 Estimated Pricing Breakdown")
st.write(f"**Base Tier Price**: ${base_price:,.2f}")
if record_overage_cost > 0:
    st.write(f"**Record Overage**: ${record_overage_cost:,.2f}")
if storage_overage_cost > 0:
    st.write(f"**Storage Overage**: ${storage_overage_cost:,.2f}")
if transcription_cost > 0:
    st.write(f"**Transcription**: ${transcription_cost:,.2f}")
if redaction_cost > 0:
    st.write(f"**Redaction**: ${redaction_cost:,.2f}")
if extra_connector:
    st.write(f"**Extra Connector**: ${addons['Extra Connector']:,}")
if analytics_module:
    st.write(f"**Analytics Module**: ${addons['Analytics Module']:,}")
if extra_channel:
    st.write(f"**Extra Channel**: ${addons['Extra Channel (Basic only)']:,}")
if compliance_bundle:
    st.write(f"**Compliance Bundle**: ${addons['Compliance Bundle (Basic only)']:,}")

st.markdown(f"### ✅ **Total Estimated Price: ${total_price:,.2f}**")
st.caption("Built for Wilmac Case Competition – Powered by Streamlit 🚀")

