import os
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np

# Importer la fonction predict_advertisement
def predict_advertisement(image_data, model_path='model_with_dropout1.h5'):
    # Charger le modèle 
    model = tf.keras.models.load_model(model_path)

    # Prétraiter l'image
    img_array = image.img_to_array(image_data)
    img_array = np.expand_dims(img_array, axis=0) / 255.0  # Normaliser l'image

    # prédiction
    prediction = model.predict(img_array)

    prob_advertisement_a = prediction[0][0]  # Probabilité de "advertisement"
    prob_no_advertisement_a = prediction[0][1]  # Probabilité de "no advertisement"

    # Formater les probabilités pour les afficher sous forme de chiffres normaux
    prob_advertisement = np.format_float_positional(prob_advertisement_a, precision=6) # logo
    prob_no_advertisement = np.format_float_positional(prob_no_advertisement_a, precision=6) # pas logo

    print("Probabilité de publicité:", prob_advertisement)
    print("Probabilité de non-publicité:", prob_no_advertisement)

    return prob_advertisement, prob_no_advertisement






















# folder_path = "snapshot/2024-03-15"

# # Liste des fichiers dans le dossier
# image_files = os.listdir(folder_path)


# # Parcourir tous les fichiers d'images et appliquer la fonction predict_advertisement
# for image_file in image_files:
#     # Charger l'image
#     image_path = os.path.join(folder_path, image_file)
#     img = image.load_img(image_path, target_size=(100, 100))

#     # Appeler la fonction predict_advertisement
#     print("Analyse de l'image:", image_file)
#     predict_advertisement(img)
#     print()