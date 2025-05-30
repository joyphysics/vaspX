#!/bin/bash

# 1. Check whether the folder 'Initial' is present in the current directory
if [ ! -d "Initial" ]; then
    echo "Folder 'Initial' is not present. Exiting."
    exit 1
fi

# 2. Check whether required files are present in the 'Initial' directory
required_files=("INCAR" "POSCAR" "job.sh" "KPOINTS" "POTCAR")
files_present=true

for file in "${required_files[@]}"; do
    if [ ! -f "Initial/$file" ]; then
        echo "Required file $file is not present."
        files_present=false
    fi
done

if $files_present; then
    echo "All required files are present."
else
    echo "Some required files are not present."
fi

echo "Now generating different KPOINT files"
# Loop to generate different KPOINTS files with different values of 'x'
for ((x=1; x<=5; x++)); do
    # Create folder with name "K_x"
    folder_name="K_$x"
    mkdir -p "$folder_name"
    
    # Generate KPOINTS file with different 'x' value
    sed "s/'x'/$x/g" Initial/KPOINTS > "$folder_name/KPOINTS"

    # Copy other files into the folder
    cp Initial/INCAR "$folder_name/"
    cp Initial/POSCAR "$folder_name/"
    cp Initial/POTCAR "$folder_name/"
    cp Initial/job.sh "$folder_name/"

    # Run VASP job
    cd "$folder_name"
    qsub job.sh
    cd .. 
done

echo "KPOINTS files with different 'x' values have been generated."

