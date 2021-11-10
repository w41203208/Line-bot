from sqlalchemy.orm import backref
from . import db
from sqlalchemy.sql import func


class ProteinRange(db.Model):
    __tablename__ = 'protein_range'

    protein_index = db.Column(db.Integer, primary_key=True, autoincrement=True)
    protein_name = db.Column(db.Text)
    protein_desc = db.Column(db.Text)
    products = db.relationship('Product', backref='product')

class Product(db.Model):
    __tablename__ = 'product'

    product_index = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_name = db.Column(db.Text(150))
    product_tag = db.Column(db.Text)
    product_kcal = db.Column(db.Float)
    product_protein = db.Column(db.Float)
    product_Na = db.Column(db.Float)
    product_Ka = db.Column(db.Float)
    product_p = db.Column(db.Float)
    product_carbohydrate = db.Column(db.Float)
    product_protein_range = db.Column(db.Integer, db.ForeignKey('protein_range.protein_index'))


