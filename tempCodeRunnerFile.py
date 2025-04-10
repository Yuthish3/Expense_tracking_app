from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Email Configuration (Use your own email to test)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'yuthishkumar2004@gmail.com'  # replace
app.config['MAIL_PASSWORD'] = 'Yuthish#3'     # replace

db = SQLAlchemy(app)
mail = Mail(app)

# --------------------- MODELS ---------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    budgets = db.relationship('Budget', backref='user', lazy=True)

class Budget(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    month = db.Column(db.String(7))  # Format: YYYY-MM
    limit = db.Column(db.Float, nullable=False)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(120), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, default=datetime.utcnow)

# --------------------- ROUTES ---------------------
@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.json
    user = User(email=data['email'])
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User added'}), 201

@app.route('/add_budget', methods=['POST'])
def add_budget():
    data = request.json
    user = User.query.filter_by(email=data['email']).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    budget = Budget(user_id=user.id, category=data['category'], month=data['month'], limit=data['limit'])
    db.session.add(budget)
    db.session.commit()
    return jsonify({'message': 'Budget set'}), 201

@app.route('/add_expense', methods=['POST'])
def add_expense():
    data = request.json
    expense = Expense(user_email=data['email'], category=data['category'], amount=data['amount'])
    db.session.add(expense)
    db.session.commit()

    # Check for budget alert
    user = User.query.filter_by(email=data['email']).first()
    month = datetime.utcnow().strftime('%Y-%m')
    budget = Budget.query.filter_by(user_id=user.id, category=data['category'], month=month).first()
    if budget:
        total_spent = db.session.query(db.func.sum(Expense.amount)).filter_by(
            user_email=data['email'], category=data['category']
        ).filter(Expense.date.like(f"{month}-%")).scalar() or 0
        if total_spent > budget.limit:
            send_email(data['email'], f"Budget Alert: You exceeded your {data['category']} budget!")
        elif total_spent > 0.9 * budget.limit:
            send_email(data['email'], f"Warning: You have used over 90% of your {data['category']} budget.")
    return jsonify({'message': 'Expense added'}), 201

@app.route('/report/<email>', methods=['GET'])
def monthly_report(email):
    month = datetime.utcnow().strftime('%Y-%m')
    expenses = Expense.query.filter_by(user_email=email).filter(Expense.date.like(f"{month}-%")).all()
    summary = {}
    for e in expenses:
        summary[e.category] = summary.get(e.category, 0) + e.amount
    return jsonify({
        'month': month,
        'summary': summary,
        'total': sum(summary.values())
    })

# --------------------- UTIL ---------------------
def send_email(to, body):
    msg = Message("Expense Tracker Alert", sender="your_email@gmail.com", recipients=[to])
    msg.body = body
    mail.send(msg)

# --------------------- MAIN ---------------------
if __name__ == '__main__':
    with app.app_context():      # <-- This is the fix
        if not os.path.exists('expenses.db'):
            db.create_all()
    app.run(debug=True)

@app.route('/')
def home():
    return '''
    <h1>Expense Tracker API</h1>
    <p>Welcome! Use Postman or curl to interact with the API.</p>
    <p>Endpoints available:</p>
    <ul>
      <li>POST /add_user</li>
      <li>POST /add_budget</li>
      <li>POST /add_expense</li>
      <li>GET /report/&lt;email&gt;</li>
    </ul>
    '''

