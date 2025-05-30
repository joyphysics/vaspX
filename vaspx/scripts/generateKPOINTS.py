import os
import subprocess

def main():
    # Check if the KPOINTS file exists
    if os.path.isfile('KPOINTS'):
        with open('KPOINTS', 'r') as file:
            content = file.read()
            print("\nKPOINTS file already exists. Content of the file:")
            print("\n==========================================")
            print(content)
            print("==========================================\n")
            
        # Ask user if they want to continue with the existing KPOINTS file
        user_input = raw_input("Do you want to continue with the existing KPOINTS file? (y/n): ")
        if user_input.lower() == 'y':
            print("\n----> Continuing with the existing KPOINTS file.\n")
            return
        elif user_input.lower() != 'n':
            print("Invalid input. Exiting.")
            return
    
    # If the user chose not to use the existing file, or if the file didn't exist
    print("\nChoose the type of KPOINTS file to create:")
    print("a) Monkhorst-Pack KPOINTS")
    print("b) Gamma-centered KPOINTS")

    choice = raw_input("Enter your choice (a/b): ")

    if choice.lower() == 'a':
        # Monkhorst-Pack KPOINTS
        generate_kpoints_monkhorst_pack()
    elif choice.lower() == 'b':
        # Gamma-centered KPOINTS
        generate_kpoints_gamma_centered()
    else:
        print("Invalid choice. Exiting.")
        return

    print("\n----> KPOINTS file generated successfully.\n")
    
    print("-----------------------------------------------------------------------\n")

def generate_kpoints_monkhorst_pack():
    # Run vaspkit in background to generate Monkhorst-Pack KPOINTS
    process = subprocess.Popen(['vaspkit'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process.communicate(input="102\n1\n0.04\n")

def generate_kpoints_gamma_centered():
    # Run vaspkit in background to generate Gamma-centered KPOINTS
    process = subprocess.Popen(['vaspkit'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process.communicate(input="102\n2\n0.04\n")
    


if __name__ == '__main__':
    main()
