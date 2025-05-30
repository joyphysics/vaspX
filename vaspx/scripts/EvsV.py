# -*- coding: utf-8 -*-
import os
import shutil
import subprocess
import time

# Step 1: Check for required files
required_files = ['POSCAR', 'POTCAR', 'INCAR', 'KPOINTS', 'job.sh']
for file_name in required_files:
    if not os.path.exists(file_name):
        print("Error: Required file {0} not found. Exiting script.".format(file_name))
        exit(1)

# Step 2: Check for WAVECAR file existence
if os.path.exists('WAVECAR'):
    wavecar_exists = True
else:
    wavecar_exists = False

# Step 2.5: Create the summary.dat file
with open('summary.dat', 'w') as summary_file:
    summary_file.write("# Volume (Ang^3)    Energy (eV)\n")

# Step 3: Create folders and copy files
scaling_factors = [-0.15, -0.12, -0.09, -0.06, -0.03, 0.0, 0.03, 0.06, 0.09, 0.12, 0.15]
for i in range(len(scaling_factors)):
    folder_name = 'vol{0}'.format(i + 1)
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # Copy files to each folder
    for file_name in required_files:
        shutil.copy(file_name, folder_name)
    if wavecar_exists:
        shutil.copy('WAVECAR', folder_name)

    # Step 4: Modify POSCAR file scaling factor
    poscar_path = os.path.join(folder_name, 'POSCAR')
    with open(poscar_path, 'r') as poscar_file:
        poscar_lines = poscar_file.readlines()
    
    original_scaling_factor = float(poscar_lines[1].strip())
    new_scaling_factor = original_scaling_factor * (1 + scaling_factors[i])
    poscar_lines[1] = '   {0:.14f}\n'.format(new_scaling_factor)

    with open(poscar_path, 'w') as poscar_file:
        poscar_file.writelines(poscar_lines)

# Step 5: Run VASP jobs and gather data
for i in range(len(scaling_factors)):
    folder_name = 'vol{0}'.format(i + 1)
    os.chdir(folder_name)

    # Submit VASP job
    print("Submitting job in : %s" % folder_name)
    subprocess.call(['qsub', 'job.sh'])

    # Wait for OUTCAR file to be created and VASP job to complete
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
            print("Waiting for VASP run to finish...")
            time.sleep(30)

    # Initialize variables to store volume and energy values
    volume_value = None
    energy_value = None

    # Open and read the OUTCAR file line by line
    with open('OUTCAR', 'r') as outcar_file:
        for line in outcar_file:
            # Check for the volume of cell line
            if 'volume of cell' in line:
                volume_value = float(line.split(':')[-1].strip())
        
            # Check for the TOTEN line that contains the free energy
            if 'TOTEN' in line and 'free  energy' in line:
                energy_value = float(line.split('=')[-1].split()[0].strip())

    # Validate that the required values were found
    if volume_value is None or energy_value is None:
        print("Error: Could not find required data in OUTCAR.")
        exit(1)

    # Write volume and energy to summary.dat
    with open('../summary.dat', 'a') as summary_file:
        summary_file.write('{0:.6f}    {1:.8f}\n'.format(volume_value, energy_value))

    os.chdir('..')

# Step 6: Ask user if they want to delete all VASP runs
delete_runs = raw_input("Do you want to delete all VASP runs (y/n)? ")
if delete_runs.lower() == 'y':
    for i in range(len(scaling_factors) - 1):  # Delete all but the last
        folder_name = 'vol{0}'.format(i + 1)
        shutil.rmtree(folder_name)

# Step 7: Plot the data
import matplotlib.pyplot as plt

volumes = []
energies = []

with open('summary.dat', 'r') as summary_file:
    for line in summary_file:
        if line.startswith('#'):
            continue
        parts = line.split()
        volumes.append(float(parts[0]))
        energies.append(float(parts[1]))

plt.plot(volumes, energies, '-o')
plt.xlabel('Volume (Ang^3)')
plt.ylabel('Energy (eV)')
plt.title('Energy vs Volume Plot')

min_energy_index = energies.index(min(energies))
min_volume = volumes[min_energy_index]

plt.text(min_volume, min(energies), 'Vol_min = {0:.2f}'.format(min_volume))
plt.savefig('energy_vs_volume.jpeg')
plt.show()
