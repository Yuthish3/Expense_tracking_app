
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
- Email notifications when budget limits are approached or exceeded *(optional)*

### Group Expense Sharing
- Create and manage groups
- Add group expenses
- Automatically split and calculate balances
- View group reports and individual balances
- Track expense history within a group

---

## Technologies Used

- **Backend:** Flask, Flask-SQLAlchemy, Flask-Mail
- **Frontend:** HTML, Bootstrap (minimal styling)
- **Database:** SQLite
- **Emailing:** Flask-Mail with custom alerts (optional)
- **Deployment:** Docker-ready

---

## Getting Started

### Clone the Repository
```bash
git clone https://github.com/Yuthish3/Expense_tracking_app.git
cd Expense_tracking_app
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

#### 3. [Optional] Set Email Credentials for Budget Alerts

> 💡 *You can skip this step if you do not want email alerts. The application will still work fully — only the alerts will be skipped.*

If you want email alerts, open `app.py` and enter:
```python
MAIL_USERNAME = 'your_email@gmail.com'
MAIL_PASSWORD = 'your_google_app_password'
```

Alternatively, you can set these as environment variables before running.

#### 4. Run the application:
```bash
flask run
```

Visit [http://127.0.0.1:5000](http://127.0.0.1:5000)


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

To enable email alerts using Gmail:

1. Go to your Google Account: [https://myaccount.google.com](https://myaccount.google.com)
2. Navigate to **Security**
3. Enable **2-Step Verification**
4. After enabling, go to **App Passwords**
5. Select App = Mail, Device = Other (name it "Expense Tracker")
6. Click **Generate**
7. Copy the 16-character app password
8. Paste it into `app.py` under `MAIL_PASSWORD`

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

3. Trigger email alerts by setting a budget and exceeding or nearing it (if credentials are configured)

---

Results
---

---

## 📸 Results

### 💻 Home Page
![Home Page](Output_screenshots/Screenshot%202025-04-10%20at%203.45.37%E2%80%AFPM.png)

### 📊 Budget Report
![Budget Report](Output_screenshots/Screenshot%202025-04-10%20at%203.46.07%E2%80%AFPM.png)

### ➕ Add Group Expense
![Add Group Expense](Output_screenshots/Screenshot%202025-04-10%20at%203.48.24%E2%80%AFPM.png)

### 👥 Group Expense Report
![Group Report](Output_screenshots/Screenshot%202025-04-10%20at%204.02.08%E2%80%AFPM.png)



## Developer

Developed by **Yuthish Kumar V**

Features include:
- Budget tracking and reporting
- Email notifications
- Group-based expense sharing (like Splitwise)


