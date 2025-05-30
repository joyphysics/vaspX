#!/bin/bash

#Step 1: Create the '2_SPC' folder if it doesn't exist
mkdir -p 2_SPC

# Step 2: Copy necessary files from '1_Relax_ISIF3' to '2_SPC'
cp 1_Relax_ISIF3/CONTCAR 1_Relax_ISIF3/INCAR 1_Relax_ISIF3/KPOINTS 1_Relax_ISIF3/POTCAR 1_Relax_ISIF3/job.sh 2_SPC/

# Step 3: Rename 'CONTCAR' to 'POSCAR' in the '2_SPC' folder
mv 2_SPC/CONTCAR 2_SPC/POSCAR

# Step 4: Double the K-point grids values in the 'KPOINTS' file
awk 'NR==4 { for (i = 1; i <= NF; i++) $i *= 2 } 1' 2_SPC/KPOINTS > 2_SPC/KPOINTS.temp && mv 2_SPC/KPOINTS.temp 2_SPC/KPOINTS


# Step 5: Modify the 'INCAR' file
# Uncomment and set LWAVE, LCHARG, set NSW, IBRION, ISIF, and comment EDIFFG
sed -i 's/^\(  NELM\s*=\s*\).*/  NELM      = 500/' 2_SPC/INCAR
sed -i 's/^#\s*\(LWAVE\s*=\s*\).*/  \1.TRUE./' 2_SPC/INCAR
sed -i 's/^#\s*\(LCHARG\s*=\s*\).*/  \1.TRUE./' 2_SPC/INCAR
sed -i 's/^\(  NSW\s*=\s*\).*/  NSW       = 0/' 2_SPC/INCAR
sed -i 's/^\(  IBRION\s*=\s*\).*/  IBRION    = -1/' 2_SPC/INCAR
sed -i 's/^\(  ISIF\s*=\s*\).*/  ISIF      = 2/' 2_SPC/INCAR
sed -i 's/^\(\s*EDIFFG\s*=\s*.*\)$/#  \1/' 2_SPC/INCAR

# Step 6: Modify the 'job.sh' file
sed -i 's/^#PBS -N .*/#PBS -N 2_SPC/' 2_SPC/job.sh

echo "The 2_SPC folder is created successfully."

# step 6: Ask the user if they want to submit the VASP run
read -p "Do you want to submit the job? (Y/N): " user_input

if [[ "$user_input" == "Y" || "$user_input" == "y" ]]; then
    # If the user inputs Y, submit the job
    cd 2_SPC
    qsub job.sh
    cd ..
    qstat
elif [[ "$user_input" == "N" || "$user_input" == "n" ]]; then
    # If the user inputs N, exit the script
    echo "Exiting the script."
    exit 0
else
    # If the user inputs anything else, show an error message
    echo "Invalid input. Please enter Y for Yes or N for No."
    exit 1
fi

