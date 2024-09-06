import os
import shutil

# Define the directory paths
downloads_folder = "c:/Users/Shaheem Mushtaq/Downloads"  # Replace with the actual path to your Downloads folder
pdfs_folder = os.path.join(downloads_folder, "PDFs")

# Create the PDFs directory if it doesn't exist
if not os.path.exists(pdfs_folder):
    os.makedirs(pdfs_folder)

# Move .pdf files to the PDFs directory
for file_name in os.listdir(downloads_folder):
    file_path = os.path.join(downloads_folder, file_name)
    if os.path.isfile(file_path) and file_name.lower().endswith('.pdf'):
        shutil.move(file_path, os.path.join(pdfs_folder, file_name))

print("PDF files have been moved to the PDFs directory.")
