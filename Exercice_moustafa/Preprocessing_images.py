import os
import cv2
import numpy as np
from keras.preprocessing.image import ImageDataGenerator

def is_rgb(image_path):
    
    img = cv2.imread(image_path)

    
    return len(img.shape) == 3 and img.shape[2] == 3

def resize_and_save(input_folder, output_folder, target_size=(256, 256)):
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    
    files = os.listdir(input_folder)

    for file in files:
        
        image_path = os.path.join(input_folder, file)

        if os.path.isfile(image_path) and image_path.lower().endswith(('.png', '.PNG')):
            if is_rgb(image_path):
                
                img = cv2.imread(image_path)
                
                img_resized = cv2.resize(img, target_size)
                
                output_path = os.path.join(output_folder, file)
                
                cv2.imwrite(output_path, img_resized)

def augment_and_save_images(input_folder, output_folder):
    
    resized_folder = os.path.join(output_folder, 'resized_images')
    resize_and_save(input_folder, resized_folder, target_size=(256, 256))

    
    datagen = ImageDataGenerator(
        rotation_range=40,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest'
    )

    
    files = os.listdir(resized_folder)

    for file in files:
        
        image_path = os.path.join(resized_folder, file)

        if os.path.isfile(image_path) and image_path.lower().endswith(('.png', '.PNG')):
            
            img = cv2.imread(image_path)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # OpenCV reads images in BGR, convert to RGB for Keras

            
            img = np.expand_dims(img, axis=0)

            
            it = datagen.flow(img, batch_size=1, save_to_dir=output_folder, save_prefix='aug', save_format='png')

           
            for _ in range(5):  
                batch = it.next()

if __name__ == "__main__":
    input_folder = "C:/Users/moust/OneDrive/Bureau/Scrapping_logo/pythonP_roject/image_folder/"
    output_folder = "C:/Users/moust/OneDrive/Bureau/Scrapping_logo/pythonP_roject/saved_images/"

    augment_and_save_images(input_folder, output_folder)