from flask import Flask
from __init__ import create_app
import sys
import logging


#--------------- VIEW FUNCTION------------------------------------------------

app = create_app()
#main method called web server application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) #runs a local server on a port 5000