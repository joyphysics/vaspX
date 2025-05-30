import os
import shutil
import subprocess
import re

# Step 1: Create a folder named 11_wannier_band in the present directory
output_dir = "11_wannier_band"
if os.path.exists(output_dir):
    shutil.rmtree(output_dir)
os.makedirs(output_dir)

# Step 2: Copy specific files from the folder 10_wannier_input to 11_wannier_band
source_dir = "10_wannier_input"
files_to_copy = ["wannier90.win", "wannier90.amn", "wannier90.mmn", "wannier90.eig", "POSCAR"]

for filename in files_to_copy:
    src_file = os.path.join(source_dir, filename)
    dst_file = os.path.join(output_dir, filename)
    shutil.copy(src_file, dst_file)

# Step 3: Run VASPkit and generate KPATH.wannier90
process = subprocess.Popen(
    ['vaspkit'], 
    stdin=subprocess.PIPE, 
    stdout=subprocess.PIPE, 
    stderr=subprocess.PIPE, 
    universal_newlines=True, 
    cwd=output_dir  # Run vaspkit in the 11_wannier_band directory
)

# Sending commands to VASPkit
commands = """
304   # Correct VASPkit option for generating KPATH.wannier90
2     # Appropriate options as needed
"""  
stdout, stderr = process.communicate(input=commands)

# Optional: Print the output and errors from VASPkit for debugging
print("Output:", stdout)
print("Errors:", stderr)

# Step 4: Modify the wannier90.win file in the 11_wannier_band folder
wannier90_win_path = os.path.join(output_dir, "wannier90.win")

# Copy the block from KPATH.wannier90 to wannier90.win after "end atoms_cart"
kpath_file = os.path.join(output_dir, "KPATH.wannier90")

with open(kpath_file, "r") as kpath:
    kpath_lines = kpath.readlines()

begin_block = None
end_block = None
for i, line in enumerate(kpath_lines):
    if "begin kpoint_path" in line:
        begin_block = i
    if "end kpoint_path" in line:
        end_block = i
        break

# If the k-point path block is found, insert it after "end atoms_cart"
if begin_block is not None and end_block is not None:
    kpoint_block = kpath_lines[begin_block:end_block + 1]
    
    # Read the current lines of wannier90.win
    with open(wannier90_win_path, "r") as win_file:
        lines = win_file.readlines()

    # Write back with the kpoint block inserted after "end atoms_cart"
    with open(wannier90_win_path, "w") as win_file:
        for line in lines:
            win_file.write(line)
            if "end atoms_cart" in line:
                win_file.write("\nbands_plot      =  true\n")
                win_file.write("bands_plot_format = gnuplot xmgrace\n")
                win_file.write("bands_num_points = 40\n\n")
                win_file.writelines(kpoint_block)
                
                
# Step 5: Extract the value of NBANDS from OUTCAR using grep
grep_process = subprocess.Popen(
    ['grep', 'NBANDS', '2_SPC/OUTCAR'],  # Corrected the path to the OUTCAR file
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    universal_newlines=True
)
grep_output, _ = grep_process.communicate()

# Debugging: Print the raw output to verify its format
print("Grep Output:", grep_output)

# Extract the value of NBANDS using regular expressions
nbands_value = None
match = re.search(r"NBANDS\s*=\s*(\d+)", grep_output)
if match:
    nbands_value = match.group(1)

print("Extracted NBANDS Value:", nbands_value)

# Insert num_bands after "num_wann" if NBANDS was found
if nbands_value:
    with open(wannier90_win_path, "r") as win_file:
        lines = win_file.readlines()

    with open(wannier90_win_path, "w") as win_file:
        for line in lines:
            win_file.write(line)
            if line.strip().startswith("num_wann"):
                win_file.write("num_bands = {0}\n".format(nbands_value))


# Step 6: Print a success message
print("wannier_band directory created successfully and wannier90.win modified. You can now proceed with your calculations.")

