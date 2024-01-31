from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Utilisateur(db.Model):
    id_utilisateurs = db.Column(db.Integer, primary_key=True)