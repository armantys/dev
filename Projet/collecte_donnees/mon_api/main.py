from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
import pymysql
import requests
from generate_token import get_stored_token
from Conf import db_config,secret_key

app = Flask(__name__)

# Obtenez la clé secrète depuis la fonction get_stored_token
stored_token = get_stored_token()

# Assurez-vous que la clé secrète est définie avant de configurer le JWTManager
if stored_token:
    app.config['JWT_SECRET_KEY'] = secret_key
    jwt = JWTManager(app)
else:
    print("La clé secrète n'est pas disponible. Veuillez vous connecter pour générer un token.")

# Variable pour stocker le token
current_token = None

# Fonction pour établir une connexion à la base de données
def get_db():
    return pymysql.connect(**db_config)

# Route pour générer un token JWT
@app.route('/login', methods=['POST'])
def login():
    global current_token  # Utilisez la variable globale pour stocker le token
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    # Établir une connexion à la base de données
    connection = get_db()

    try:
        with connection.cursor() as cursor:
            # Rechercher l'utilisateur dans la base de données
            sql = "SELECT * FROM utilisateurs WHERE nom_utilisateurs = %s"
            cursor.execute(sql, (username,))
            user = cursor.fetchone()
            
            # Vérifier si l'utilisateur existe et si le mot de passe est correct
            if user and user[1] == username and user[2] == password:
                # Générer le token JWT avec create_access_token
                access_token = create_access_token(identity=username)
                
                # Stocker le token dans la variable globale
                current_token = access_token

                # Retourner le token sous forme JSON
                return jsonify({'token': access_token}), 200
            else:
                # Informer que l'utilisateur n'existe pas
                return jsonify({'message': 'Utilisateur inexistant'}), 401
    finally:
        connection.close()

# Utilisez la variable current_token dans vos requêtes futures
# par exemple, dans la route /api/data
@app.route('/api/data', methods=['GET'])
@jwt_required()
def get_databases():
    print("La route /api/data est atteinte.")  # Ajoutez cette ligne pour déboguer
    global current_token  # Utilisez la variable globale pour inclure le token
    try:
        connection = get_db()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SHOW TABLES")

        # Utilisez current_token dans l'en-tête Authorization
        headers = {'Authorization': f'Bearer {current_token}'}

        # Ajoutez une ligne pour imprimer le token côté serveur
        print(f"Token reçu côté serveur : {request.headers.get('Authorization')}")

        # Effectuez la requête avec les en-têtes
        response = requests.get('http://127.0.0.1:5000/api/data', headers=headers)

        # Traitez la réponse
        data = response.json()

        return jsonify(data)
    finally:
        cursor.close()
        connection.close()
 
# Route pour obtenir tous les enregistrements d'une table spécifique
@app.route('/Gdata/<table_name>', methods=['GET'])
@jwt_required()
def get_all_data(table_name):
    if table_name == 'utilisateurs':
        return jsonify({'message': 'La table utilisateurs ne peut pas être consultée.'}), 403  # 403 Forbidden
    else :
        try:
            connection = get_db()
            cursor = connection.cursor(pymysql.cursors.DictCursor)
            cursor.execute(f'SELECT * FROM {table_name}')
            data = cursor.fetchall()
            return jsonify(data)
        finally:
            cursor.close()
            connection.close()
 
# Route pour insérer un nouvel enregistrement
@app.route('/Pdata/<table_name>', methods=['POST'])
@jwt_required()
def insert_data(table_name):
    try:
        connection = get_db()
        cursor = connection.cursor()
        data_to_insert = request.json
        columns = ', '.join(data_to_insert.keys())
        values = ', '.join(['%s'] * len(data_to_insert))
        query = f'INSERT INTO {table_name} ({columns}) VALUES ({values})'
        cursor.execute(query, tuple(data_to_insert.values()))
        connection.commit()
        return jsonify({'message': 'Enregistrement inséré avec succès'})
    finally:
        cursor.close()
        connection.close()
 
# Route pour mettre à jour un enregistrement
@app.route('/Udata/<table_name>/<int:data_id>', methods=['PUT'])
@jwt_required()
def update_data(table_name, data_id):
    try:
        connection = get_db()
        cursor = connection.cursor()
        data_to_update = request.json
        updates = ', '.join([f"{key}=%s" for key in data_to_update.keys()])
        query = f'UPDATE {table_name} SET {updates} WHERE id={data_id}'
        cursor.execute(query, tuple(data_to_update.values()))
        connection.commit()
        return jsonify({'message': 'Enregistrement mis à jour avec succès'})
    finally:
        cursor.close()
        connection.close()
 
# Route pour supprimer un enregistrement
@app.route('/Ddata/<table_name>/<int:data_id>', methods=['DELETE'])
@jwt_required()
def delete_data(table_name, data_id):
    try:
        connection = get_db()
        cursor = connection.cursor()
        cursor.execute(f'DELETE FROM {table_name} WHERE id={data_id}')
        connection.commit()
        return jsonify({'message': 'Enregistrement supprimé avec succès'})
    finally:
        cursor.close()
        connection.close()
 
if __name__ == '__main__':
    # Récupérez le token de votre stockage (base de données, fichier, etc.)
    stored_token = get_stored_token()  # Vous devez implémenter cette fonction

    if stored_token:
        app.config['JWT_SECRET_KEY'] = stored_token  # Utilisez le token stocké comme clé secrète
        app.run(host='127.0.0.1', port=5000, debug=True)
    else:
        print("Impossible de démarrer l'application sans un token valide.")

print(f"Clé secrète utilisée côté serveur : {app.config['JWT_SECRET_KEY']}")
