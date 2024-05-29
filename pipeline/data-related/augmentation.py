import os
import Augmentor
import aws

# Source directory containing original images
source_dir = 'downloaded_images'

# Function to perform image augmentation
def augment_images():
    # Create an Augmentor Pipeline
    p = Augmentor.Pipeline(source_directory=source_dir)

    # Define augmentation operations
    p.rotate(probability=0.7, max_left_rotation=10, max_right_rotation=10)
    p.zoom_random(probability=0.5, percentage_area=0.8)
    p.flip_left_right(probability=0.5)

    # Sample multiple images from the pipeline and generate multiple augmented versions
    for image_path in os.listdir(source_dir):
        # Skip non-image files
        if not image_path.endswith(('.jpg', '.jpeg', '.png')):
            continue
        
        # Sample 10 augmented versions for each image
        p.sample(5)

        # Upload original and augmented images to S3
        aws.upload_to_s3(os.path.join(source_dir, image_path))
        aws.upload_to_s3(os.path.join(source_dir, "output", image_path))

# Main function to execute the workflow
def main():
    augment_images()

if __name__ == "__main__":
    main()
