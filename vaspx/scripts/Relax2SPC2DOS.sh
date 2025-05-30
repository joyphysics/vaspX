#!/bin/bash


########################################################################
# SPC calculation
########################################################################

#Step 1: Create the 'SPC' folder if it doesn't exist
mkdir -p SPC

# Step 2: Copy necessary files from 'Relax_ISIF3' to 'SPC'
cp Relax_ISIF3/CONTCAR Relax_ISIF3/INCAR Relax_ISIF3/KPOINTS Relax_ISIF3/POTCAR Relax_ISIF3/job.sh SPC/

# Step 3: Rename 'CONTCAR' to 'POSCAR' in the 'SPC' folder
mv SPC/CONTCAR SPC/POSCAR

# Step 4: Double the K-point grids values in the 'KPOINTS' file
awk 'NR==4 { for (i = 1; i <= NF; i++) $i *= 2 } 1' SPC/KPOINTS > SPC/KPOINTS.temp && mv SPC/KPOINTS.temp SPC/KPOINTS


# Step 5: Modify the 'INCAR' file
# Uncomment and set LWAVE, LCHARG, set NSW, IBRION, ISIF, and comment EDIFFG
sed -i 's/^#\s*\(LWAVE\s*=\s*\).*/  \1.TRUE./' SPC/INCAR
sed -i 's/^#\s*\(LCHARG\s*=\s*\).*/  \1.TRUE./' SPC/INCAR
sed -i 's/^\(  NSW\s*=\s*\).*/  NSW       = 0/' SPC/INCAR
sed -i 's/^\(  IBRION\s*=\s*\).*/  IBRION    = -1/' SPC/INCAR
sed -i 's/^\(  ISIF\s*=\s*\).*/  ISIF      = 2/' SPC/INCAR
sed -i 's/^\(\s*EDIFFG\s*=\s*.*\)$/#  \1/' SPC/INCAR

echo "The SPC folder is created successfully."

cd SPC
qsub job.sh
cd ..
qstat


# Step 6: Checking the VASP run
# Path to the OUTCAR file
OUTCAR="SPC/OUTCAR"

# Loop until the OUTCAR file is generated
while [ ! -f "$OUTCAR" ]; do
    echo "Waiting for OUTCAR file to be generated..."
    sleep 10
done

echo "OUTCAR file found. Starting to check for completion."

# Loop until the VASP run is finished
while true; do
    # Wait for 10 seconds
    sleep 60

    # Check for the completion message in the OUTCAR file
    if tail -n 100 "$OUTCAR" | grep -q "Voluntary context switches"; then
        echo "VASP SPC run has finished successfully."
        break
    else
        echo "VASP SPC run is still in progress. Checking again in few minutes..."
        qstat
    fi
done


########################################################################
# DOS calculation
########################################################################


# Step 7: Create the 'DOS_calculation' folder if it doesn't exist
mkdir -p DOS_calculation

# Step 8: Copy necessary files from 'SPC' to 'DOS_calculation'
cp SPC/CONTCAR SPC/INCAR SPC/KPOINTS SPC/POTCAR SPC/WAVECAR SPC/CHGCAR SPC/job.sh DOS_calculation/

# Step 9: Rename 'CONTCAR' to 'POSCAR' in the 'DOS_calculation' folder
mv DOS_calculation/CONTCAR DOS_calculation/POSCAR

# Step 10: Double the K-point grids values in the 'KPOINTS' file
awk 'NR==4 { for (i = 1; i <= NF; i++) $i *= 2 } 1' DOS_calculation/KPOINTS > DOS_calculation/KPOINTS.temp && mv DOS_calculation/KPOINTS.temp DOS_calculation/KPOINTS

# Step 11: Modify the 'INCAR' file LWAVE, LCHARG, ISTART, ICHARG, NEDOS, EMAX, EMIN
# Comment out LWAVE and LCHARG
sed -i 's/^\(\s*LWAVE\s*=\s*.*\)$/# \1/' DOS_calculation/INCAR
sed -i 's/^\(\s*LCHARG\s*=\s*.*\)$/# \1/' DOS_calculation/INCAR
# Modify ISTART and uncomment ICHARG, NEDOS, EMAX, EMIN
sed -i 's/^\(\s*ISTART\s*=\s*\).*/\1 1/' DOS_calculation/INCAR
sed -i 's/^#\s*\(  ICHARG\s*=\s*11\)/\1/' DOS_calculation/INCAR
sed -i 's/^#\s*\(  NEDOS\s*=\s*701\)/\1/' DOS_calculation/INCAR
sed -i 's/^#\s*\(  EMIN\s*=\s*.*\)/\1/' DOS_calculation/INCAR
sed -i 's/^#\s*\(  EMAX\s*=\s*.*\)/\1/' DOS_calculation/INCAR

# Step 12: Modify the 'job.sh' file
# Change the #PBS -N tag to DOS_calculation
sed -i 's/^#PBS -N .*/#PBS -N DOS_calculation/' DOS_calculation/job.sh

echo "DOS_calculation folder is created successfully."
echo "Starting the calculation in DOS_calculation."


cd DOS_calculation
qsub job.sh
cd ..
qstat


# Step 12: Checking the VASP run
# Path to the OUTCAR file
OUTCAR="DOS_calculation/OUTCAR"

# Loop until the OUTCAR file is generated
while [ ! -f "$OUTCAR" ]; do
    echo "Waiting for OUTCAR file to be generated..."
    sleep 10
done

echo "OUTCAR file found. Starting to check for completion."

# Loop until the VASP run is finished
while true; do
    # Wait for 10 seconds
    sleep 60

    # Check for the completion message in the OUTCAR file
    if tail -n 100 "$OUTCAR" | grep -q "Voluntary context switches"; then
        echo "VASP DOS run has finished successfully."
        break
    else
        echo "VASP DOS run is still in progress. Checking again in few minutes..."
        qstat
    fi
done



########################################################################
# BAND structure calculation
########################################################################







