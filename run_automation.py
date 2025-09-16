import os
import re
import pandas as pd
from google.cloud import vision
import shutil

INPUT_CSV_FILE = "products.csv"
OUTPUT_CSV_FILE = "products_updated.csv"
SOURCE_FOLDER = "products"
DESTINATION_FOLDER = "uploaded_products"
# Google Credentials file for Vision API
SERVICE_ACCOUNT_FILE = "service-account-key.json"

def clean_text_for_filename(text):
    """Cleans text to be a valid, URL-friendly filename slug."""
    text = text.replace('\n', ' ').replace('\t', ' ')
    text = text.lower()
    text = text.replace(' ', '-')
    text = re.sub(r'[^a-z0-9-]', '', text)
    # Refine the slug by removing common unhelpful words
    common_words = ['poster', 'of', 'the', 'and', 'art', 'print']
    words = text.split('-')
    words = [word for word in words if word not in common_words]
    text = '-'.join(words)
    text = text.strip('-')
    return text

def main():
    """Main function to run the automation workflow with image recognition."""
    print("--- Starting Poster Automation (Image Recognition Mode) ---")

    # Authenticate with Google Vision API
    try:
        vision_client = vision.ImageAnnotatorClient.from_service_account_file(SERVICE_ACCOUNT_FILE)
        print("Successfully authenticated with Google Vision API.")
    except Exception as e:
        print(f"Error authenticating with Google Vision: {e}")
        print("Please ensure your 'service-account-key.json' file is correct.")
        return

    if not os.path.exists(INPUT_CSV_FILE):
        print(f"Error: Input file '{INPUT_CSV_FILE}' not found.")
        return

    new_slugs = []
    image_files = sorted([f for f in os.listdir(SOURCE_FOLDER) if f.lower().endswith(('.png', '.jpg', '.jpeg'))])
    
    if not image_files:
        print("No image files found in the 'products' folder. Exiting.")
        return

    for filename in image_files:
        source_path = os.path.join(SOURCE_FOLDER, filename)
        
        print(f"\nProcessing '{filename}'...")
        
        try:
            with open(source_path, 'rb') as image_file:
                content = image_file.read()
            image = vision.Image(content=content)
            
            
            response = vision_client.web_detection(image=image)
            annotations = response.web_detection

            
            if annotations.best_guess_labels:
                detected_text = annotations.best_guess_labels[0].label
                print(f"  > AI's best guess: '{detected_text}'")

            
            elif annotations.web_entities:
                detected_text = annotations.web_entities[0].description
                print(f"  > AI found entity: '{detected_text}'")

            else:
                print(f"  > Could not recognize the image content. Skipping.")
                continue

            slug = clean_text_for_filename(detected_text)
            if not slug:
                slug = f"untitled-image-{len(new_slugs) + 1}"
                print("  > Could not generate a valid slug. Using default.")

            print(f"  > Generated slug: '{slug}'")
            new_slugs.append(slug)
            
            new_filename = f"{slug}{os.path.splitext(filename)[1]}"
            destination_path = os.path.join(DESTINATION_FOLDER, new_filename)
            
            shutil.copy(source_path, destination_path)
            print(f"  > Renamed and saved to '{destination_path}'")
                
        except Exception as e:
            # Check for billing error specifically
            if 'billing' in str(e).lower():
                 print(f"  > CRITICAL ERROR: Billing is not enabled for your Google Cloud project.")
                 print(f"  > Please visit the link in the error message to enable it, wait a few minutes, then retry.")
                 return 
            else:
                print(f"  > An error occurred processing '{filename}': {e}")


    # --- Update the CSV file ---
    try:
        print(f"\nUpdating CSV file: '{INPUT_CSV_FILE}'...")
        df = pd.read_csv(INPUT_CSV_FILE)
        
        num_rows_to_update = min(len(new_slugs), len(df))
        
        
        df.loc[:num_rows_to_update-1, 'Slug'] = new_slugs[:num_rows_to_update]
        
        
        proper_names = [name.replace('-', ' ').title() for name in new_slugs]
        df.loc[:num_rows_to_update-1, 'Name'] = proper_names[:num_rows_to_update]

        df.to_csv(OUTPUT_CSV_FILE, index=False)
        print(f"Successfully created updated file: '{OUTPUT_CSV_FILE}'")

    except Exception as e:
        print(f"An error occurred while updating the CSV file: {e}")

    print("\n--- Automation Complete ---")

if __name__ == '__main__':
    main()