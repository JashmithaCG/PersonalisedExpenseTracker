import streamlit as st
import pandas as pd
import altair as alt
import os
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --------------- CONFIGURATION ---------------
EMAIL_ADDRESS = ""  # Receiver email
EMAIL_SENDER = ""  # Your Gmail address
EMAIL_PASSWORD = ""  # App-specific password
DATA_FILE = "expenses.csv"
SETTINGS_FILE = "settings.csv"

# --------------- STREAMLIT PAGE SETTINGS ---------------
st.set_page_config(page_title="Expense Tracker", layout="centered")
st.markdown("""<style>
    .stApp {
        background: linear-gradient(to right, #f7f1e3, #fad0c4);
        font-family: 'Segoe UI', sans-serif;
    }
    .css-18e3th9 {
        padding: 2rem;
        border-radius: 20px;
        background-color: #ffffffcc;
        box-shadow: 0px 0px 10px #ccc;
    }
</style>""", unsafe_allow_html=True)

st.markdown("""<h1 style='text-align: center;'>📒 Expense Tracker</h1>""", unsafe_allow_html=True)

# --------------- FUNCTIONS ---------------
def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE, parse_dates=["Date"])
    else:
        return pd.DataFrame(columns=["Date", "Category", "Amount", "Description"])

def save_data(data):
    data.to_csv(DATA_FILE, index=False)

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        df = pd.read_csv(SETTINGS_FILE)
        return float(df.loc[0, "Budget"])
    else:
        return 0.0

def save_settings(budget):
    pd.DataFrame({"Budget": [budget]}).to_csv(SETTINGS_FILE, index=False)

def send_email_alert(total):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_SENDER
    msg['To'] = EMAIL_ADDRESS
    msg['Subject'] = "🚨 Monthly Budget Limit Exceeded!"

    body = f"You have exceeded your monthly budget. Your total spending this month is ₹{total:.2f}."
    msg.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(msg)

# --------------- LOAD DATA ---------------
data = load_data()
budget_limit = load_settings()
if not data.empty:
    data["Date"] = pd.to_datetime(data["Date"], format='mixed', errors='coerce')

# --------------- UI: SET MONTHLY LIMIT ---------------
st.sidebar.header("⚙️ Settings")
budget_limit = st.sidebar.number_input("Monthly Budget Limit (₹)", min_value=0.0, value=budget_limit, step=100.0, format="%.2f")
if st.sidebar.button("Save Budget"):
    save_settings(budget_limit)
    st.sidebar.success("Budget limit saved!")

# --------------- UI: ADD EXPENSE ---------------
with st.form("expense_form", clear_on_submit=True):
    st.subheader("➕ Add Expense")
    col1, col2 = st.columns(2)
    with col1:
        date = st.date_input("Date", datetime.today())
    with col2:
        category = st.selectbox("Category", ["Food", "Transport", "Shopping", "Bills", "Health", "Entertainment", "Others"])

    amount = st.number_input("Amount (₹)", min_value=0.0, step=0.01, format="%.2f")
    description = st.text_input("Description (optional)", max_chars=100)

    submitted = st.form_submit_button("Add Expense")
    if submitted and amount > 0:
        new_expense = pd.DataFrame({
            "Date": [pd.to_datetime(date)],
            "Category": [category],
            "Amount": [amount],
            "Description": [description]
        })
        data = pd.concat([data, new_expense], ignore_index=True)
        save_data(data)
        st.success("Expense added!")
        st.rerun()

# ---------------- DELETE ALL DATA ----------------
st.markdown("<hr>", unsafe_allow_html=True)
with st.expander("🗑️ Delete All Expense Data"):
    if st.button("Delete All Data"):
        if os.path.exists(DATA_FILE):
            os.remove(DATA_FILE)
        data = pd.DataFrame(columns=["Date", "Category", "Amount", "Description"])
        save_data(data)
        st.success("✅ All expense data has been deleted.")
        st.rerun()

# --------------- ANALYSIS ---------------
if not data.empty:
    st.subheader("📊 Monthly Spending Summary")
    data["Month"] = data["Date"].dt.to_period("M").astype(str)
    monthly_total = data.groupby("Month")["Amount"].sum().reset_index()
    this_month = datetime.today().strftime("%Y-%m")
    spent_this_month = monthly_total[monthly_total["Month"] == this_month]["Amount"].sum()

    if spent_this_month > budget_limit > 0:
        st.error(f"🚨 You exceeded your monthly budget of ₹{budget_limit:.2f}! You've spent ₹{spent_this_month:.2f}.")
        send_email_alert(spent_this_month)
    else:
        st.info(f"💸 This month: ₹{spent_this_month:.2f} / ₹{budget_limit:.2f}")

    chart = alt.Chart(monthly_total).mark_bar(color="#ff85a2").encode(
        x=alt.X("Month", sort=None, title="Month"),
        y=alt.Y("Amount", title="Total Spent (₹)"),
        tooltip=["Month", "Amount"]
    ).properties(height=350)

    st.altair_chart(chart, use_container_width=True)
    st.subheader("📋 All Expenses")
    st.dataframe(data.sort_values("Date", ascending=False), use_container_width=True)
else:
    st.info("No expenses yet. Start adding your expenses above!")
