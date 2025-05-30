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
        
##############################################################################################       
# Step 1.5: Ensure that NSW = 0, ISIF = 2, IBRION = -1 in the INCAR file
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
    elif 'LWAVE' in line:
        incar_content[i] = '  LWAVE     = .FALSE.\n'
    elif 'LCHARG' in line:
        incar_content[i] = '  LCHARG    = .FALSE.\n'
# Write the updated content back to the INCAR file
with open('INCAR', 'w') as incar_file:
    incar_file.writelines(incar_content)


##############################################################################################
# Step 2: Ask the user for the initial and final K values
initial_k = int(raw_input("Enter the initial K value: "))
final_k = int(raw_input("Enter the final K value: "))

# Create the folders and the summary.dat file
summary_file = open('summary.dat', 'w')
summary_file.write("#KPOINTS    ENERGY\n")


##############################################################################################
# Step 3: Copy the necessary files into each new folder
for k in range(initial_k, final_k + 1):
    folder_name = 'K{0}'.format(k)
    os.mkdir(folder_name)
    
    for filename in required_files:
        shutil.copy(filename, folder_name)

    # Read the existing KPOINTS file
    with open('KPOINTS', 'r') as kpoints_file:
        kpoints_content = kpoints_file.readlines()

    # Determine the k-point method (Gamma or Monkhorst)
    method = kpoints_content[2].strip()

    # Update the KPOINTS file for the current folder
    kpoints_content[3] = '{0} {0} {0}\n'.format(k)
    
    # Write the updated KPOINTS file into the folder
    with open(os.path.join(folder_name, 'KPOINTS'), 'w') as kpoints_file:
        kpoints_file.writelines(kpoints_content)


##############################################################################################
# Step 4: Ask user if they want to perform the VASP run
perform_vasp_run = raw_input("Do you want to perform the VASP run? (y/n): ").strip().lower()
if perform_vasp_run != 'y':
    print("Exiting script as per user request.")
    exit(0)


##############################################################################################
# Step 5: Perform the VASP run for each folder and collect energy values
for k in range(initial_k, final_k + 1):
    folder_name = 'K{0}'.format(k)
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

    # Write K value and energy to summary.dat
    with open('../summary.dat', 'a') as summary_file:
        summary_file.write('{0}    {1:.8f}\n'.format(k, energy_value))
    
    os.chdir('..')

print("K-point convergence run completed. Check summary.dat for the results.")


##############################################################################################
# Step 6: Ask user if they want to delete all VASP runs
delete_runs = raw_input("Do you want to delete all VASP runs (y/n)? ")
if delete_runs.lower() == 'y':
    for i in range(initial_k, final_k):  # Delete all but the last
        folder_name = 'K{0}'.format(i)
        shutil.rmtree(folder_name)


##############################################################################################
# step 7 : Plot the curve
import matplotlib.pyplot as plt

# Initialize lists to store K values and energies
kvalues = []
energies = []

# Read the K values and energy values from summary.dat
with open('summary.dat', 'r') as summary_file:
    for line in summary_file:
        if line.startswith('#') or 'KPOINTS' in line:  # Skip header lines
            continue
        parts = line.split()
        kvalues.append(float(parts[0]))
        energies.append(float(parts[1]))

# Plotting the K point convergence
plt.plot(kvalues, energies, '-o')
plt.xlabel('K values')
plt.ylabel('Energy (eV)')
plt.title('K point convergence plot (Scheme: {0})'.format(method))
plt.savefig('energy_vs_kpoints.jpeg')
plt.show()
