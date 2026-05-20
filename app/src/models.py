from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)

    suscripciones = db.relationship('Suscripcion', backref='usuario', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Usuario {self.email}>"

class Producto(db.Model):
    __tablename__ = 'productos'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Numeric(10, 2), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)

    suscripciones = db.relationship('Suscripcion', backref='producto', lazy=True)

    def __repr__(self):
        return f"<Producto {self.nombre}>"

class Suscripcion(db.Model):
    __tablename__ = 'suscripciones'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id', ondelete='CASCADE'), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'), nullable=False)
    estado = db.Column(db.String(20), default='activa', nullable=False)
    fecha_inicio = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_fin = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f"<Suscripcion Usuario:{self.usuario_id} -> Producto:{self.producto_id}>"
