#!/bin/bash

#Step 1: Create the 'DOS_data' folder if it doesn't exist
mkdir -p DOS_data

# Step 2: Copy the necessary files to the 'DOS_data' folder
cp PROCAR DOSCAR INCAR POSCAR DOS_data/

# Step 3: Run VASPkit with the option 111
cd DOS_data
vaspkit << EOF
111
EOF

# Step 4: Create a new directory '111_TDOS'
mkdir -p 111_TDOS

# Step 5: Move all newly created files by VASPkit to '111_TDOS', except INCAR, POSCAR, PROCAR, and DOSCAR
find . -maxdepth 1 -type f ! -name 'INCAR' ! -name 'POSCAR' ! -name 'PROCAR' ! -name 'DOSCAR' -exec mv {} 111_TDOS/ \;


# Step 6: PDOS
vaspkit << EOF
113
EOF
mkdir -p 113_PDOS
find . -maxdepth 1 -type f ! -name 'INCAR' ! -name 'POSCAR' ! -name 'PROCAR' ! -name 'DOSCAR' -exec mv {} 113_PDOS/ \;


# Step 7: LDOS
vaspkit << EOF
116
EOF
mkdir -p 116_LDOS
find . -maxdepth 1 -type f ! -name 'INCAR' ! -name 'POSCAR' ! -name 'PROCAR' ! -name 'DOSCAR' -exec mv {} 116_LDOS/ \;



echo "                                                             "
echo "                                                             "
echo "==================== DOS data generated.... ==================="
echo "                                                             "
echo "                                                             "

