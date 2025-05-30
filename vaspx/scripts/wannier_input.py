import os
import shutil

# Step 1: Create a folder named 10_wannier_input in the present directory
output_dir = "10_wannier_input"
if os.path.exists(output_dir):
    shutil.rmtree(output_dir)
os.makedirs(output_dir)


# Step 2: Copy specific files from the folder 2_SCF to 10_wannier_input
source_dir = "2_SCF"
files_to_copy = ["INCAR", "KPOINTS", "POTCAR", "CONTCAR", "job.sh", "WAVECAR", "CHGCAR"]


for filename in files_to_copy:
    src_file = os.path.join(source_dir, filename)
    dst_file = os.path.join(output_dir, filename)
    shutil.copy(src_file, dst_file)
    
os.rename(os.path.join(output_dir, "CONTCAR"), os.path.join(output_dir, "POSCAR"))
    

# Step 3: Generate a file named wannier90.win in 10_wannier_input
wannier90_win_path = os.path.join(output_dir, "wannier90.win")
with open(wannier90_win_path, "w") as win_file:
    win_file.write("Begin Projections\n\nEnd Projections\n\nnum_wann =\n")

# Step 4: Modify the INCAR file in 10_wannier_input folder
incar_path = os.path.join(output_dir, "INCAR")

with open(incar_path, "r") as incar_file:
    incar_content = incar_file.readlines()

with open(incar_path, "w") as incar_file:
    for line in incar_content:
        if "ISTART" in line:
            incar_file.write("  ISTART    = 1\n")
        elif "LWAVE" in line:
            incar_file.write("#  " + line)
        elif "LCHARG" in line:
            incar_file.write("#  " + line)
        elif "NCORE" in line:
            incar_file.write("#  " + line)
        else:
            incar_file.write(line)
    incar_file.write("\n#Wannier\n  LWANNIER90 = .TRUE.\n")

# Step 6: Print a success message
print("wannier_input directory created successfully. Edit the wannier90.win file first and then submit the job.")

