import os
import zipfile
import rarfile  # Required for .cbr files
from PIL import Image
import fitz  # PyMuPDF for splitting PDFs
import math


# Function: Convert CBZ to PDF
def cbz_to_pdf(cbz_file, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    base_name = os.path.splitext(os.path.basename(cbz_file))[0]
    pdf_path = os.path.join(output_folder, base_name + '.pdf')

    with zipfile.ZipFile(cbz_file, 'r') as cbz:
        image_files = [f for f in cbz.namelist() if f.lower().endswith(('png', 'jpg', 'jpeg'))]
        image_files.sort()

        images = []
        print(f"Now creating: {cbz_file}")
        for image_file in image_files:
            with cbz.open(image_file) as img_file:
                image = Image.open(img_file)
                image = image.convert('RGB')
                images.append(image)

        if images:
            images[0].save(pdf_path, save_all=True, append_images=images[1:])
            print(f"Created PDF: {pdf_path}")
        else:
            print(f"No images found in {cbz_file}")


# Function: Convert CBR to PDF
def cbr_to_pdf(cbr_file, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    base_name = os.path.splitext(os.path.basename(cbr_file))[0]
    pdf_path = os.path.join(output_folder, base_name + '.pdf')

    with rarfile.RarFile(cbr_file, 'r') as cbr:
        image_files = [f for f in cbr.namelist() if f.lower().endswith(('png', 'jpg', 'jpeg'))]
        image_files.sort()

        images = []
        print(f"Now creating: {cbr_file}")
        for image_file in image_files:
            with cbr.open(image_file) as img_file:
                image = Image.open(img_file)
                image = image.convert('RGB')
                images.append(image)

        if images:
            images[0].save(pdf_path, save_all=True, append_images=images[1:])
            print(f"Created PDF: {pdf_path}")
        else:
            print(f"No images found in {cbr_file}")


# Function: Convert all CBZ/CBR files to PDFs in a folder
def convert_all_cbz_cbr_to_pdf(folder_path, output_folder):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith('.cbz'):
                cbz_file = os.path.join(root, file)
                cbz_to_pdf(cbz_file, output_folder)
            elif file.lower().endswith('.cbr'):
                cbr_file = os.path.join(root, file)
                cbr_to_pdf(cbr_file, output_folder)


# Function: Split oversized PDFs
def split_pdf(file_path, output_folder, max_size_mb=200):
    if max_size_mb <= 0:
        raise ValueError("max_size_mb must be greater than 0")

    max_size_bytes = max_size_mb * 1024 * 1024
    original_size = os.path.getsize(file_path)

    if original_size <= max_size_bytes:
        print(f"{file_path} is already within the size limit ({max_size_mb} MB).")
        return

    pdf_document = fitz.open(file_path)
    total_pages = pdf_document.page_count
    num_parts = math.ceil(original_size / max_size_bytes)
    pages_per_part = math.ceil(total_pages / num_parts)

    part_number = 1
    start_page = 0

    while start_page < total_pages:
        end_page = min(start_page + pages_per_part, total_pages)

        while True:
            new_pdf = fitz.open()
            for page_num in range(start_page, end_page):
                new_pdf.insert_pdf(pdf_document, from_page=page_num, to_page=page_num)

            part_file_name = f"{os.path.splitext(os.path.basename(file_path))[0]}-{part_number}.pdf"
            part_file_path = os.path.join(output_folder, part_file_name)
            new_pdf.save(part_file_path)
            new_pdf.close()

            part_size = os.path.getsize(part_file_path)
            if part_size > max_size_bytes and end_page - start_page > 1:
                end_page -= 1
                os.remove(part_file_path)
            else:
                print(f"Saved part {part_number} as '{part_file_path}' ({part_size / (1024 * 1024):.2f} MB)")
                part_number += 1
                start_page = end_page
                break

    pdf_document.close()
    print(f"Splitting complete for '{file_path}'.")


# Function: Process all PDFs in a folder for splitting
def process_folder(folder_path, output_folder, max_size_mb=200):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".pdf"):
            file_path = os.path.join(folder_path, filename)
            split_pdf(file_path, output_folder, max_size_mb)


# Main execution: Conversion and splitting
if __name__ == "__main__":
    # Folder paths
    input_folder = 'Ultra Maniac'  # Change as needed
    output_folder = input_folder

    # Convert all CBZ/CBR to PDFs
    print("Starting CBZ/CBR to PDF conversion...")
    convert_all_cbz_cbr_to_pdf(input_folder, output_folder)

    # Process PDFs for splitting if they exceed size limits
    print("\nStarting PDF splitting for oversized files...")
    process_folder(input_folder, output_folder, max_size_mb=200)
