import os
import shutil
import subprocess

print("\n-----------------------------------------------------------------------")
# Step 1: Check if a POSCAR file exists
if not os.path.isfile('POSCAR'):
    print("Error: POSCAR file not found in the current directory.")
    exit(1)

# Step 2: Check if an INCAR file exists and rename it to INCAR_old if it does
if os.path.isfile('INCAR'):
    shutil.move('INCAR', 'INCAR_old')

# Step 3: Create a new INCAR file
with open('INCAR', 'w') as incar_file:

    # Step 4: Read the System Name from the POSCAR file and add it to the INCAR file
    with open('POSCAR', 'r') as poscar_file:
        system_name = poscar_file.readline().strip().replace(" ", "")
    
    incar_file.write('#System_Name\n')
    incar_file.write('  SYSTEM    = "{0}"\n'.format(system_name))

    # Step 5: Add Global Parameters block to the INCAR file
    incar_file.write('\n#Global_Parameters\n')
    incar_file.write('  ISTART    = 1\n')
    incar_file.write('  ENCUT     = 520\n')
    incar_file.write('  LREAL     = .FALSE.\n')
    incar_file.write('  ALGO      = Normal\n')
    incar_file.write('  PREC      = Accurate\n')
    incar_file.write('  ADDGRID   = .TRUE.\n')
    incar_file.write('  LASPH     = .TRUE.\n')
    incar_file.write('  GGA_COMPAT = .FALSE.\n')

    # Step 5: Add Electronic Minimization block to the INCAR file
    incar_file.write('\n#Electronic_minimization\n')
    incar_file.write('  ISMEAR    = 0\n')
    incar_file.write('  EDIFF     = 1E-8\n')
    incar_file.write('  SIGMA     = 0.05\n')
    incar_file.write('  NELMIN    = 5\n')
    incar_file.write('  NELM      = 300\n')

    # Step 5: Add Ionic Minimization block to the INCAR file
    incar_file.write('\n#Ionic_minimization\n')
    incar_file.write('  ISYM      = 2\n')
    incar_file.write('  ISIF      = 3\n')
    incar_file.write('  NSW       = 300\n')
    incar_file.write('  IBRION    = 2\n')
    incar_file.write('  EDIFFG    = -0.01\n')

    # Step 5: Add Output Control block to the INCAR file
    incar_file.write('\n#Output_Control\n')
    incar_file.write('  LORBIT    = 11\n')
    incar_file.write('  LWAVE     = .TRUE.\n')

# Step 6: Add Spin Polarization block and run the spin_polarization.py script
with open('INCAR', 'a') as incar_file:
    incar_file.write('\n#Spin_polarization\n')
    incar_file.write('  ISPIN     = 1\n')

# Determine the full path of the current Python script
current_script_path = os.path.abspath(__file__)
current_script_dir = os.path.dirname(current_script_path)
spin_polarization_script_path = os.path.join(current_script_dir, 'spin_polarization.py')
subprocess.call(['python', spin_polarization_script_path])



# Step 7: Ask if the user wants to add Hubbard U parameters
hubbard_u = raw_input("Do you want to add Hubbard_U parameters? (y/n): ").strip().lower()
if hubbard_u == 'y':
    with open('INCAR', 'a') as incar_file:
        incar_file.write('\n#Hubbard_U\n')
        incar_file.write('  LDAU      = .TRUE.\n')
        incar_file.write('  LDAUTYPE  = 2\n')
        incar_file.write('  LDAUL     = 2 0 0 0\n')
        incar_file.write('  LDAUU     = 3.9 0.0 0.0 0.0\n')
        incar_file.write('  LDAUJ     = 0.0 0.0 0.0 0.0\n')
        incar_file.write('  LDAUPRINT = 2\n')
        incar_file.write('  LMAXMIX   = 4\n')
    print("Note: Modify the Hubbard U block according to your system.")

# Step 8: Ask if the user wants to add mixing parameters
mixing_params = raw_input("Do you want to add mixing parameters? (y/n): ").strip().lower()
if mixing_params == 'y':
    with open('INCAR', 'a') as incar_file:
        incar_file.write('\n#Mixing_parameters\n')
        incar_file.write('  AMIX      = 0.2\n')
        incar_file.write('  BMIX      = 0.00001\n')
        incar_file.write('  AMIX_MAG  = 0.8\n')
        incar_file.write('  BMIX_MAG  = 0.00001\n')

# Step 9: Ask if the user wants to add SOC tags
soc_tags = raw_input("Do you want to add SOC tags? (y/n): ").strip().lower()
if soc_tags == 'y':
    with open('INCAR', 'a') as incar_file:
        incar_file.write('\n#SOC_tags\n')
        incar_file.write('  LSORBIT   = .TRUE.\n')
        incar_file.write('  LORBMOM   = .TRUE.\n')
        incar_file.write('  SAXIS     = 0 0 1\n')
        incar_file.write('  NBANDS    = 80\n')

# Step 10: Add MPI block to the INCAR file
with open('INCAR', 'a') as incar_file:
    incar_file.write('\n#MPI\n')
    incar_file.write('  NCORE     = 4\n')

# Final message
print("\n----> INCAR file generated successfully.")
print("----> Check/modify the INCAR file carefully before running the job.\n")
print("-----------------------------------------------------------------------\n")
