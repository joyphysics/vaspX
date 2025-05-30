#!/bin/bash

echo -e "\n-----------------------------------------------------------------------"

#Step 1: Create the '2_SCF' folder if it doesn't exist
mkdir -p 2_SCF

# Step 2: Copy necessary files from '1_Relax' to '2_SCF'
cp 1_Relax/CONTCAR 1_Relax/INCAR 1_Relax/KPOINTS 1_Relax/POTCAR 1_Relax/job.sh 2_SCF/

# Step 3: Rename 'CONTCAR' to 'POSCAR' in the '2_SCF' folder
mv 2_SCF/CONTCAR 2_SCF/POSCAR

# Step 3.1: Check if 'WAVECAR' file exists in the '1_Relax' folder, and copy it if it does
if [ -f "1_Relax/WAVECAR" ]; then
    cp 1_Relax/WAVECAR 2_SCF/
fi

# Step 4: Double the K-point grids values in the 'KPOINTS' file
awk 'NR==4 { for (i = 1; i <= NF; i++) $i *= 2 } 1' 2_SCF/KPOINTS > 2_SCF/KPOINTS.temp && mv 2_SCF/KPOINTS.temp 2_SCF/KPOINTS


# Step 5: Modify the 'INCAR' file
# Uncomment and set LWAVE, LCHARG, set NSW, IBRION, ISIF, and comment EDIFFG
sed -i 's/^\(  NELM\s*=\s*\).*/  NELM      = 500/' 2_SCF/INCAR
sed -i 's/^#\s*\(LWAVE\s*=\s*\).*/  \1.TRUE./' 2_SCF/INCAR
sed -i 's/^\(  NSW\s*=\s*\).*/  NSW       = 0/' 2_SCF/INCAR
sed -i 's/^\(  IBRION\s*=\s*\).*/  IBRION    = -1/' 2_SCF/INCAR
sed -i 's/^\(  ISIF\s*=\s*\).*/  ISIF      = 2/' 2_SCF/INCAR

# Step 5.1: Add 'LCHARG = .TRUE.' after 'LWAVE = .TRUE.' in the 'Output_Control' block
sed -i '/^  LWAVE\s*=\s*\.TRUE\./a\  LCHARG    = .TRUE.' 2_SCF/INCAR


# Step 5.2: Run the 'includeSOC.py' script with its full path
cd 2_SCF
python "$(dirname "$0")/includeSOC.py"
cd ..

# Step 6: Modify the 'job.sh' file
sed -i 's/^#PBS -N .*/#PBS -N 2_SCF/' 2_SCF/job.sh

echo -e "\n----> The 2_SCF folder is created successfully.\n"

# step 6: Ask the user if they want to submit the VASP run
read -p "Do you want to submit the job? (Y/N): " user_input

if [[ "$user_input" == "Y" || "$user_input" == "y" ]]; then
    # If the user inputs Y, submit the job
    cd 2_SCF
    qsub job.sh
    cd ..
    qstat
elif [[ "$user_input" == "N" || "$user_input" == "n" ]]; then
    # If the user inputs N, exit the script
    echo -e "Exiting the script.\n"
    echo -e "-----------------------------------------------------------------------\n"
    exit 0
else
    # If the user inputs anything else, show an error message
    echo "Invalid input. Please enter Y for Yes or N for No."
    exit 1
fi



