import cv2
import os

def preprocess_images(input_dir, output_dir, target_size=(100, 100)):
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Iterate over each file in the input directory
    for filename in os.listdir(input_dir):
        # Load the image
        image_path = os.path.join(input_dir, filename)
        image = cv2.imread(image_path)

        if image is not None:
            # Convert the image to grayscale
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # Resize the image to the target size
            resized_image = cv2.resize(gray_image, target_size)

            # Save the preprocessed image to the output directory
            output_path = os.path.join(output_dir, filename)
            cv2.imwrite(output_path, resized_image)

            print(f'Preprocessed image saved: {output_path}')

# Example usage:
input_directory = 'images'
output_directory = 'preprocessed_images'
preprocess_images(input_directory, output_directory)
