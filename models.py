from flask_sqlalchemy import SQLAlchemy
from app import db

class Composition(db.Model):
    __tablename__ = 'composition'
    id         = db.Column(db.Integer,   primary_key=True, nullable=False)
    name       = db.Column(db.String(100), nullable=False)
    price      = db.Column(db.Float,      nullable=False)
    cost       = db.Column(db.Float,      nullable=False)
    margin     = db.Column(db.Float, nullable=False)
    status     = db.Column(db.String(20), nullable=True)
    created_at = db.Column(db.DateTime,   nullable=False)

class CompositionIngredient(db.Model):
    __tablename__     = 'composition_ingredient'
    id                = db.Column(db.Integer, primary_key=True, nullable=False)
    composition_id    = db.Column(db.Integer, db.ForeignKey('composition.id'), nullable=False)
    product_id        = db.Column(db.Integer, db.ForeignKey('product.id'),     nullable=False)
    quantity          = db.Column(db.Float,   nullable=False)

class Product(db.Model):
    __tablename__ = 'product'
    id            = db.Column(db.Integer,   primary_key=True, nullable=False)
    name          = db.Column(db.String(100), nullable=False)
    category      = db.Column(db.String(50),  nullable=False)
    cost          = db.Column(db.Float,      nullable=False)
    unit          = db.Column(db.String(20), nullable=False)
    stock         = db.Column(db.Integer,    nullable=False)
    created_at    = db.Column(db.DateTime,   nullable=False)

class Note(db.Model):
    __tablename__ = 'note'
    id          = db.Column(db.Integer,   primary_key=True, nullable=False)
    title       = db.Column(db.String(200), nullable=False)
    content     = db.Column(db.Text,      nullable=False)
    created_at  = db.Column(db.DateTime,  nullable=False)

class Report(db.Model):
    __tablename__ = 'report'
    id           = db.Column(db.Integer,   primary_key=True, nullable=False)
    date         = db.Column(db.Date,      nullable=False)
    revenue      = db.Column(db.Float,     nullable=False)
    orders_count = db.Column(db.Integer,   nullable=False)
    costs        = db.Column(db.Float,     nullable=False)
    profit       = db.Column(db.Float,     nullable=False)
    notes        = db.Column(db.Text,      nullable=True)
    created_at   = db.Column(db.DateTime,  nullable=False)

class ShoppingItem(db.Model):
    __tablename__  = 'shopping_item'
    id              = db.Column(db.Integer, primary_key=True, nullable=False)
    product_id      = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity        = db.Column(db.Float,   nullable=False)
    priority        = db.Column(db.String(20), nullable=True)
    status          = db.Column(db.String(20), nullable=True)
    created_at      = db.Column(db.DateTime,  nullable=False)

class WorkTime(db.Model):
    __tablename__ = 'work_time'
    id           = db.Column(db.Integer,   primary_key=True, nullable=False)
    employee     = db.Column(db.String(100), nullable=False)
    date         = db.Column(db.Date,      nullable=False)
    hours        = db.Column(db.Float,     nullable=False)
    description  = db.Column(db.String(200), nullable=True)
    created_at   = db.Column(db.DateTime,  nullable=False)

class User(db.Model):
    __tablename__    = 'users'
    id               = db.Column(db.Integer,  primary_key=True, nullable=False)
    username         = db.Column(db.String(80),  unique=True, nullable=False)
    password_hash    = db.Column(db.String(120), nullable=False)
