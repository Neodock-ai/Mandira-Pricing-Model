import streamlit as st

# Tiers
tiers = {
    "Starter": 15000,
    "Basic": 30000,
    "Standard": 90000,
    "Enterprise": 180000
}

# Add-ons
addons = {
    "Transcription ($1/hr)": 1000,
    "Redaction ($0.50/hr)": 500,
    "Analytics Module": 10000,
    "Connector": 15000,
    "Financial Compliance": 9800,
    "Healthcare Compliance": 12500
}

st.set_page_config(page_title="Wilmac Pricing Checkout", layout="centered")
st.title("Wilmac Pricing Checkout")

# Step 1: Tier selection
st.subheader("1. Select a Tier Plan")
tier = st.radio("", list(tiers.keys()), horizontal=True)
base_price = tiers[tier]

# Step 2: Add-ons
st.subheader("2. Add-On Features")
selected_addons = []
for key in addons:
    if tier in ["Starter", "Basic"] or key not in ["Financial Compliance", "Healthcare Compliance", "Analytics Module"]:
        if st.checkbox(f"{key} (${addons[key]:,})"):
            selected_addons.append(key)

# Step 3: Summary
addon_cost = sum(addons[add] for add in selected_addons)
total_price = base_price + addon_cost

st.subheader("3. Pricing Summary")
st.write(f"Base Plan: ${base_price:,.2f}")
st.write(f"Add-ons: ${addon_cost:,.2f}")
st.markdown(f"### Total Estimated Price: **${total_price:,.2f}**")

