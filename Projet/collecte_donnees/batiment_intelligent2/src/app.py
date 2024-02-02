from flask import Flask
from __init__ import create_app, db  # Importez également db si nécessaire
from auth import auth  # Importez le blueprint 'auth'

# Créez l'application Flask
app = create_app()

# Enregistrez le blueprint 'auth' dans l'application
app.register_blueprint(auth)

# main method called web server application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)