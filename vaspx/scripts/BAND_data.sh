#!/bin/bash

#Step 1: Create the 'BAND_data' folder if it doesn't exist
mkdir -p BAND_data

# Step 2: Copy the necessary files to the 'BAND_data' folder
cp PROCAR DOSCAR INCAR POSCAR OUTCAR EIGENVAL KPOINTS  BAND_data/

# Step 3: Run VASPkit with the option 111
cd BAND_data
vaspkit << EOF
211
EOF

# Step 4: Create a new directory '111_TDOS'
mkdir -p 211_TBAND

# Step 5: Move all newly created files by VASPkit to '111_TDOS', except INCAR, POSCAR, PROCAR, and DOSCAR
find . -maxdepth 1 -type f ! -name 'INCAR' ! -name 'POSCAR' ! -name 'PROCAR' ! -name 'DOSCAR' ! -name 'OUTCAR' ! -name 'EIGENVAL' ! -name 'KPOINTS' -exec mv {} 211_TBAND/ \;


# Step 6: PDOS
vaspkit << EOF
213
EOF
mkdir -p 213_PBAND
find . -maxdepth 1 -type f ! -name 'INCAR' ! -name 'POSCAR' ! -name 'PROCAR' ! -name 'DOSCAR' ! -name 'OUTCAR' ! -name 'EIGENVAL' ! -name 'KPOINTS' -exec mv {} 213_PBAND/ \;

# Step 7: PDOS by element
vaspkit << EOF
215
EOF
mkdir -p 215_PBAND
find . -maxdepth 1 -type f ! -name 'INCAR' ! -name 'POSCAR' ! -name 'PROCAR' ! -name 'DOSCAR' ! -name 'OUTCAR' ! -name 'EIGENVAL' ! -name 'KPOINTS' -exec mv {} 215_PBAND/ \;


echo "                                                             "
echo "                                                             "
echo "==================== BAND data generated.... ==================="
echo "                                                             "
echo "                                                             "
