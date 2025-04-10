from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail, Message
from datetime import datetime
import os

# ======================
# App and Configurations
# ======================

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# ======================
# Mail Configuration
# ======================

app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USERNAME='',## enter own email id 
    MAIL_PASSWORD='',  # enter App-specific password genrated by google to send emails
)
mail = Mail(app)

# ======================
# Database Models
# ======================

class User(db.Model):
    """Model for registered users."""
    email = db.Column(db.String(120), primary_key=True)

class Budget(db.Model):
    """Model for storing monthly budget limits by category."""
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), db.ForeignKey('user.email'))
    category = db.Column(db.String(50))
    month = db.Column(db.String(7))  # Format: YYYY-MM
    limit = db.Column(db.Float)

class Expense(db.Model):
    """Model for tracking individual user expenses."""
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), db.ForeignKey('user.email'))
    category = db.Column(db.String(50))
    amount = db.Column(db.Float)
    date = db.Column(db.DateTime, default=datetime.utcnow)

class Group(db.Model):
    """Model representing a shared expense group."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

class GroupMember(db.Model):
    """Model representing members within a group."""
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    email = db.Column(db.String(120))

class GroupExpense(db.Model):
    """Model to track group expenses and their contributors."""
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    description = db.Column(db.String(200))
    paid_by = db.Column(db.String(120))
    amount = db.Column(db.Float)
    date = db.Column(db.DateTime, default=datetime.utcnow)

# ======================
# Utility Functions
# ======================

def send_email(to, body):
    """Sends email alerts regarding budget status."""
    try:
        msg = Message("Expense Tracker Alert", sender="yuthishkumar2004@gmail.com", recipients=[to])
        msg.body = body
        mail.send(msg)
        print("✅ Email sent to", to)
    except Exception as e:
        print("❌ Email sending failed:", e)

# ======================
# Routes - Web Interface
# ======================

@app.route('/')
def index():
    """Render the home page."""
    return render_template('index.html')

@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    """Add a new user based on email."""
    if request.method == 'POST':
        email = request.form['email']
        if not User.query.get(email):
            db.session.add(User(email=email))
            db.session.commit()
            return redirect(url_for('index'))
        else:
            return "User already exists"
    return render_template('add_user.html')

@app.route('/add_budget', methods=['GET', 'POST'])
def add_budget():
    """Add a budget limit for a category in a specific month."""
    if request.method == 'POST':
        email = request.form['email']
        category = request.form['category']
        month = request.form['month']
        limit = float(request.form['limit'])
        budget = Budget(email=email, category=category, month=month, limit=limit)
        db.session.add(budget)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_budget.html')

@app.route('/add_expense', methods=['GET', 'POST'])
def add_expense():
    """Add an expense and send alerts if the budget is exceeded."""
    if request.method == 'POST':
        email = request.form['email']
        category = request.form['category']
        amount = float(request.form['amount'])
        expense = Expense(email=email, category=category, amount=amount)
        db.session.add(expense)
        db.session.commit()

        # === Budget Check ===
        now = datetime.now()
        month = f"{now.year}-{now.month:02d}"
        budget = Budget.query.filter_by(email=email, category=category, month=month).first()

        if budget:
            total_spent = db.session.query(db.func.sum(Expense.amount)).filter_by(email=email, category=category).scalar() or 0
            if total_spent > budget.limit:
                send_email(email, f"🚨 Budget Alert: You exceeded your {category} budget of ₹{budget.limit}!")
            elif total_spent > 0.9 * budget.limit:
                send_email(email, f"⚠️ Warning: You've used over 90% of your {category} budget!")

        return redirect(url_for('index'))

    return render_template('add_expense.html')

@app.route('/report/<email>')
def report(email):
    """Generate a monthly spending report for a user."""
    now = datetime.now()
    month = f"{now.year}-{now.month:02d}"

    # Fetch all expenses
    expenses = Expense.query.filter_by(email=email).all()
    summary = {}
    total = 0
    for expense in expenses:
        cat = expense.category
        summary[cat] = summary.get(cat, 0) + expense.amount
        total += expense.amount

    # Fetch budgets
    budget_entries = Budget.query.filter_by(email=email, month=month).all()
    budgets = {entry.category: entry.limit for entry in budget_entries}

    return render_template('report.html', email=email, month=month, summary=summary, total=total, budgets=budgets)

@app.route('/report_redirect', methods=['POST'])
def report_redirect():
    """Redirect POST form input to the user-specific report page."""
    email = request.form['email']
    return redirect(url_for('report', email=email))

# ======================
# Routes - Group Expenses
# ======================

@app.route('/create_group', methods=['GET', 'POST'])
def create_group():
    """Create a group with a list of members."""
    if request.method == 'POST':
        name = request.form['group_name']
        members = request.form['members'].split(',')
        group = Group(name=name)
        db.session.add(group)
        db.session.commit()
        for email in members:
            db.session.add(GroupMember(group_id=group.id, email=email.strip()))
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('create_group.html')

@app.route('/add_group_expense', methods=['GET', 'POST'])
def add_group_expense():
    """Add a shared expense to a group."""
    if request.method == 'POST':
        group_name = request.form['group_name']
        description = request.form['description']
        paid_by = request.form['paid_by']
        amount = float(request.form['amount'])
        date_str = request.form['date']
        date = datetime.strptime(date_str, '%Y-%m-%d')

        group = Group.query.filter_by(name=group_name).first()
        if group:
            new_expense = GroupExpense(
                group_id=group.id,
                description=description,
                paid_by=paid_by,
                amount=amount,
                date=date
            )
            db.session.add(new_expense)
            db.session.commit()
            return "Expense added successfully!"
        else:
            return "Group not found!"

    return render_template('add_group_expense.html')

@app.route('/group_report', methods=['GET'])
def group_report():
    """
    Generate a report showing how much each member owes or is owed
    based on total group expenses.
    """
    group_name = request.args.get('group_name')
    balances = {}
    expense_history = []

    if group_name:
        group = Group.query.filter_by(name=group_name).first()
        if not group:
            return "Group not found!"

        members = GroupMember.query.filter_by(group_id=group.id).all()
        member_emails = [m.email for m in members]
        expenses = GroupExpense.query.filter_by(group_id=group.id).order_by(GroupExpense.date).all()

        contributions = {email: 0 for email in member_emails}
        total = 0

        for e in expenses:
            contributions[e.paid_by] += e.amount
            total += e.amount
            expense_history.append({
                'date': e.date.strftime('%Y-%m-%d'),
                'description': e.description,
                'paid_by': e.paid_by,
                'amount': e.amount
            })

        share = total / len(member_emails)
        balances = {email: round(contributions[email] - share, 2) for email in member_emails}

    return render_template('group_report.html', balances=balances, expense_history=expense_history)

# ======================
# Run Application
# ======================

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
