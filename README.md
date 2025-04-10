Sure! Here's the complete content of your `README.md` in markdown format, cleaned up (no emojis, no folder structure or evaluation criteria) and with a **Google App Password setup guide** added at the end.

---

```markdown
# Expense & Budget Tracker with Group Sharing

This is a Flask-based Expense Tracker web application that helps users manage their **daily expenses**, set **monthly budgets** for each category, receive **alerts when budgets are exceeded**, and even share **group expenses** similar to Splitwise.

---

## Features

### Individual Features
- Add daily expenses
- Categorize expenses (e.g., Food, Transport, Entertainment)
- Set monthly budgets per category
- Alerts when category budget is exceeded
- Custom alert when only 10% budget remains
- Monthly reports showing:
  - Total spending
  - Spending vs. budget per category
- Email notifications when budget limits are approached or exceeded

### Group Expense Sharing
- Create and manage groups
- Add group expenses
- Automatically split and calculate balances
- View group reports and individual balances
- Track expense history within a group

---

## Technologies Used

- Backend: Flask, Flask-SQLAlchemy, Flask-Mail
- Frontend: HTML, Bootstrap (minimal styling)
- Database: SQLite
- Emailing: Flask-Mail with custom alerts
- Deployment: Docker-ready

---

## Getting Started

### Clone the Repository
```bash
git clone https://github.com/yourusername/expense-tracker.git
cd expense-tracker
```

### Run Locally (Without Docker)

#### 1. Create virtual environment & activate:
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

#### 2. Install requirements:
```bash
pip install -r requirements.txt
```

#### 3. Set environment variables:
Create a `.env` file and add the following:
```
FLASK_APP=app.py
FLASK_ENV=development
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_google_app_password
```

#### 4. Run the application:
```bash
flask run
```

Visit [http://localhost:5000](http://localhost:5000)

---

## Running Using Docker

### Step 1: Build Docker Image
```bash
docker build -t expense-tracker .
```

### Step 2: Run Docker Container
```bash
docker run -p 5050:5000 expense-tracker
```

Visit [http://localhost:5050](http://localhost:5050)

---

## Setting Up Google App Password (for Gmail Alerts)

If you're using a Gmail account to send email notifications, a regular password will not work. Follow the steps below to generate an **App Password**:

1. Go to your Google Account: [https://myaccount.google.com](https://myaccount.google.com)
2. Navigate to **Security**.
3. Enable **2-Step Verification** if not already enabled.
4. Once enabled, go to the **App Passwords** section.
5. Select the app as "Mail" and the device as "Other" (name it anything, like "Expense Tracker").
6. Click **Generate**.
7. Copy the 16-character app password provided.
8. Use this password in your `.env` file as `MAIL_PASSWORD`.

---

## Test Instructions

Once the app is running:

1. Navigate to the home page:
   - Add individual expenses
   - Set budgets for each category
   - View reports

2. For group expenses:
   - Create a group
   - Add shared expenses
   - View balance and expense history

3. Trigger email alerts by setting a budget and exceeding or nearing it

---

## Developer

Developed by **Yuthish Kumar V**  
Features including budget alerts, email notifications, and group-based expense sharing were implemented as part of this application.
