import cv2
import numpy as np
from tensorflow.keras.models import load_model

def obtenir_pourcentages(predictions):
    pourcentages_pub = []
    pourcentages_nopub = []

    for prediction in predictions:
        pourcentage_pub = prediction[0][0] * 100
        pourcentage_nopub = prediction[0][1] * 100
        pourcentages_pub.append(pourcentage_pub)
        pourcentages_nopub.append(pourcentage_nopub)

    return pourcentages_pub, pourcentages_nopub