import os
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import layers, models

with_logo_dir = r'C:\Users\ludovic.souquet\Documents\GitHub\ludovic.souquet\Projet\Pub_noPub\pubnopub\logo2'
without_logo_dir = r'C:\Users\ludovic.souquet\Documents\GitHub\ludovic.souquet\Projet\Pub_noPub\pubnopub\nologo'

# Définir les paramètres
img_height, img_width = 100, 100
batch_size = 32
num_epochs = 10

# Créer les générateurs de données
train_datagen = ImageDataGenerator(rescale=1./255)
validation_datagen = ImageDataGenerator(rescale=1./255)

# Utiliser le générateur d'images augmentées pour l'entraînement
train_datagen_augmented = ImageDataGenerator(
    rescale=1./255,
    rotation_range=40,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest'
)

# Utiliser le générateur d'images augmentées pour l'entraînement
train_generator_augmented = train_datagen_augmented.flow_from_directory(
    with_logo_dir,
    target_size=(img_height, img_width),
    batch_size=batch_size,
    class_mode='binary'
)

validation_generator = validation_datagen.flow_from_directory(
    without_logo_dir,
    target_size=(img_height, img_width),
    batch_size=batch_size,
    class_mode='binary'
)

print(f"Nombre d'images avec logos dans le répertoire d'entraînement : {len(train_generator_augmented.filenames)}")
print(f"Nombre d'images sans logos dans le répertoire de validation : {len(validation_generator.filenames)}")


# Utiliser le générateur d'images augmentées pour l'entraînement
train_generator_augmented = train_datagen_augmented.flow_from_directory(
    with_logo_dir,
    target_size=(img_height, img_width),
    batch_size=batch_size,
    class_mode='binary'
)

# Construire le modèle CNN avec des modifications
model = models.Sequential()
model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(img_height, img_width, 3)))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))

# Ajouter des couches supplémentaires
model.add(layers.Conv2D(128, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Flatten())

# Ajouter des couches denses supplémentaires avec Dropout
model.add(layers.Dense(256, activation='relu'))
model.add(layers.Dropout(0.5))
model.add(layers.Dense(128, activation='relu'))

# Couche de sortie
model.add(layers.Dense(1, activation='sigmoid'))

# Compiler le modèle
model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])

# Entraîner le modèle
model.fit(train_generator_augmented, epochs=num_epochs, validation_data=validation_generator)

# Nouvelle méthode (utilise le format natif de Keras)
model.save('mon_model.h5')

# Afficher un message indiquant que l'entraînement et la sauvegarde sont terminés
print("Entraînement terminé, modèle sauvegardé sous 'mon_model.h5'")
