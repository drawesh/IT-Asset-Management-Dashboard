import streamlit as st
import pandas as pd
from sqlalchemy.orm import Session
from datetime import date
import plotly.express as px

from database import SessionLocal
from models import Asset, AssetLog

st.set_page_config(page_title="IT Asset Management Dashboard", layout="wide")

def get_session():
    return SessionLocal()

# Fetch all assets
def load_assets():
    session = get_session()
    assets = session.query(Asset).all()
    session.close()
    return pd.DataFrame([{
        "ID": a.asset_id,
        "Name": a.asset_name,
        "Type": a.asset_type,
        "Status": a.status,
        "Purchase Date": a.purchase_date,
        "Warranty Expiry": a.warranty_expiry,
        "Assigned To": a.assigned_to,
        "Cost": float(a.cost)
    } for a in assets])

# Log asset action
def log_asset_action(asset_id, action, details):
    session = get_session()
    log = AssetLog(asset_id=int(asset_id), action=action, details=details)
    session.add(log)
    session.commit()
    session.close()

# Add new asset
def add_asset(name, type_, status, purchase, expiry, assigned, cost):
    session = get_session()
    asset = Asset(
        asset_name=name,
        asset_type=type_,
        status=status,
        purchase_date=purchase,
        warranty_expiry=expiry,
        assigned_to=assigned,
        cost=cost
    )
    session.add(asset)
    session.commit()
    asset_id = asset.asset_id
    session.close()
    log_asset_action(asset_id, "Added", f"Asset '{name}' added with type '{type_}' and status '{status}'")

# Update asset
def update_asset(asset_id, name, type_, status, purchase, expiry, assigned, cost):
    session = get_session()
    asset = session.query(Asset).filter(Asset.asset_id == int(asset_id)).first()
    if asset:
        asset.asset_name = name
        asset.asset_type = type_
        asset.status = status
        asset.purchase_date = purchase
        asset.warranty_expiry = expiry
        asset.assigned_to = assigned
        asset.cost = cost
        session.commit()
        log_asset_action(asset_id, "Updated", f"Asset '{name}' updated")
    session.close()

# Delete asset
def delete_asset(asset_id):
    session = get_session()
    asset = session.query(Asset).filter(Asset.asset_id == int(asset_id)).first()
    if asset:
        name = asset.asset_name
        session.delete(asset)
        session.commit()
        log_asset_action(asset_id, "Deleted", f"Asset '{name}' deleted")
    session.close()

# Fetch logs
def load_logs():
    session = get_session()
    logs = session.query(AssetLog).order_by(AssetLog.timestamp.desc()).all()
    session.close()
    return pd.DataFrame([{
        "Log ID": l.log_id,
        "Asset ID": l.asset_id,
        "Action": l.action,
        "Details": l.details,
        "Timestamp": l.timestamp
    } for l in logs])

st.title("💼 IT Asset Management Dashboard")

# Load table early for sidebar use
df = load_assets()

st.sidebar.header("Add New Asset")
name = st.sidebar.text_input("Asset Name")
type_ = st.sidebar.selectbox("Asset Type", ["Laptop", "Monitor", "Mobile Device", "Software", "Other"])
status = st.sidebar.selectbox("Status", ["In Use", "Available", "Under Repair", "Retired"])
purchase = st.sidebar.date_input("Purchase Date")
expiry = st.sidebar.date_input("Warranty Expiry")
assigned = st.sidebar.text_input("Assigned To (optional)")
cost = st.sidebar.number_input("Cost", min_value=0.0)

if st.sidebar.button("Add Asset"):
    add_asset(name, type_, status, purchase, expiry, assigned, cost)
    st.success("Asset added successfully!")

st.sidebar.header("Edit/Delete Asset")
if not df.empty:
    asset_options = df["Name"].tolist()
    selected_asset = st.sidebar.selectbox("Select Asset to Edit/Delete", asset_options)
    asset_row = df[df["Name"] == selected_asset].iloc[0]
    asset_id = asset_row["ID"]

    edit_name = st.sidebar.text_input("Edit Name", value=asset_row["Name"])
    edit_type = st.sidebar.selectbox("Edit Type", ["Laptop", "Monitor", "Mobile Device", "Software", "Other"], index=["Laptop", "Monitor", "Mobile Device", "Software", "Other"].index(asset_row["Type"]))
    edit_status = st.sidebar.selectbox("Edit Status", ["In Use", "Available", "Under Repair", "Retired"], index=["In Use", "Available", "Under Repair", "Retired"].index(asset_row["Status"]))
    edit_purchase = st.sidebar.date_input("Edit Purchase Date", value=asset_row["Purchase Date"])
    edit_expiry = st.sidebar.date_input("Edit Warranty Expiry", value=asset_row["Warranty Expiry"])
    edit_assigned = st.sidebar.text_input("Edit Assigned To", value=asset_row["Assigned To"])
    edit_cost = st.sidebar.number_input("Edit Cost", value=float(asset_row["Cost"]), min_value=0.0)

    if st.sidebar.button("Update Asset"):
        update_asset(asset_id, edit_name, edit_type, edit_status, edit_purchase, edit_expiry, edit_assigned, edit_cost)
        st.success("Asset updated successfully!")

    if st.sidebar.button("Delete Asset"):
        delete_asset(asset_id)
        st.success("Asset deleted successfully!")

st.subheader("📋 Asset Inventory")
st.dataframe(df, width='stretch')

# Dashboard Charts
st.subheader("📊 Asset Analytics")

if not df.empty:
    col1, col2 = st.columns(2)

    with col1:
        fig1 = px.pie(df, names="Status", title="Asset Status Distribution")
        st.plotly_chart(fig1)

    with col2:
        fig2 = px.bar(df, x="Type", title="Assets by Type")
        st.plotly_chart(fig2)

    # Expired Warranty Alerts
    st.subheader("⚠ Warranty Expiry Alerts")

    today = date.today()
    df["Warranty Expiry"] = pd.to_datetime(df["Warranty Expiry"])
    df["Warranty Expired"] = df["Warranty Expiry"].dt.date < today

    expired = df[df["Warranty Expired"] == True]
    st.warning(f"Expired Warranties: {len(expired)}")
    st.dataframe(expired, width='stretch')

else:
    st.info("No assets found. Add some from the sidebar.")

# Asset Logs
st.subheader("📝 Asset Activity Logs")
logs_df = load_logs()
st.dataframe(logs_df, width='stretch')
