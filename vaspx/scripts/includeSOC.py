import os

# Step 1: Check if INCAR and POSCAR files exist
required_files = ['INCAR', 'POSCAR']
for filename in required_files:
    if not os.path.isfile(filename):
        print("\n----> Error: {0} not found in the current directory.".format(filename))
        exit(1)

# Step 2: Ask the user whether to do SOC calculation
user_input = raw_input("\n----> Do you want to perform SOC calculation? (y/n): ").strip().lower()
if user_input != 'y':
    print("\n----> Exiting as SOC calculation is not required.")
    exit(0)

# Step 3: Append SOC tags/block in the INCAR file before the MPI block
with open('INCAR', 'r') as incar_file:
    incar_lines = incar_file.readlines()

soc_block = [
    '#SOC_tags\n',
    '  LSORBIT   = .TRUE.\n',
    '  LORBMOM   = .TRUE.\n',
    '  SAXIS     = 0 0 1\n',
    '  NBANDS    = \n \n'
]

# Insert SOC block before MPI block
insert_index = next((i for i, line in enumerate(incar_lines) if '#MPI' in line), len(incar_lines))
incar_lines = incar_lines[:insert_index] + soc_block + incar_lines[insert_index:]

# Write the modified INCAR content back to the file
with open('INCAR', 'w') as incar_file:
    incar_file.writelines(incar_lines)

# Step 4: Ask the user for NBANDS value
nbands_value = raw_input("\n----> Enter the value for NBANDS: ").strip()

# Set the NBANDS value in the SOC block
with open('INCAR', 'r') as incar_file:
    incar_content = incar_file.read()

incar_content = incar_content.replace('  NBANDS    = \n', '  NBANDS    = {0}\n'.format(nbands_value))

with open('INCAR', 'w') as incar_file:
    incar_file.write(incar_content)

# Step 5: Read the element species and number of species from POSCAR
element_species = []
number_of_species = []

with open('POSCAR', 'r') as poscar_file:
    lines = poscar_file.readlines()

# Extract element species and number of species
element_species = lines[5].split()
number_of_species = list(map(int, lines[6].split()))

# Print the number of atoms for each element species
species_info = []
for i in range(len(element_species)):
    species_info.append("{0} {1}".format(number_of_species[i], element_species[i]))

print("\n----> In the POSCAR file: " + ", ".join(species_info) + " atom(s) are present.")

# Step 6: Ask the user to enter magnetic moments for each species
magmom_values = []
for i in range(len(element_species)):
    magmom = raw_input("\n----> Enter magnetic moment for {0}: ".format(element_species[i])).strip()
    magmom_values.append(int(magmom))

# Step 7: Check for existing MAGMOM tag and remove its value
with open('INCAR', 'r') as incar_file:
    incar_lines = incar_file.readlines()

# Find the MAGMOM tag if it exists
magmom_index = -1
for i, line in enumerate(incar_lines):
    if 'MAGMOM' in line:
        magmom_index = i
        break

# Remove existing MAGMOM values
if magmom_index != -1:
    incar_lines[magmom_index] = '  MAGMOM    = \n'
else:
    # Add MAGMOM tag if not present
    incar_lines.append('  MAGMOM    = \n')

# Step 7: Calculate the new MAGMOM values and append them to the INCAR file
magmom_list = []
for i in range(len(element_species)):
    for _ in range(number_of_species[i]):
        magmom_list.extend([0, 0, magmom_values[i]])

# Update MAGMOM tag in INCAR file
magmom_str = ' '.join(map(str, magmom_list))
incar_content = ''.join(incar_lines)
incar_content = incar_content.replace('  MAGMOM    = \n', '  MAGMOM    = {0}\n'.format(magmom_str))

with open('INCAR', 'w') as incar_file:
    incar_file.write(incar_content)

print("\n----> INCAR file modified successfully with the new SOC and MAGMOM settings.")
