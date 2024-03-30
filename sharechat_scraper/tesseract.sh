#!/bin/bash

# Define input and output directories
input_dir="data"
output_dir="tesseract"

# Loop through each folder in the input directory
for folder in "$input_dir"/*; do
    if [ -d "$folder" ]; then
        folder_name=$(basename "$folder")
        output_folder="$output_dir/$folder_name"

        # Create output folder if it doesn't exist
        mkdir -p "$output_folder"

        # Loop through each image file in the folder
        for image_file in "$folder"/*.jpg; do
            if [ -f "$image_file" ]; then
                file_name=$(basename -s .jpg "$image_file")
                output_file="$output_folder/$file_name.txt"

                # Run tesseract command
                tesseract "$image_file" "$output_folder/$file_name" -l hin Devanagari eng > /dev/null 2>&1

                # Check if the output file exists
                if [ -f "$output_folder/$file_name.txt" ]; then
                    echo "Output saved: $output_file"
                else
                    echo "Error: Failed to save output for $image_file"
                fi
            fi
        done
    fi
done
