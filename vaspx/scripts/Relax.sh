#!/bin/bash

echo " "
echo " "
echo "------------------------------------------------------------------------------ "
echo "N.B.: This command only works in the folder downloaded from Materials Project."
echo "------------------------------------------------------------------------------ "

# Check if all required files are present
required_files=("INCAR" "KPOINTS" "POTCAR.spec" "POSCAR")
for file in "${required_files[@]}"; do
    if [[ ! -f $file ]]; then
        echo "Error: $file is missing."
        exit 1
    fi
done

# Create the 1_Relax_ISIF3 directory
mkdir -p 1_Relax_ISIF3

# Copy KPOINTS and POSCAR to the 1_Relax_ISIF3 directory
cp KPOINTS POSCAR 1_Relax_ISIF3/

# Alternative method to get the script directory
script_dir="$(cd "$(dirname "$0")" && pwd)"
cp "$script_dir/INCAR" 1_Relax_ISIF3/

# Read elements from the POTCAR.spec file and store them in an array
elements=()
while IFS= read -r line || [[ -n "$line" ]]; do
    elements+=("$line")
done < POTCAR.spec

# Print the elements read from POTCAR.spec
echo "POTCAR tags are: ${elements[@]}"

# Generate POTCAR in the 1_Relax_ISIF3 directory using the generatePOTCAR.sh script
cd 1_Relax_ISIF3 || exit 1
"$script_dir/generatePOTCAR.sh" "${elements[@]}"

echo "------------------------------------------------------------------------------ "
echo "                1_Relax_ISIF3 folder is created successfully.    "
echo "------------------------------------------------------------------------------ "
echo " "
echo " "

