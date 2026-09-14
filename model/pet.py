from model.base import db

class Pet(db.Model):
    __tablename__ = 'pets'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    especie = db.Column(db.String(20), nullable=False)
    sexo = db.Column(db.String(20), nullable=False)
    cor_pelagem = db.Column(db.String(50))
    raca = db.Column(db.String(50))
    idade = db.Column(db.Integer)
    bairro = db.Column(db.String(100))
    municipio = db.Column(db.String(100))
    uf = db.Column(db.String(2))
    foto = db.Column(db.String(200), nullable=True)
        