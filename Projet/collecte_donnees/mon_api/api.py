from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# Configuration de la base de données MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://ludo:root@192.168.20.61/domotique'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Désactive le suivi des modifications pour éviter les avertissements

db = SQLAlchemy(app)

class Capteurs(db.Model):
    id_capteur = db.Column(db.Integer, primary_key=True)
    nom_capteur = db.Column(db.String(30), nullable=False)
    horodatage_capteur = db.Column(db.DateTime, nullable=False)
    temperature_capteur = db.Column(db.Float, nullable=True)
    humidite_capteur = db.Column(db.Float, nullable=True)
    distance_capteur = db.Column(db.Integer, nullable=True)
    presence_capteur = db.Column(db.SmallInteger, nullable=False)
    Bouton_capteur = db.Column(db.SmallInteger, nullable=True)

    def as_dict(self):
        return {
            'id_capteur': self.id_capteur,
            'nom_capteur': self.nom_capteur,
            'horodatage_capteur': self.horodatage_capteur,
            'temperature_capteur': self.temperature_capteur,
            'humidite_capteur': self.humidite_capteur,
            'distance_capteur': self.distance_capteur,
            'presence_capteur': self.presence_capteur,
            'Bouton_capteur': self.Bouton_capteur
        }

class donneesMeteo(db.Model):
    __tablename__ = 'donneesMeteo'

    id_donneesMeteo = db.Column(db.Integer, primary_key=True)
    horodatage_donneesMeteo = db.Column(db.DateTime, nullable=False)
    temperature_donneesMeteo = db.Column(db.Float, nullable=True)
    humidite_donneesMeteo = db.Column(db.Float, nullable=True)

    def as_dict(self):
        return {
            'id_donneesMeteo': self.id_donneesMeteo,
            'horodatage_donneesMeteo': self.horodatage_donneesMeteo,
            'temperature_donneesMeteo': self.temperature_donneesMeteo,
            'humidite_donneesMeteo': self.humidite_donneesMeteo
        }
    
class comparaison_api(db.Model):
    id_comparaison_api = db.Column(db.Integer, primary_key=True)
    ludo_temperature_api = db.Column(db.Float, nullable=False)
    ludo_humidite_api = db.Column(db.Float, nullable=True)
    flo_temperature_api = db.Column(db.Float, nullable=True)
    flo_humidite_api = db.Column(db.Float, nullable=True)
    flo_ressentie_api = db.Column(db.Float, nullable=False)
    flo_pression_api = db.Column(db.Float, nullable=True)
    flo_vitessevent_api = db.Column(db.Float, nullable=True)
    flo_directionvent_api = db.Column(db.Float, nullable=True)
        
    def as_dict(self):
        return {
            'id_comparaison_api': self.id_comparaison_api,
            'ludo_temperature_api': self.ludo_temperature_api,
            'ludo_humidite_api': self.ludo_humidite_api,
            'flo_temperature_api': self.flo_temperature_api,
            'flo_humidite_api': self.flo_humidite_api,
            'flo_ressentie_api': self.flo_ressentie_api,
            'flo_pression_api': self.flo_pression_api,
            'flo_vitessevent_api': self.flo_vitessevent_api,
            'flo_directionvent_api': self.flo_directionvent_api
        }

# Routes
@app.route('/capteur', methods=['GET', 'POST'])
def manage_capteurs():
    if request.method == 'GET':
        items = Capteurs.query.all()
        items_list = [item.as_dict() for item in items]
        return jsonify({'capteur': items_list})
    elif request.method == 'POST':
        data = request.get_json()
        new_item = Capteurs(
            nom_capteur=data['nom_capteur'],
            horodatage_capteur=data['horodatage_capteur'],
            temperature_capteur=data.get('temperature_capteur'),
            humidite_capteur=data.get('humidite_capteur'),
            distance_capteur=data.get('distance_capteur'),
            presence_capteur=data['presence_capteur'],
            Bouton_capteur=data.get('Bouton_capteur')
        )
        db.session.add(new_item)
        db.session.commit()
        return jsonify({'message': 'Item created successfully!'})
    
@app.route('/capteur/<int:item_id>', methods=['DELETE'])
def delete_capteur(item_id):
    # Récupérer l'entrée spécifique par ID
    capteur = Capteurs.query.get(item_id)

    if capteur:
        # Supprimer l'entrée spécifique
        db.session.delete(capteur)
        db.session.commit()
        return jsonify({'message': f'Capteur with ID {item_id} deleted successfully!'})
    else:
        return jsonify({'message': f'Capteur with ID {item_id} not found'})


@app.route('/donneesmeteo', methods=['GET', 'POST'])
def manage_donnees_meteo():
    if request.method == 'GET':
        donnees = donneesMeteo.query.all()
        donnees_list = [donnee.as_dict() for donnee in donnees]
        return jsonify({'donnees_meteo': donnees_list})
    elif request.method == 'POST':
        data = request.get_json()
        new_donnee = donneesMeteo(
            horodatage_donneesMeteo=data.get('horodatage_donneesMeteo'),
            temperature_donneesMeteo=data.get('temperature_donneesMeteo'),
            humidite_donneesMeteo=data.get('humidite_donneesMeteo')
        )
        db.session.add(new_donnee)
        db.session.commit()
        return jsonify({'message': 'Donnee meteo created successfully!'})
    
@app.route('/comparaison_api', methods=['GET', 'POST'])
def manage_comparaison_api():
    if request.method == 'GET':
        comparaisons = comparaison_api.query.all()
        comparaisons_list = [comparaison.as_dict() for comparaison in comparaisons]
        return jsonify({'comparaison_api': comparaisons_list})
    elif request.method == 'POST':
        data = request.get_json()
        new_comparaison = comparaison_api(
            ludo_temperature_api=data.get('ludo_temperature_api'),
            ludo_humidite_api=data.get('ludo_humidite_api'),
            flo_temperature_api=data.get('flo_temperature_api'),
            flo_humidite_api=data.get('flo_humidite_api'),
            flo_ressentie_api=data.get('flo_ressentie_api'),
            flo_pression_api=data.get('flo_pression_api'),
            flo_vitessevent_api=data.get('flo_vitessevent_api'),
            flo_directionvent_api=data.get('flo_directionvent_api')
        )
        db.session.add(new_comparaison)
        db.session.commit()
        return jsonify({'message': 'Comparaison API data created successfully!'})
    
@app.route('/tables', methods=['GET'])
def get_tables():
    # Retourne la liste des tables disponibles
    tables = db.engine.table_names()
    return jsonify({'tables': tables})

@app.route('/table/<table_name>', methods=['GET', 'DELETE'])
def manage_table(table_name):
    if request.method == 'GET':
        # Récupérer toutes les données de la table spécifiée
        table_data = db.session.execute(f'SELECT * FROM {table_name}')
        rows = [dict(row) for row in table_data]
        return jsonify({'data': rows})

    elif request.method == 'DELETE':
        # Supprimer toutes les données de la table spécifiée
        db.session.execute(f'DELETE FROM {table_name}')
        db.session.commit()
        return jsonify({'message': f'All data in table {table_name} deleted successfully!'})
    

if __name__ == '__main__':
    app.run(host='192.168.20.55', port=5000, debug=True)

    