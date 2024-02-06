import os
import numpy as np
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from tensorflow.keras.callbacks import EarlyStopping

# Chemins des dossiers contenant les images avec et sans logo
dossier_logo = os.path.join('datasets', 'augmente2', 'logo-tv')
dossier_pas_logo = os.path.join('datasets', 'augmente2', 'pas-logo-tv')

# Paramètres pour l'entraînement
batch_size = 32
epochs = 20
img_height, img_width = 100, 100

# Utilisation de l'ImageDataGenerator pour charger les images
datagen = ImageDataGenerator(rescale=1./255)

# Chargement des images depuis les dossiers
train_generator_logo = datagen.flow_from_directory(
    dossier_logo,
    target_size=(img_height, img_width),
    batch_size=batch_size,
    class_mode='binary'
)

train_generator_pas_logo = datagen.flow_from_directory(
    dossier_pas_logo,
    target_size=(img_height, img_width),
    batch_size=batch_size,
    class_mode='binary'
)

# Création du modèle CNN
model = Sequential()
model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(img_height, img_width, 3)))
model.add(MaxPooling2D((2, 2)))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D((2, 2)))
model.add(Conv2D(128, (3, 3), activation='relu'))
model.add(MaxPooling2D((2, 2)))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dense(1, activation='sigmoid'))

# Compilation du modèle
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Callback pour arrêter l'entraînement prématurément si la performance ne s'améliore pas
early_stopping_callback = EarlyStopping(monitor='val_loss', patience=3)

# Entraînement du modèle avec le callback
model.fit(
    x=train_generator_logo,
    epochs=epochs,
    steps_per_epoch=len(train_generator_logo),
    validation_data=train_generator_pas_logo,
    validation_steps=len(train_generator_pas_logo),
    callbacks=[early_stopping_callback]
)

# Sauvegarde du modèle
model.save('modele_logo.h5')
