import os
import json

def get_image_files(directory):
    # List of image extensions to look for
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff'}
    
    # List to store image filenames
    image_files = []
    
    # Iterate over files in the specified directory
    for filename in os.listdir(directory):
        full_path = os.path.join(directory, filename)
        if os.path.isfile(full_path):
            # Check file extension
            if any(filename.lower().endswith(ext) for ext in image_extensions):
                image_files.append(filename)
    
    return image_files

def write_json(data, filename):
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)

def main():
    # Absolute path to the images directory
    images_directory = r'C:\Users\Daniel\Documents\GitHub\rage65.github.io\photogrophy\images'
    
    # Path to the JSON file
    json_file_path = r'C:\Users\Daniel\Documents\GitHub\rage65.github.io\photogrophy\images_list.json'
    
    # Get list of image files
    image_files = get_image_files(images_directory)
    
    # Write the list to a JSON file
    write_json(image_files, json_file_path)
    
    print(f'Updated {json_file_path} with {len(image_files)} image filenames.')

if __name__ == "__main__":
    main()
