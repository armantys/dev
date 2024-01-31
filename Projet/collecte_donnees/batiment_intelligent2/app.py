from flask import *
import sys
import logging

#--------CONFIGURE APP -----------------------------------------------

app = Flask(__name__)
logging.basicConfig(filename='logs/flask.log', level=logging.INFO)
sys.tracebacklimit = 10

#--------------- VIEW FUNCTION------------------------------------------------

@app.route('/')
def login():
    app.logger.info("Login")
    return "<h1>Login<h1>"

@app.route('/register')
def register():
    app.logger.info("Register")
    return "<h1>Register<h1>"

#main method called web server application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) #runs a local server on a port 5000