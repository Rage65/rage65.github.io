import os
import json

def change_extensions_and_collect(directory):
    # List of image extensions to look for
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff'}
    
    # List to store image filenames
    image_files = []
    changed_files = []

    # Iterate over files in the specified directory
    for filename in os.listdir(directory):
        full_path = os.path.join(directory, filename)
        if os.path.isfile(full_path):
            # Check file extension
            if any(filename.lower().endswith(ext) for ext in image_extensions):
                # Collect original filenames
                image_files.append(filename)
                
                # If file extension is .jpg, change to .JPEG
                if filename.lower().endswith('.jpg'):
                    new_filename = filename[:-4] + '.JPEG'
                    new_full_path = os.path.join(directory, new_filename)
                    
                    # Rename the file
                    os.rename(full_path, new_full_path)
                    
                    # Collect the new filename
                    changed_files.append(new_filename)
                else:
                    # Collect filenames that were not changed
                    changed_files.append(filename)

    return image_files, changed_files

def write_json(data, filename):
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)

def main():
    # Absolute path to the images directory
    images_directory = r'C:\Users\Daniel\Documents\GitHub\rage65.github.io\photogrophy\images'
    
    # Path to the JSON file
    json_file_path = r'C:\Users\Daniel\Documents\GitHub\rage65.github.io\photogrophy\images_list.json'
    
    # Change file extensions and get list of image files
    original_files, updated_files = change_extensions_and_collect(images_directory)
    
    # Write the list of updated filenames to a JSON file
    write_json(updated_files, json_file_path)
    
    print(f'Updated {json_file_path} with {len(updated_files)} image filenames.')
    print(f'Original filenames: {original_files}')
    print(f'Renamed files: {updated_files}')

if __name__ == "__main__":
    main()
