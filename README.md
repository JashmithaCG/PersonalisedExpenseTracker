# PersonalisedExpenseTracker
A personalized Streamlit-based Expense Tracker to record, analyze, and visualize monthly spending. Features include budget limit alerts (UI + email), expense categorization, data deletion, beautiful UI theme, and interactive charts. Ideal for managing personal finances with ease and clarity.
# 📒 Personalized Expense Tracker

A user-friendly **Streamlit** web app to record, analyze, and visualize monthly expenses. Perfect for managing personal finances with features like **monthly budget alerts**, **email notifications**, and **interactive graphs**.

## 🚀 Features

- 📅 **Add Daily Expenses** with category, amount, and description.
- 📊 **Interactive Monthly Graphs** using Altair.
- 🧾 **Expense Table View** sorted by date.
- 💸 **Set Monthly Budget Limit** via sidebar.
- 🚨 **Warning Display** if the budget limit is exceeded.
- 📧 **Email Notification** when you cross your budget.
- 🗑️ **One-Click Data Deletion** with confirmation.
- 🎨 **Clean UI Theme** with gradient background.

---

## 🛠️ Tech Stack

- [Python 3.x](https://www.python.org/)
- [Streamlit](https://streamlit.io/)
- [Pandas](https://pandas.pydata.org/)
- [Altair](https://altair-viz.github.io/)
- [SMTP](https://docs.python.org/3/library/smtplib.html) (for email alerts)

---

## 📂 Project Structure

📁 PersonalizedExpenseTracker/
├── expense_tracker.py
├── expenses.csv # Generated after adding data
├── settings.csv # Stores budget limit
└── README.md

🔐 Security
The app uses an app-specific Gmail password to send email alerts.
⚠️ Do not commit your actual password to GitHub — use environment variables or .streamlit/secrets.toml for production use.

📧 Email Alerts
If monthly expenses exceed the budget, an alert email will be sent to your configured Gmail address (EMAIL_ADDRESS in code). Make sure your email and password are valid and have SMTP enabled.

📸 Screenshots
<img width="436" height="655" alt="image" src="https://github.com/user-attachments/assets/c15df6ec-fe36-47f2-8d52-e5520c7004a4" />


✅ Future Enhancements
Authentication/Login support.

Filter expenses by custom date ranges.

Export to Excel/PDF.

Cloud sync (e.g., Firebase or Google Sheets).

Mobile-optimized view.

📄 License
This project is developed for educational purposes only, not for commercial use.
