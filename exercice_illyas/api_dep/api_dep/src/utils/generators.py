from datetime import datetime
import uuid

def generer_horodatage():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def generer_identifiant_unique():
    return str(uuid.uuid4())
