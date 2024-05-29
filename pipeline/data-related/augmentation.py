import os
import Augmentor
import aws

# Source directory containing original images
source_dir = 'D:\Python\scraped_images'

# Function to perform image augmentation
def augment_images():
    # Create an Augmentor Pipeline
    p = Augmentor.Pipeline(source_directory=source_dir, output_directory=os.path.join(source_dir, "output"))

    # Define augmentation operations
    p.rotate(probability=0.7, max_left_rotation=10, max_right_rotation=10)
    p.zoom_random(probability=0.5, percentage_area=0.8)
    p.flip_left_right(probability=0.5)

    # Sample augmented versions for each image
    p.sample(5)  # You can adjust the number of samples here

    # Upload original and augmented images to S3
    for image_path in os.listdir(os.path.join(source_dir, "output")):
        # Skip non-image files
        if not image_path.endswith(('.jpg', '.jpeg', '.png')):
            continue
        
        aws.upload_to_s3(os.path.join(source_dir, "output", image_path))

# Main function to execute the workflow
def main():
    augment_images()

if __name__ == "__main__":
    main()
