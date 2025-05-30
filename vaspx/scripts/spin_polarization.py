import os

# Step 1: Check if INCAR and POSCAR files exist
required_files = ['INCAR', 'POSCAR']
for filename in required_files:
    if not os.path.isfile(filename):
        print("\n----> Error: {0} not found in the current directory.".format(filename))
        exit(1)

# Step 2: Read the element species and number of species from POSCAR
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

# Step 3: Ask the user whether to do a spin-polarized calculation
spin_polarized = raw_input("\n----> Do you want to do a spin-polarized calculation? (y/n): ").strip().lower()

# Step 4: Modify INCAR for non-spin-polarized calculation if the user selects 'no'
if spin_polarized == 'n':
    with open('INCAR', 'r') as incar_file:
        incar_content = incar_file.readlines()

    # Update or add tags in the INCAR file
    incar_modified = []
    found_ispin = False

    for line in incar_content:
        if 'ISPIN' in line:
            incar_modified.append('  ISPIN     = 1\n')
            found_ispin = True
        elif 'MAGMOM' not in line and 'VOSKOWN' not in line:
            incar_modified.append(line)

    if not found_ispin:
        incar_modified.insert(0, '#Spin_Polarization\n  ISPIN     = 1\n')

    # Write modified INCAR content back to file
    with open('INCAR', 'w') as incar_file:
        incar_file.writelines(incar_modified)

# Step 5: Modify INCAR for spin-polarized calculation if the user selects 'yes'
elif spin_polarized == 'y':
    with open('INCAR', 'r') as incar_file:
        incar_content = incar_file.readlines()

    # Update or add tags in the INCAR file
    incar_modified = []
    found_ispin = False
    found_voskown = False

    for line in incar_content:
        if 'ISPIN' in line:
            incar_modified.append('  ISPIN     = 2\n')
            found_ispin = True
        elif 'VOSKOWN' in line:
            found_voskown = True
        elif 'MAGMOM' not in line:
            incar_modified.append(line)

    # Insert ISPIN and associated tags at the beginning of the spin-polarized block
    isp_tags = ['  ISPIN     = 2\n']
    isp_tags.append('  VOSKOWN   = 0\n')
    #if not found_voskown:
     #   isp_tags.append('  VOSKOWN   = 0\n')

    # Step 6: Set the MAGMOM tag
    magmom_values = []
    print(" ")
    for i, element in enumerate(element_species):
        magmom = float(raw_input("Enter the initial magnetic moment for {0}: ".format(element)))
        magmom_values.append("{0}*{1}".format(number_of_species[i], magmom))

    magmom_tag = '  MAGMOM    = ' + ' '.join(magmom_values) + '\n'
    isp_tags.append(magmom_tag)

    # Add ISPIN tags right after ISPIN line
    if found_ispin:
        incar_modified = [line.replace('  ISPIN     = 2\n', ''.join(isp_tags)) if 'ISPIN' in line else line for line in incar_modified]
    else:
        incar_modified = isp_tags + incar_modified

    # Write modified INCAR content back to file
    with open('INCAR', 'w') as incar_file:
        incar_file.writelines(incar_modified)

# Step 7: Print the full spin-polarized block from the INCAR file
print("\n----> Spin polarization tags in the INCAR file:")
with open('INCAR', 'r') as incar_file:
    incar_content = incar_file.readlines()
    spin_block_started = False
    for line in incar_content:
        if 'ISPIN' in line:
            print(line.strip())
            spin_block_started = True
        elif spin_block_started and ('VOSKOWN' in line or 'MAGMOM' in line):
            print(line.strip())
        elif spin_block_started and line.strip() == '':
            break

print(" ")
