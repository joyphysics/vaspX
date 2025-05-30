import os
import shutil
import subprocess
import time

# Step 1: Check if necessary files exist in the current directory
required_files = ['INCAR', 'KPOINTS', 'POSCAR', 'POTCAR', 'job.sh']
for filename in required_files:
    if not os.path.isfile(filename):
        print("Error: {0} not found in the current directory.".format(filename))
        exit(1)

# Step 1.5: Ensure that NSW = 0, ISIF = 2, IBRION = -1 in the INCAR file

# Read the content of the INCAR file
with open('INCAR', 'r') as incar_file:
    incar_content = incar_file.readlines()

# Update the required values in the INCAR file
for i, line in enumerate(incar_content):
    if 'NSW' in line:
        incar_content[i] = '  NSW       = 0\n'
    elif 'ISIF' in line:
        incar_content[i] = '  ISIF      = 2\n'
    elif 'IBRION' in line:
        incar_content[i] = '  IBRION    = -1\n'

# Write the updated content back to the INCAR file
with open('INCAR', 'w') as incar_file:
    incar_file.writelines(incar_content)

# Step 2: Ask the user for initial and final ENCUT values
initial_encut = int(raw_input("Enter the initial ENCUT value (multiple of 25): "))
final_encut = int(raw_input("Enter the final ENCUT value (multiple of 25): "))

# Validate the ENCUT values
if initial_encut % 25 != 0 or final_encut % 25 != 0 or initial_encut >= final_encut:
    print("Error: ENCUT values must be multiples of 25 and initial ENCUT should be less than final ENCUT.")
    exit(1)

# Create the folders and the summary.dat file
summary_file = open('summary.dat', 'w')
summary_file.write("#ENCUT    ENERGY\n")

# Step 3: Create folders and copy files
encut_values = range(initial_encut, final_encut + 1, 25)
for encut in encut_values:
    folder_name = 'ENCUT{0}'.format(encut)
    os.mkdir(folder_name)
    
    # Copy necessary files into each new folder
    for filename in required_files:
        shutil.copy(filename, folder_name)

    # Step 4: Modify the ENCUT value in the INCAR file for each folder
    incar_path = os.path.join(folder_name, 'INCAR')
    with open(incar_path, 'r') as incar_file:
        incar_content = incar_file.readlines()
    
    for i, line in enumerate(incar_content):
        if 'ENCUT' in line:
            incar_content[i] = '  ENCUT     = {0}\n'.format(encut)
            break

    # Write the updated content back to the INCAR file
    with open(incar_path, 'w') as incar_file:
        incar_file.writelines(incar_content)

# Step 5: Ask user if they want to perform the VASP run
print("Please check the INCAR file befor submitting the jobs ... ")
perform_vasp_run = raw_input("Do you want to perform the VASP run? (y/n): ").strip().lower()
if perform_vasp_run != 'y':
    print("Exiting script as per user request.")
    exit(0)

# Step 5.1: Perform the VASP run for each folder and collect energy values
for encut in encut_values:
    folder_name = 'ENCUT{0}'.format(encut)
    os.chdir(folder_name)
    
    # Submit VASP job
    print("Submitting job in: {0}".format(folder_name))
    subprocess.call(['qsub', 'job.sh'])
    
    # Wait for the OUTCAR file to be created and VASP job to complete
    while not os.path.exists('OUTCAR'):
        time.sleep(5)
    
    # Check for completion of the VASP job
    vasp_finished = False
    while not vasp_finished:
        with open('OUTCAR', 'r') as outcar_file:
            for line in outcar_file:
                if 'Voluntary context switches:' in line:
                    vasp_finished = True
                    break
        if not vasp_finished:
            print("Waiting for VASP run to finish in folder: {0}".format(folder_name))
            time.sleep(30)
    
    # Extract energy value (TOTEN) from OUTCAR file
    energy_value = None
    with open('OUTCAR', 'r') as outcar_file:
        for line in outcar_file:
            if 'TOTEN' in line and 'free  energy' in line:
                energy_value = float(line.split('=')[-1].split()[0].strip())
                break
    
    # Validate that the required energy value was found
    if energy_value is None:
        print("Error: Could not find energy data in OUTCAR in folder: {0}".format(folder_name))
        exit(1)

    # Write ENCUT value and energy to summary.dat
    with open('../summary.dat', 'a') as summary_file:
        summary_file.write('{0}    {1:.8f}\n'.format(encut, energy_value))
    
    os.chdir('..')

print("ENCUT convergence run completed. Check summary.dat for the results.")

# Step 6: Ask user if they want to delete all VASP runs
delete_runs = raw_input("Do you want to delete all VASP runs except the last folder (y/n)? ")
if delete_runs.lower() == 'y':
    for encut in encut_values[:-1]:  # Exclude the last ENCUT value
        folder_name = 'ENCUT{0}'.format(encut)
        shutil.rmtree(folder_name)

# Step 7: Plot the convergence results
import matplotlib.pyplot as plt

# Initialize lists to store ENCUT values and energies
encut_values = []
energies = []

# Read the ENCUT values and energy values from summary.dat
with open('summary.dat', 'r') as summary_file:
    for line in summary_file:
        if line.startswith('#') or 'ENCUT' in line:  # Skip header lines
            continue
        parts = line.split()
        encut_values.append(float(parts[0]))
        energies.append(float(parts[1]))

# Plotting the ENCUT convergence
plt.plot(encut_values, energies, '-o')
plt.xlabel('ENCUT (eV)')
plt.ylabel('Energy (eV)')
plt.title('ENCUT Convergence Plot')
plt.savefig('energy_vs_encut.jpeg')
plt.show()
