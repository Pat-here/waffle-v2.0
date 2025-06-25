from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FloatField, IntegerField, SelectField, DateField, PasswordField
from wtforms.validators import DataRequired, NumberRange
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date
from models import db
import os
from sqlalchemy_utils import database_exists, create_database

DEFAULT_ADMIN_USERNAME = 'admin'
DEFAULT_ADMIN_PASSWORD = 'admin123'



def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)  # rejestracja ORM w kontekście aplikacji

    with app.app_context():
        db.create_all()  # tworzy tabele zdefiniowane w models.py

    return app

app = create_app()

with app.app_context():
    # Tworzenie tabel, jeśli nie istnieją
    db.create_all()

    # Dodanie domyślnego konta administratora
    if not User.query.filter_by(username=DEFAULT_ADMIN_USERNAME).first():
        admin = User(
            username=DEFAULT_ADMIN_USERNAME,
            password_hash=generate_password_hash(DEFAULT_ADMIN_PASSWORD)
        )
        db.session.add(admin)
        db.session.commit()

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    cost = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(20), nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Composition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    cost = db.Column(db.Float, nullable=False, default=0)
    margin = db.Column(db.Float, nullable=False, default=0)
    status = db.Column(db.String(20), default='Aktywny')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class CompositionIngredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    composition_id = db.Column(db.Integer, db.ForeignKey('composition.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Float, nullable=False, default=1)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class WorkTime(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)
    hours = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    revenue = db.Column(db.Float, nullable=False, default=0)
    orders_count = db.Column(db.Integer, nullable=False, default=0)
    costs = db.Column(db.Float, nullable=False, default=0)
    profit = db.Column(db.Float, nullable=False, default=0)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ShoppingItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    priority = db.Column(db.String(20), default='Medium')
    status = db.Column(db.String(20), default='Oczekuje')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Forms
class LoginForm(FlaskForm):
    username = StringField('Nazwa użytkownika', validators=[DataRequired()])
    password = PasswordField('Hasło', validators=[DataRequired()])

class ProductForm(FlaskForm):
    name = StringField('Nazwa produktu', validators=[DataRequired()])
    category = SelectField('Kategoria', choices=[
        ('Podstawowe', 'Podstawowe'),
        ('Dodatki', 'Dodatki'),
        ('Owoce', 'Owoce'),
        ('Napoje', 'Napoje'),
        ('Inne', 'Inne')
    ])
    cost = FloatField('Koszt', validators=[DataRequired(), NumberRange(min=0)])
    unit = StringField('Jednostka', validators=[DataRequired()])
    stock = IntegerField('Stan magazynowy', validators=[DataRequired(), NumberRange(min=0)])

class CompositionForm(FlaskForm):
    name = StringField('Nazwa kompozycji', validators=[DataRequired()])
    price = FloatField('Cena sprzedaży', validators=[DataRequired(), NumberRange(min=0)])

class NoteForm(FlaskForm):
    title = StringField('Tytuł', validators=[DataRequired()])
    content = TextAreaField('Treść', validators=[DataRequired()])

class WorkTimeForm(FlaskForm):
    employee = StringField('Pracownik', validators=[DataRequired()])
    date = DateField('Data', validators=[DataRequired()])
    hours = FloatField('Godziny', validators=[DataRequired(), NumberRange(min=0, max=24)])
    description = StringField('Opis')

class ReportForm(FlaskForm):
    date = DateField('Data', validators=[DataRequired()])
    revenue = FloatField('Przychód', validators=[DataRequired(), NumberRange(min=0)])
    orders_count = IntegerField('Liczba zamówień', validators=[DataRequired(), NumberRange(min=0)])
    costs = FloatField('Koszty', validators=[DataRequired(), NumberRange(min=0)])
    notes = TextAreaField('Notatki')

# Routes
@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect(url_for('index'))
        flash('Nieprawidłowe dane logowania', 'error')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/products')
def products():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    products = Product.query.all()
    return render_template('products.html', products=products)

@app.route('/products/add', methods=['GET', 'POST'])
def add_product():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    form = ProductForm()
    if form.validate_on_submit():
        product = Product(
            name=form.name.data,
            category=form.category.data,
            cost=form.cost.data,
            unit=form.unit.data,
            stock=form.stock.data
        )
        db.session.add(product)
        db.session.commit()
        flash('Produkt został dodany', 'success')
        return redirect(url_for('products'))
    return render_template('add_product.html', form=form)

@app.route('/compositions')
def compositions():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    compositions = Composition.query.all()
    return render_template('compositions.html', compositions=compositions)

@app.route('/compositions/add', methods=['GET', 'POST'])
def add_composition():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    form = CompositionForm()
    if form.validate_on_submit():
        composition = Composition(
            name=form.name.data,
            price=form.price.data,
            cost=0,  # Will be calculated based on ingredients
            margin=0  # Will be calculated
        )
        db.session.add(composition)
        db.session.commit()
        flash('Kompozycja została dodana', 'success')
        return redirect(url_for('compositions'))
    return render_template('add_composition.html', form=form)

@app.route('/notes')
def notes():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    notes = Note.query.order_by(Note.created_at.desc()).all()
    return render_template('notes.html', notes=notes)

@app.route('/notes/add', methods=['GET', 'POST'])
def add_note():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    form = NoteForm()
    if form.validate_on_submit():
        note = Note(
            title=form.title.data,
            content=form.content.data
        )
        db.session.add(note)
        db.session.commit()
        flash('Notatka została dodana', 'success')
        return redirect(url_for('notes'))
    return render_template('add_note.html', form=form)

@app.route('/worktime')
def worktime():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    worktime_records = WorkTime.query.order_by(WorkTime.date.desc()).all()
    return render_template('worktime.html', worktime_records=worktime_records)

@app.route('/worktime/add', methods=['GET', 'POST'])
def add_worktime():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    form = WorkTimeForm()
    if form.validate_on_submit():
        worktime = WorkTime(
            employee=form.employee.data,
            date=form.date.data,
            hours=form.hours.data,
            description=form.description.data
        )
        db.session.add(worktime)
        db.session.commit()
        flash('Czas pracy został zapisany', 'success')
        return redirect(url_for('worktime'))
    return render_template('add_worktime.html', form=form)

@app.route('/reports')
def reports():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    reports = Report.query.order_by(Report.date.desc()).all()
    return render_template('reports.html', reports=reports)

@app.route('/reports/add', methods=['GET', 'POST'])
def add_report():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    form = ReportForm()
    if form.validate_on_submit():
        profit = form.revenue.data - form.costs.data
        report = Report(
            date=form.date.data,
            revenue=form.revenue.data,
            orders_count=form.orders_count.data,
            costs=form.costs.data,
            profit=profit,
            notes=form.notes.data
        )
        db.session.add(report)
        db.session.commit()
        flash('Raport został dodany', 'success')
        return redirect(url_for('reports'))
    return render_template('add_report.html', form=form)

@app.route('/shopping')
def shopping():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    shopping_items = db.session.query(ShoppingItem, Product).join(Product).all()
    return render_template('shopping.html', shopping_items=shopping_items)

@app.route('/calculator')
def calculator():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    products = Product.query.all()
    return render_template('calculator.html', products=products)

@app.route('/api/dashboard_stats')
def dashboard_stats():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    total_products = Product.query.count()
    total_compositions = Composition.query.count()
    low_stock_products = Product.query.filter(Product.stock < 5).count()

    # Calculate monthly revenue
    current_month = date.today().replace(day=1)
    monthly_revenue = db.session.query(db.func.sum(Report.revenue)).filter(
        Report.date >= current_month
    ).scalar() or 0

    return jsonify({
        'total_products': total_products,
        'total_compositions': total_compositions,
        'low_stock_products': low_stock_products,
        'monthly_revenue': monthly_revenue
    })

def init_db():
    with app.app_context():
        db.create_all()

        # Create admin user if not exists
        if not User.query.filter_by(username='admin').first():
            admin = User(
                username='admin',
                password_hash=generate_password_hash('admin123')
            )
            db.session.add(admin)

        # Add sample data if database is empty
        if Product.query.count() == 0:
            sample_products = [
                Product(name="Mąka", category="Podstawowe", cost=3.50, unit="kg", stock=10),
                Product(name="Jajka", category="Podstawowe", cost=12.00, unit="30szt", stock=2),
                Product(name="Mleko", category="Podstawowe", cost=3.20, unit="1l", stock=5),
                Product(name="Masło", category="Podstawowe", cost=8.50, unit="500g", stock=3),
                Product(name="Cukier", category="Podstawowe", cost=4.00, unit="1kg", stock=8),
                Product(name="Nutella", category="Dodatki", cost=15.00, unit="750g", stock=4),
                Product(name="Bita śmietana", category="Dodatki", cost=6.50, unit="500ml", stock=6),
                Product(name="Truskawki", category="Owoce", cost=12.00, unit="500g", stock=3),
                Product(name="Banany", category="Owoce", cost=6.00, unit="1kg", stock=2),
            ]

            for product in sample_products:
                db.session.add(product)

            sample_compositions = [
                Composition(name="Gofr podstawowy", price=8.00, cost=2.50, margin=68.75),
                Composition(name="Gofr z Nutellą", price=12.00, cost=4.20, margin=65.00),
                Composition(name="Gofr owocowy", price=15.00, cost=5.80, margin=61.33),
                Composition(name="Gofr premium", price=18.00, cost=6.50, margin=63.89),
            ]

            for comp in sample_compositions:
                db.session.add(comp)

            sample_notes = [
                Note(title="Zamówienie na piątek", content="Zamówić więcej truskawek na weekend"),
                Note(title="Nowy dostawca", content="Sprawdzić ceny u dostawcy z Krakowa"),
            ]

            for note in sample_notes:
                db.session.add(note)

        db.session.commit()

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
