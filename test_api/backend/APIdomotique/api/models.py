from django.db import models


class lieux(models.Model):
    nom_lieu = models.CharField(max_length=50)
    latitude_lieu = models.FloatField()
    longitude_lieu = models.FloatField()

class capteurs(models.Model):
    nom_capteur = models.CharField(max_length=10)
    horodatage_capteur = models.DateTimeField()
    temperature_capteur = models.FloatField()
    humidite_capteur = models.FloatField()
    distance_capteur = models.IntegerField()
    presence_capteur = models.BooleanField()
    bouton_capteur = models.BooleanField()
    nom_lieu = models.ForeignKey(lieux, on_delete=models.CASCADE)

class comparaison_api(models.Model):
    ludo_temperature_api = models.FloatField()
    ludo_humidite_api = models.FloatField()
    flo_temperature_api = models.FloatField()
    flo_humidite_api = models.FloatField()
    flo_ressentie_api = models.FloatField()
    flo_pression_api = models.FloatField()
    flo_vitessevent_api = models.FloatField()
    flo_directionvent_api = models.FloatField

class donneesMeteo(models.Model):
    horodatage_donneesMeteo = models.DateTimeField()
    temperature_donneesMeteo = models.FloatField()
    humidite_donneesMeteo = models.FloatField()
    nom_lieu = models.ForeignKey(lieux, on_delete=models.CASCADE)



    # Ajoutez d'autres champs selon vos besoins
