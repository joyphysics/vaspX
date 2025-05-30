import os
import shutil
import subprocess

def main():
    # Check if POSCAR file exists
    print("\n==============================================================")
    if not os.path.isfile('POSCAR'):
        print("\n----> POSCAR file does not exist. Exiting the script.\n")
        return

    # Check if an INCAR file exists and rename it if it does
    if os.path.isfile('INCAR'):
        os.rename('INCAR', 'INCAR_old')
        print("\n----> Existing INCAR file renamed to INCAR_old.")

    # Copy master_INCAR to current directory and rename it INCAR
    script_path = os.path.dirname(os.path.realpath(__file__))
    master_incar_path = os.path.join(script_path, 'master_INCAR')
    
    if not os.path.isfile(master_incar_path):
        print("\n----> master_INCAR file does not exist in the script's directory. Exiting.")
        return
    
    shutil.copy(master_incar_path, 'INCAR')
    print("\n----> INCAR file created.")

    # Read system name from POSCAR and update SYSTEM tag in INCAR
    with open('POSCAR', 'r') as poscar_file:
        system_name = poscar_file.readline().strip().replace(" ", "")

    # Update SYSTEM tag in INCAR file
    with open('INCAR', 'r') as incar_file:
        incar_lines = incar_file.readlines()

    with open('INCAR', 'w') as incar_file:
        for line in incar_lines:
            if line.strip().startswith('SYSTEM'):
                incar_file.write('  SYSTEM    = "{0}"\n'.format(system_name))
            else:
                incar_file.write(line)

    # Ask user if they want to uncomment Hubbard U tags
    user_input = raw_input("\n----> Do you want to keep the Hubbard_U tags? (y/n): ")
    if user_input.lower() == 'y':
        uncomment_section('INCAR', '#Hubbard_U')

    # Ask user if they want to uncomment mixing parameters tags
    user_input = raw_input("\n----> Do you want to keep the mixing_parameter tags? (y/n): ")
    if user_input.lower() == 'y':
        uncomment_section('INCAR', '#Mixing_parameters')
        
    # Spin polarizatio
    spinpol_script = os.path.join(script_path, 'spin_polarization.py')
    subprocess.call(['python', spinpol_script])

    print("\n----> INCAR file generated and modified successfully.")
    print("\n==============================================================\n")

def uncomment_section(file_path, section_start):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    with open(file_path, 'w') as file:
        uncommenting = False
        for line in lines:
            if line.startswith(section_start):
                uncommenting = True
                file.write(line)
            elif uncommenting and line.startswith('#'):
                file.write(line[1:])  # Remove the leading '#' to uncomment
            else:
                uncommenting = False
                file.write(line)

if __name__ == '__main__':
    main()
