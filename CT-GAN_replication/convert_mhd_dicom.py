import os
import shutil

def organize_files_in_convertible(main_folder):
    # Path for the "convertible" subfolder
    convertible_folder = os.path.join(main_folder, "convertible")
    os.makedirs(convertible_folder, exist_ok=True)
    
    # Search all files in the main folder
    files_in_main_folder = os.listdir(main_folder)
    mhd_files = [f for f in files_in_main_folder if f.endswith(".mhd")]
    raw_files = [f for f in files_in_main_folder if f.endswith(".raw")]

    # Set of RAW file basenames (without extension)
    raw_file_basenames = {os.path.splitext(f)[0] for f in raw_files}

    for mhd_file in mhd_files:
        # Basename without extension
        basename = os.path.splitext(mhd_file)[0]
        if basename in raw_file_basenames:
            # Create paths
            mhd_path = os.path.join(main_folder, mhd_file)
            raw_path = os.path.join(main_folder, f"{basename}.raw")
            
            # Move files to the "convertible" folder
            shutil.move(mhd_path, os.path.join(convertible_folder, mhd_file))
            shutil.move(raw_path, os.path.join(convertible_folder, f"{basename}.raw"))
            print(f"Moved {mhd_file} and {basename}.raw to {convertible_folder}")

    print("Organizing completed.")

# Specify the main folder (replace the path with the desired folder)
main_folder_path = "data/healthy_scans/"
organize_files_in_convertible(main_folder_path)


########################################

import os
import random
from procedures.attack_pipeline import scan_manipulator

def select_random_patient(base_path, patient_prefix="1.3.6.1.4.1.14519.5.2.1.6279."):  
    # Select only files with the given prefix and the ".mhd" extension
    patients = [f for f in os.listdir(base_path) if f.startswith(patient_prefix) and f.endswith(".mhd")]
    if not patients:
        raise ValueError("No .mhd patients found with the given prefix!")
    return patients

def get_next_available_name(save_path, start=2000):
    num = start
    while True:
        potential_name = f"{num}"
        if not os.path.exists(os.path.join(save_path, potential_name)):
            return potential_name
        num += 1

# Define main paths and parameters
base_path = "data/healthy_scans/convertible"
save_path = "data/converted_scans/"  # Corrected Windows path

try:
    # Get all patients from the directory
    all_patients = select_random_patient(base_path, patient_prefix="1.3.6.1.4.1.14519.5.2.1.6279.")
    random.shuffle(all_patients)  # Optional: Randomize the order
    
    # Initialize manipulator
    injector = scan_manipulator()
    
    # Process all patients sequentially
    for patient in all_patients:
        patient_path = os.path.join(base_path, patient)
        print(f"Processing patient: {patient}")
        
        # Load and manipulate scan
        injector.load_target_scan(patient_path)
        next_name = get_next_available_name(save_path)
        injector.save_tampered_scan(os.path.join(save_path, next_name), output_type='dicom')
        print(f"Converted scan saved to: {os.path.join(save_path, next_name)}")
    
    print("All patients have been successfully processed.")
except Exception as e:
    print(f"Error: {e}")
