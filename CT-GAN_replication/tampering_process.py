import os
import random
import numpy as np
import csv
from procedures.attack_pipeline import *
from skimage.filters import threshold_otsu

# Initialize the pipeline
injector = scan_manipulator()

def select_random_patient(base_path, patient_prefix="1.3."):
    patients = [f for f in os.listdir(base_path) if f.startswith(patient_prefix) and f.endswith('.mhd')]
    if not patients:
        raise ValueError("No .mhd files found with the given prefix!")
    
    selected_patient = random.choice(patients)
    patient_path = os.path.join(base_path, selected_patient)
    print(f"Selected patient: {selected_patient}")
    return patient_path

def generate_random_coordinate(scan_shape_zyx):
    size_z, size_y, size_x = scan_shape_zyx
    
    # Range for z
    middle_z = int(0.5 * size_z)
    tolerance_z = int(0.007 * size_z)
    z_min = middle_z - tolerance_z
    z_max = middle_z + tolerance_z
    
    # Range for y
    y_min_range = 180
    y_max_range = 320
    
    # Ranges for x
    x_ranges = [
        (100, 175),
        (325, 400)
    ]
    
    selected_x_range = random.choice(x_ranges)
    x_min, x_max = selected_x_range
    
    z = random.randint(z_min, z_max)
    y = random.randint(y_min_range, y_max_range)
    x = random.randint(x_min, x_max)
    print(z, y, x)
    return [z, y, x]

def get_next_available_name(save_path, start=3000):
    num = start
    while True:
        potential_name = f"{num}"
        if not os.path.exists(os.path.join(save_path, potential_name)):
            return potential_name
        num += 1

def append_to_csv(log_file_path, data, fieldnames):
    file_exists = os.path.isfile(log_file_path)
    with open(log_file_path, mode='a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)

def inject_random_nodules(base_path, save_base_path, patient_prefix="1.3."):
    """
    Randomly selects a patient. If the found coordinate is not black,
    restarts from the beginning, selects a new patient, and tries again.
    """
    while True:
        # Select a random patient
        patient_path = select_random_patient(base_path, patient_prefix)
        
        print('Starting scan manipulation...')
        
        
        # Load the target scan
        injector.load_target_scan(patient_path)
        
        # Get the shape of the scan (z, y, x)
        scan_shape = injector.scan.shape
        
        # Generate a random coordinate
        z, y, x = generate_random_coordinate(scan_shape)
        
        # Apply Otsu on the corresponding slice
        slice_z = injector.scan[z]
        otsu_thresh = threshold_otsu(slice_z)
        otsu_mask = slice_z > otsu_thresh
        
        # Check if coordinate is black
        if not otsu_mask[y, x]:
            # If black, exit the while loop and inject
            vox_coord1 = [z, y, x]
            break
        else:
            # If not black, go back to the beginning of the loop,
            # select a new patient, and try again
            print("Coordinate is not black, selecting a new patient...")
            # The loop continues and jumps back to patient_path selection
    
    # If a suitable coordinate is found, inject the nodule
    injector.tamper(np.array(vox_coord1), action='inject', isVox=True)
    
    # Determine the next available folder name
    new_folder_name = get_next_available_name(save_base_path, start=3000)
    save_path = os.path.join(save_base_path, new_folder_name)
    
    # Create the new folder
    os.makedirs(save_path, exist_ok=True)
    
    # Save the tampered scan
    injector.save_tampered_scan(save_path, output_type='dicom') 
    print(f'Manipulation complete and scan saved in {save_path}.')
    
    # Update the CSV log
    log_file_path = os.path.join(save_base_path, 'log.csv')
    data = {
        'ID': new_folder_name,
        'patient_path': patient_path,
        'vox_coord1': vox_coord1
    }
    fieldnames = ['ID', 'patient_path', 'vox_coord1']
    append_to_csv(log_file_path, data, fieldnames)
    print(f'Data saved in {log_file_path}.')

if __name__ == "__main__":
    base_path = 'data/convertible/'
    save_base_path = 'data/tampered_scans/'
    
    os.makedirs(save_base_path, exist_ok=True)
    
    existing_files = [f for f in os.listdir(save_base_path) if f.isdigit() and int(f) >= 3000]
    num_existing_files = len(existing_files)
    
    total_files_needed = 1100
    num_files_to_generate = total_files_needed - num_existing_files
    
    print(f"Existing files: {num_existing_files}. {num_files_to_generate} files still need to be generated.")
    
    for _ in range(num_files_to_generate):
        inject_random_nodules(base_path, save_base_path)
