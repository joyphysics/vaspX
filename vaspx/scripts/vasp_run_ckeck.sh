#!/bin/bash

# Path to the OUTCAR file
OUTCAR="SCF/OUTCAR"

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
        echo "VASP SCF run has finished successfully."
        break
    else
        echo "VASP SCF run is still in progress. Checking again in few minutes..."
        qstat
    fi
done
