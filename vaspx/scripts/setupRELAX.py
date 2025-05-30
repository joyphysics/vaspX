
import os
import shutil
import subprocess

def main():
    # Step 1: Check for POSCAR or a directory ending with 'MPRelaxSet'
    if os.path.isfile('POSCAR'):
        print("\n----> POSCAR file exists. Proceeding with the script...")
        if os.path.exists('1_Relax'):
            shutil.rmtree('1_Relax')
        os.mkdir('1_Relax')
        # Copy POSCAR file to the new directory
        shutil.copy2('POSCAR', '1_Relax/POSCAR')
        print("\n----> POSCAR file copied to '1_Relax' directory.\n")
    else:
        # Find directory ending with 'MPRelaxSet'
        mp_relax_dir = None
        for item in os.listdir('.'):
            if os.path.isdir(item) and item.endswith('MPRelaxSet'):
                mp_relax_dir = item
                break
        
        if not mp_relax_dir:
            print("\n----> No POSCAR file found and no directory ending with 'MPRelaxSet' found. Exiting.\n")
            return
        
        # Create '1_Relax' directory and copy contents
        if os.path.exists('1_Relax'):
            shutil.rmtree('1_Relax')

        os.mkdir('1_Relax')
        for item in os.listdir(mp_relax_dir):
            s = os.path.join(mp_relax_dir, item)
            d = os.path.join('1_Relax', item)
            if os.path.isdir(s):
                shutil.copytree(s, d)
            else:
                shutil.copy2(s, d)
        print("\n----> Directory '1_Relax' created and contents copied from '{0}'. Continuing with the script...\n".format(mp_relax_dir))

    # Step 2: Generate INCAR file
    print("----> Generating INCAR file")
    script_path = os.path.dirname(os.path.realpath(__file__))
    incar_script = os.path.join(script_path, 'generateINCAR2.py')
    subprocess.call(['python', incar_script], cwd='1_Relax')

    # Step 3: Generate KPOINTS file
    print("----> Generating KPOINTS file")
    kpoints_script = os.path.join(script_path, 'generateKPOINTS.py')
    subprocess.call(['python', kpoints_script], cwd='1_Relax')

    # Step 4: Generate POTCAR file
    print("----> Generating POTCAR file")
    potcar_script = os.path.join(script_path, 'generatePOTCAR2.py')
    subprocess.call(['python', potcar_script], cwd='1_Relax')

    # Step 5: Copy job.sh file
    job_script_path = os.path.join(script_path, 'job.sh')
    if os.path.isfile(job_script_path):
        shutil.copy2(job_script_path, '1_Relax')
        print("\n----> job.sh file copied to '1_Relax' directory.")
    else:
        print("\n----> job.sh file not found in the script directory. Exiting.")
        return

    # Step 6: Delete POTCAR.spec file if it exists
    potcar_spec_path = os.path.join('1_Relax', 'POTCAR.spec')
    if os.path.isfile(potcar_spec_path):
        os.remove(potcar_spec_path)
        print("\n----> POTCAR.spec file found and deleted.")
    
    # Step 7: Ask user whether to submit the VASP job
    user_input = raw_input("\n----> Do you want to submit the VASP job? (y/n): ")
    if user_input.lower() == 'y':
        print("\n----> Submitting the job...\n")
        subprocess.call(['qsub', 'job.sh'], cwd='1_Relax')
    else:
        print("\n----> Exiting without submitting the job.\n")
        return

if __name__ == '__main__':
    main()
