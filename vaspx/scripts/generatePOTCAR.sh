#!/bin/bash

# Base directory where all the potential files are stored
BASE_DIR="~/vasp_pot/potPAW_PBE.54/"

# Expand the tilde (~) to the full home directory path
EXPANDED_BASE_DIR=$(eval echo $BASE_DIR)

# Check if at least one element is provided
if [ $# -lt 1 ]; then
    echo "Error: At least one element must be provided."
    exit 1
fi

# Initialize the POTCAR content
POTCAR_CONTENT=""

# Iterate over all positional arguments provided by the user
for ELEMENT in "$@"
do
    POTCAR_PATH="${EXPANDED_BASE_DIR}${ELEMENT}/POTCAR"
    
    # Check if the POTCAR file exists for the element
    if [ ! -f "$POTCAR_PATH" ]; then
        echo "Error: POTCAR file not found for element '$ELEMENT' at '$POTCAR_PATH'."
        exit 1
    fi
    
    # Concatenate the POTCAR file of the current element to POTCAR_CONTENT
    POTCAR_CONTENT="${POTCAR_CONTENT}$(cat "$POTCAR_PATH")\n"
done

# Create the final POTCAR file
echo -e "$POTCAR_CONTENT" > POTCAR

echo " "
echo "------> POTCAR file generated successfully. "
echo " "
echo "------> TITEL in the POTCAR file is/are."
echo " "
grep TITEL POTCAR
echo " "
echo "------> ENMAX(s) in the POTCAR file is/are."
echo " "
grep ENMAX POTCAR
echo " "
#echo "==================================================================="








