#!/bin/bash
#list of files to keep
files_to_keep=("INCAR" "job.sh" "KPOINTS" "POSCAR" "POTCAR" "WAVECAR")

# Loop through each file in the directory
for file in *; do
    # Check if the file is in the list of files to keep
    if [[ " ${files_to_keep[@]} " =~ " $file " ]]; then
        echo "Keeping file: $file"
    else
        # If not in the list, delete the file
        rm "$file"
        echo "Deleted file: $file"
    fi
done

