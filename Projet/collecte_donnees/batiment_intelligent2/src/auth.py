# auth.py
from database import Utilisateurs
from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
import validators
from __init__ import db

auth = Blueprint("auth", __name__, url_prefix="/api/v1/auth")

@auth.post('/register')
def register():
    nom_utilisateur = request.json['username']
    mdp_utilisateur = request.json['password']
    

    if len(mdp_utilisateur) < 5:

        return jsonify({'error':"Password is too short"})
    
    if len(nom_utilisateur) < 3:

        return jsonify({'error':"Username is too short"})
    
    if not nom_utilisateur.isalnum() or " " in nom_utilisateur:

        return jsonify({'error':"Username should be alphanumeric, also no spaces"})
    
    pwd_hash = generate_password_hash(mdp_utilisateur)

    user = Utilisateurs(nom_utilisateur=nom_utilisateur, mdp_utilisateur=pwd_hash)
    db.session.add(user)
    db.session.commit()

    return jsonify({
        'message': 'User created',
        'user':{
            'username':nom_utilisateur
        }
    })



@auth.post('/login')
def login():
    try:
        username = request.json.get('nom_utilisateur', '')
        password = request.json.get('mdp_utilisateur', '')

        user = Utilisateurs.query.filter_by(nom_utilisateur=username).first()

        if user is None:
            return jsonify({'error': 'Utilisateur non trouvé'}), 401  # 401 Unauthorized

        if check_password_hash(Utilisateurs.mdp_utilisateur, password):
            return jsonify({'message': 'Connexion réussie'}), 200  # 200 OK
        else:
            return jsonify({'error': 'Mot de passe incorrect'}), 401  # 401 Unauthorized
    except Exception as e:
        print(f"Exception in login endpoint: {e}")  # Ajoutez cette ligne pour imprimer l'exception
        return jsonify({'error': 'Une erreur interne s\'est produite'}), 500  # 500 Internal Server Error




@auth.get("/me")
def me():
    return {"user":"me"}


