from tensorflow_model_optimization.sparsity.keras import prune_low_magnitude
from tensorflow_model_optimization.sparsity.keras import strip_pruning
from tensorflow_model_optimization.sparsity.keras import ConstantSparsity, PolynomialDecay

def train_model():
    # Définir la taille cible des images
    target_size = (100, 100)

    # Charger et redimensionner les images depuis les dossiers "pub" et "nopub"
    pub_images = load_and_resize_images_from_folder(r"datasets\pub_no_pubV3\logo-tv", target_size)
    nopub_images = load_and_resize_images_from_folder(r"datasets\pub_no_pubV3\pas-logo-tv", target_size)

    # Créer les étiquettes correspondantes (1 pour "pub" et 0 pour "nopub")
    pub_labels = np.ones(len(pub_images))
    nopub_labels = np.zeros(len(nopub_images))

    # Concaténer les images et les étiquettes
    images = np.concatenate((pub_images, nopub_images))
    labels = np.concatenate((pub_labels, nopub_labels))

    # Diviser les données en ensembles d'apprentissage et de test
    X_train, X_test, y_train, y_test = train_test_split(images, labels, test_size=0.3, random_state=42)

    # Définir les paramètres de pruning
    pruning_params = {
        'pruning_schedule': PolynomialDecay(
            initial_sparsity=0.0,
            final_sparsity=0.5,
            begin_step=0,
            end_step=np.ceil(len(X_train) / 32).astype(np.int32) * 10  # Nombre d'époques * batches
        )
    }

    # Créer un modèle CNN Keras avec couche de convolution supplémentaire, pooling et dropout
    model_cnn = keras.Sequential([
        prune_low_magnitude(keras.layers.Conv2D(64, (3, 3), activation='relu', input_shape=(100, 100, 3)), **pruning_params),
        keras.layers.MaxPooling2D(2, 2),
        prune_low_magnitude(keras.layers.Conv2D(128, (3, 3), activation='relu'), **pruning_params),
        keras.layers.MaxPooling2D(2, 2),
        prune_low_magnitude(keras.layers.Conv2D(256, (3, 3), activation='relu'), **pruning_params),
        keras.layers.MaxPooling2D(2, 2),
        keras.layers.Flatten(),
        keras.layers.Dropout(0.3),
        prune_low_magnitude(keras.layers.Dense(128, activation='relu'), **pruning_params),
        prune_low_magnitude(keras.layers.Dense(64, activation='relu'), **pruning_params),
        keras.layers.Dense(2, activation='softmax')  # Nombre de neurones = nombre de classes
    ])

    # Compiler le modèle CNN Keras
    model_cnn.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    # Définir un callback pour enregistrer le modèle avec la meilleure précision sur les données de validation
    model_checkpoint = ModelCheckpoint('test_5.keras', save_best_only=True, monitor='val_accuracy', mode='max', verbose=1)

    # Définir un callback pour arrêter l'entraînement si la précision ne s'améliore pas pendant un certain nombre d'époques
    early_stopping = EarlyStopping(monitor='val_accuracy', patience=5, mode='max', verbose=1)

    # Entraîner le modèle CNN Keras avec les données d'entraînement
    model_cnn.fit(X_train, y_train, epochs=50, validation_data=(X_test, y_test), callbacks=[model_checkpoint, early_stopping])

    # Évaluer le modèle CNN Keras sur les données de test
    accuracy = model_cnn.evaluate(X_test, y_test)[1]
    print(f"Précision du modèle CNN Keras sur les données de test: {accuracy}")

    # Retirer les masques de pruning pour optimiser le modèle final
    stripped_model = strip_pruning(model_cnn)

    # Sauvegarder le modèle final après stripping
    stripped_model.save('test_5_pruned.keras')

    return stripped_model
