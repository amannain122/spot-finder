import os
import Augmentor
from PIL import Image
import aws
import shutil

# Source and output directories
source_dir = 'D:\\Python\\scraped_images'
output_dir = 'D:\\Python\\augmented_images'

def convert_image_mode(image):
    if image.mode != 'RGB':
        return image.convert('RGB')
    return image

# Function to perform image augmentation and save augmented images
def augment_and_save_images(num_augmentations=3):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    temp_dir = os.path.join(output_dir, "temp")
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    # Keep track of the number of augmentations
    augmentation_count = 1

    # Iterate through all images in the source directory
    for image_name in os.listdir(source_dir):
        image_path = os.path.join(source_dir, image_name)
        if os.path.isfile(image_path):
            try:
                # Copy image to temporary directory
                temp_image_path = os.path.join(temp_dir, image_name)
                shutil.copy(image_path, temp_image_path)

                # Create an Augmentor Pipeline for the temporary directory
                p = Augmentor.Pipeline(source_directory=temp_dir, output_directory=output_dir)

                # Define augmentation operations
                p.rotate(probability=0.7, max_left_rotation=10, max_right_rotation=10)
                p.zoom_random(probability=0.5, percentage_area=0.8)
                p.flip_left_right(probability=0.5)

                # Augment and save images
                p.sample(num_augmentations, multi_threaded=False)

                # Rename augmented images to avoid overwriting and to follow naming convention
                for aug_image in os.listdir(output_dir):
                    aug_image_path = os.path.join(output_dir, aug_image)
                    if aug_image.startswith(os.path.splitext(image_name)[0]):
                        new_image_name = f"{os.path.splitext(image_name)[0]}_aug_{augmentation_count}.jpg"
                        
                        # Open the image and convert its mode if necessary
                        with Image.open(aug_image_path) as img:
                            img = convert_image_mode(img)
                            img.save(os.path.join(output_dir, new_image_name), 'JPEG')
                        
                        os.remove(aug_image_path)  # Remove the original augmented image
                        augmentation_count += 1
            except Exception as e:
                print(f"Error processing {image_name}: {e}")

            # Clean up temporary directory
            shutil.rmtree(temp_dir)
            os.makedirs(temp_dir)
            
# Function to upload images to S3
def upload_images_to_s3():
    # # Upload original images
    # for image_name in os.listdir(source_dir):
    #     image_path = os.path.join(source_dir, image_name)
    #     if os.path.isfile(image_path):
    #         try:
    #             aws.upload_to_s3(image_path)
    #         except Exception as e:
    #             print(f"Error uploading {image_path} to S3: {str(e)}")

    # Upload augmented images
    for image_name in os.listdir(output_dir):
        image_path = os.path.join(output_dir, image_name)
        if os.path.isfile(image_path):
            try:
                aws.upload_to_s3(image_path)
            except Exception as e:
                print(f"Error uploading {image_path} to S3: {str(e)}")


# Main function to execute the workflow
def main():
    # augment_and_save_images()
    #upload_images_to_s3()

if __name__ == "__main__":
    main()
