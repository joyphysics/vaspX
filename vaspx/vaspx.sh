#!/bin/bash

# Get the script directory
script_dir="$(cd "$(dirname "$0")" && pwd)"
"$script_dir/scripts/logo1.sh"


# Display the menu options in a two-column format
echo -e "\n-----------------------------------------------------------------------"
echo "                                VASP             "
echo "-----------------------------------------------------------------------"
echo " 1> Setup Relax Calculation           2> Generate INCAR file  "
echo " 3> Generate POTCAR file              4> Generate KPOINTS file "
echo " 5> SCF calculation                   6> DOS calculation  "
echo " 7> Band structure (3D)               8> Band structure (2D)"
echo " 9> Delete vasp generated files      10> Generate DOS data"
echo "11> Generate Band data               12> Energy vs Volume plot "
echo "13> ENCUT Convergence Test           14> K Point Convergence Test "
echo -e "\n-----------------------------------------------------------------------"
echo "                              WANNIER90             "
echo "-----------------------------------------------------------------------"
echo "21> Wannier Input file               22> Wannier Band Structure 3D "
echo "23> Wannier Band Structure 2D        24> Wannier Band Structure 3D (spin)  "
echo "25> Wannier Band Structure 2D (spin) 26> soon...  "
echo -e "\n-----------------------------------------------------------------------"
echo "0> Exit (To exit VASPX.)"
echo "-----------------------------------------------------------------------"

# Prompt for user input
read -p "Enter your choice: " choice

# Execute the corresponding script based on the user's choice
case $choice in
  1) python "$script_dir/scripts/setupRELAX.py" ;;
  2) python "$script_dir/scripts/generateINCAR2.py" ;;
  3) python "$script_dir/scripts/generatePOTCAR2.py" ;;
  4) python "$script_dir/scripts/generateKPOINTS.py" ;;
  5) "$script_dir/scripts/Relax2SCF.sh" ;;
  6) python "$script_dir/scripts/SCF2DOS.py" ;;
  7) python "$script_dir/scripts/SCF2BAND_3D.py" ;;
  8) python "$script_dir/scripts/SCF2BAND_2D.py" ;;
  9) "$script_dir/scripts/delete.sh" ;; 
  10) "$script_dir/scripts/DOS_data.sh" ;;
  11) "$script_dir/scripts/BAND_data.sh" ;;
  12) python "$script_dir/scripts/EvsV.py" ;;
  13) python "$script_dir/scripts/ENCUT_convergence.py" ;;
  14) python "$script_dir/scripts/k_convergence.py" ;;
  21) python "$script_dir/scripts/wannier_input.py" ;;
  22) python "$script_dir/scripts/wannier_band3D.py" ;;
  23) python "$script_dir/scripts/wannier_band2D.py" ;;
  24) python "$script_dir/scripts/wannier_spin_band3D.py" ;;
  25) python "$script_dir/scripts/wannier_spin_band2D.py" ;;
  0) echo -e "\nSee you again...\n"; exit 0 ;;
  *) echo "Invalid choice. Please try again." ;;
esac

# Loop to return to menu after execution
#"$script_dir/vaspx.sh"
