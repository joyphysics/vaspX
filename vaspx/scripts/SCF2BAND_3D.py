import os
import shutil
import subprocess
import time

# Step 1: Check if the '2_SCF' folder exists
if not os.path.isdir('2_SCF'):
    print("\n----> Error: '2_SCF' folder does not exist in the current directory.")
    exit(1)

# Step 2: Create the '4_BAND_calculation' folder in the present directory if it does not exist
directory_name = '4_BAND_calculation'
if not os.path.exists(directory_name):
    os.makedirs(directory_name)
else:
    print("\n----> Directory '{0}' already exists. Skipping creation.".format(directory_name))

# Step 3: Copy specified files from '2_SCF' to '4_BAND_calculation'
files_to_copy = ['INCAR', 'CONTCAR', 'POTCAR', 'KPOINTS', 'WAVECAR', 'CHGCAR', 'job.sh']
for filename in files_to_copy:
    source = os.path.join('2_SCF', filename)
    if os.path.isfile(source):
        shutil.copy(source, '4_BAND_calculation')

# Step 3.1: Rename 'CONTCAR' to 'POSCAR' in the '4_BAND_calculation' folder
contcar_path = os.path.join('4_BAND_calculation', 'CONTCAR')
poscar_path = os.path.join('4_BAND_calculation', 'POSCAR')
if os.path.isfile(contcar_path):
    os.rename(contcar_path, poscar_path)

# Step 4: Generate KPATH
os.chdir('4_BAND_calculation')

process = subprocess.Popen(['vaspkit'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

process.stdin.write(b'303\n')
process.stdin.flush()

time.sleep(5)

kpath_file = 'KPATH.in'
if os.path.isfile(kpath_file):
    os.rename(kpath_file, 'KPOINTS')

os.chdir('..')



# Step 5: Append the Band and DOS block before the MPI block in the 'INCAR' file
incar_path = os.path.join('4_BAND_calculation', 'INCAR')
if os.path.isfile(incar_path):
    with open(incar_path, 'r') as incar_file:
        incar_lines = incar_file.readlines()

    band_dos_block = [
        '#Band_and_DOS\n',
        '  ICHARG   = 11\n',
        '#  NEDOS    = 601\n',
        '#  EMIN      = -10\n',
        '#  EMAX      = 10\n\n'
    ]

    # Find the index before the MPI block to insert the Band and DOS block
    mpi_index = next((i for i, line in enumerate(incar_lines) if '#MPI' in line), len(incar_lines))
    incar_lines = incar_lines[:mpi_index] + band_dos_block + incar_lines[mpi_index:]

    with open(incar_path, 'w') as incar_file:
        incar_file.writelines(incar_lines)

# Step 6: Find and set LWAVE and LCHARG tags to .FALSE.
if os.path.isfile(incar_path):
    with open(incar_path, 'r') as incar_file:
        incar_lines = incar_file.readlines()

    # Find and set the LWAVE and LCHARG tags
    for i, line in enumerate(incar_lines):
        if line.strip().startswith('LWAVE'):
            incar_lines[i] = '  LWAVE     = .FALSE.\n'
        elif line.strip().startswith('LCHARG'):
            incar_lines[i] = '  LCHARG    = .FALSE.\n'

    # Write the modified lines back to the INCAR file
    with open(incar_path, 'w') as incar_file:
        incar_file.writelines(incar_lines)

# Step 7: Change the job name from '2_SCF' to '4_BAND' in the 'job.sh' file
job_path = os.path.join('4_BAND_calculation', 'job.sh')
if os.path.isfile(job_path):
    with open(job_path, 'r') as job_file:
        job_content = job_file.read()

    # Replace the job name
    job_content = job_content.replace('#PBS -N 2_SCF', '#PBS -N 4_BAND')

    with open(job_path, 'w') as job_file:
        job_file.write(job_content)

print("\n----> The 4_BAND_calculation folder is created successfully.\n")
