from flask_jwt_extended import create_access_token, JWTManager
from Conf import db_config, secret_key
from flask import Flask
from datetime import timedelta
import pymysql

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = secret_key
jwt = JWTManager(app)  # Initialisez le JWTManager avec l'application Flask

def generate_token(username, password):
    # Établir une connexion à la base de données
    connection = pymysql.connect(**db_config)

    try:
        with connection.cursor() as cursor:
            # Rechercher l'utilisateur dans la base de données
            sql = "SELECT * FROM utilisateurs WHERE nom_utilisateurs = %s"
            cursor.execute(sql, (username,))
            user = cursor.fetchone()

            # Vérifier si l'utilisateur existe et si le mot de passe est correct
            if user and user[1] == username and user[2] == password:
                # Générer le token JWT avec create_access_token
                with app.app_context():
                    # Ajoutez le paramètre expires_delta pour définir la durée de validité
                    access_token = create_access_token(identity=username, expires_delta=timedelta(hours=1))

                # Écrivez le token dans le fichier
                with open('stored_token.txt', 'w') as file:
                    file.write(access_token)

                return access_token
            else:
                return None
    finally:
        connection.close()

def get_stored_token():
    try:
        with open('stored_token.txt', 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        return None

if __name__ == "__main__":
    # Utilisation du script en ligne de commande
    user = input("Nom d'utilisateur : ")
    password = input("Mot de passe : ")

    token = generate_token(user, password)

    if token:
        print(f"Token JWT généré : {token}")
    else:
        print("Échec de l'authentification.")

    stored_token = get_stored_token()
    print(f"Token stocké dans le fichier : {stored_token}")


print(f"Clé secrète utilisée côté client : {secret_key}")