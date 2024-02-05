from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from __init__ import db


class Utilisateurs(db.Model):
    id_utilisateur = db.Column(db.Integer, primary_key=True)
    nom_utilisateur = db.Column(db.String(50), unique=True, nullable=False)
    mdp_utilisateur = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"Utilisateur(id_utilisateur={self.id_utilisateur}, nom_utilisateur={self.nom_utilisateur})"

class Lieu(db.Model):
    nom_lieu = db.Column(db.String(50), primary_key=True, unique=True, nullable=False)
    longitude_lieu = db.Column(db.Float)
    latitude_lieu = db.Column(db.Float)

    def __repr__(self):
        return f"Lieu(nom_lieu={self.nom_lieu})"

class DonneesMeteo(db.Model):
    id_donneesMeteo = db.Column(db.Integer, primary_key=True)
    horodatage_donneesMeteo = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    temperature_donneesMeteo = db.Column(db.Float)
    humidite_donneesMeteo = db.Column(db.Float)
    nom_lieu = db.Column(db.String(50), db.ForeignKey('lieu.nom_lieu'), nullable=False)

    lieu = db.relationship('Lieu', backref=db.backref('donneesMeteo', lazy='dynamic'))

    def __repr__(self):
        return f"DonneesMeteo(id_donneesMeteo={self.id_donneesMeteo}, temperature={self.temperature_donneesMeteo}, humidite={self.humidite_donneesMeteo})"

class Capteur(db.Model):
    id_capteur = db.Column(db.Integer, primary_key=True)
    nom_capteur = db.Column(db.String(30))
    horodatage_capteur = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    temperature_capteur = db.Column(db.Float)
    humidite_capteur = db.Column(db.Float)
    distance_capteur = db.Column(db.Integer)
    presence_capteur = db.Column(db.SmallInteger)
    bouton_capteur = db.Column(db.SmallInteger)
    nom_lieu = db.Column(db.String(50), db.ForeignKey('lieu.nom_lieu'), nullable=False)

    lieu = db.relationship('Lieu', backref=db.backref('capteurs', lazy='dynamic'))

    def __repr__(self):
        return f"Capteur(id_capteur={self.id_capteur}, nom_capteur={self.nom_capteur})"

class ComparaisonAPI(db.Model):
    id_comparaison_api = db.Column(db.Integer, primary_key=True)
    ludo_temperature_api = db.Column(db.Float)
    ludo_humidite_api = db.Column(db.Float)
    flo_temperature_api = db.Column(db.Float)
    flo_humidite_api = db.Column(db.Float)
    flo_ressentie_api = db.Column(db.Float)
    flo_pression_api = db.Column(db.Float)
    flo_vitessevent_api = db.Column(db.Float)
    flo_directionvent_api = db.Column(db.Float)

    def __repr__(self):
        return f"ComparaisonAPI(id_comparaison_api={self.id_comparaison_api})"
