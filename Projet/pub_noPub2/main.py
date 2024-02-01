import os
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense

# Définition des chemins des dossiers
dossier_racine = r'C:\Users\ludovic.souquet\Documents\GitHub\ludovic.souquet\Projet\pub_noPub2'
dossier_datasets = os.path.join(dossier_racine, 'datasets')
dossier_augmente = os.path.join(dossier_datasets, 'augmente')

# Paramètres pour la data augmentation
batch_size = 32
epochs = 10
img_height, img_width = 100, 100

# Utilisation de l'ImageDataGenerator pour la data augmentation
datagen = ImageDataGenerator(
    rescale=1./255,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    validation_split=0.2
)

# Chargement des images depuis les dossiers avec data augmentation
train_generator = datagen.flow_from_directory(
    dossier_augmente,
    target_size=(img_height, img_width),
    batch_size=batch_size,
    class_mode='binary',
    subset='training'
)

validation_generator = datagen.flow_from_directory(
    dossier_augmente,
    target_size=(img_height, img_width),
    batch_size=batch_size,
    class_mode='binary',
    subset='validation'
)

# Création du modèle CNN
model = Sequential()
model.add(Conv2D(32, (3, 3), input_shape=(img_height, img_width, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(128, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dense(1, activation='sigmoid'))

# Compilation du modèle
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Entraînement du modèle
model.fit(train_generator, epochs=epochs, validation_data=validation_generator)

# Sauvegarde du modèle
model.save('modele_logo.h5')