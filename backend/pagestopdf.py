import os
from PIL import Image

def convert_to_pdf():
    folder_path = "comic_pages"  # Path to your folder
    images = sorted([f for f in os.listdir(folder_path) if f.endswith(".png")])  # Get all PNG files in order

    if not images:
        print("No images found!")
        return

    # Open the first image
    first_image = Image.open(os.path.join(folder_path, images[0])).convert('RGB')
    
    # Open the rest of the images
    image_list = [Image.open(os.path.join(folder_path, img)).convert('RGB') for img in images[1:]]

    # Save as PDF
    first_image.save("dummy.pdf", save_all=True, append_images=image_list)
    print(f"PDF created with {len(images)} pages!")

# convert_to_pdf()
