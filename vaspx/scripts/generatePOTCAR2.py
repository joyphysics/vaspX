import os

# Define the path to the POTCAR folder
POTCAR_path = "/home2/joydeep/vasp_pot/potPAW_PBE.54"

# Step 1: Check if POSCAR file exists
if not os.path.exists("POSCAR"):
    print("\n----> POSCAR file does not exist.\n")
    exit()
    

# Step 1.5: Check if POTCAR.spec file exists
if os.path.exists("POTCAR.spec"):
    choice = raw_input("\n----> POTCAR.spec file exists. Do you want to continue with this POTCAR.spec? (y/n): ").strip().lower()
    if choice in ['yes', 'y','Y']:
        # Read elements from the POTCAR.spec file
        with open("POTCAR.spec", 'r') as spec_file:
            elements = [line.strip() for line in spec_file.readlines() if line.strip()]
        
        print("\n===========================================")
        # Generate the command to run the generatePOTCAR.sh script with elements as arguments
        script_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "generatePOTCAR.sh")
        command = script_path + ' ' + ' '.join(elements)

        # Run the generatePOTCAR.sh script with the elements as positional arguments
        os.system(command)
        print("===========================================\n")
        exit()
    elif choice in ['no', 'n','N']:
        print("\n----> Continuing with the Python script.\n")
    else:
        print("\n----> Invalid input. Continuing with the Python script by default.\n")
        

# Step 2: Read elements from the POSCAR file
elements = []
with open("POSCAR", 'r') as file:
    lines = file.readlines()
    # Find the line containing element names
    for line in lines:
        if line.strip().split():
            # Assuming the line containing the elements is not numeric (otherwise it's atomic positions or counts)
            elements_line_index = lines.index(line) + 1
            if not any(char.isdigit() for char in lines[elements_line_index]):
                elements = lines[elements_line_index].split()
                break

if not elements:
    print("\n----> No elements found in the POSCAR file.\n")
    exit()

print("\n----> The element(s) in the POSCAR file is(are): {0}".format(', '.join(elements)))

# Step 3: Ask user to choose the specific POTCAR file for each element
selected_potcar_files = []

for element in elements:
    element_path = os.path.join(POTCAR_path, element)

    # List all available directories for the element
    options = [name for name in os.listdir(POTCAR_path) 
               if os.path.isdir(os.path.join(POTCAR_path, name)) and name.startswith(element)]

    if not options:
        print("\n----> No available directories for element '{0}' in {1}.".format(element, POTCAR_path))
        exit()

    print("\nAvailable options for {0}:".format(element))
    for i, option in enumerate(options, start=1):
        print("{0}: {1}".format(i, option))

    # Get user input to select a directory
    while True:
        choice = raw_input("Choose the option number for element '{0}': ".format(element))  # Use raw_input() for Python 2
        if choice.isdigit() and 1 <= int(choice) <= len(options):
            selected_directory = os.path.join(POTCAR_path, options[int(choice) - 1])
            potcar_file_path = os.path.join(selected_directory, 'POTCAR')
            if os.path.exists(potcar_file_path):
                selected_potcar_files.append(potcar_file_path)
                break
            else:
                print("\n----> POTCAR file not found in the selected directory.")
        else:
            print("\n----> Invalid choice. Please choose a valid option number.")



# Step 4: Merge the selected POTCAR files in the correct order
with open('POTCAR', 'w') as potcar_out:
    for potcar_file in selected_potcar_files:
        with open(potcar_file, 'r') as potcar_in:
            potcar_out.write(potcar_in.read())

print("\n==========================================")
print("\n----> POTCAR file generated successfully.")



# Step 5: Display TITEL and ENMAX information from the generated POTCAR file
print("\n----> TITEL(s) in the POTCAR file is(are):\n")

with open('POTCAR', 'r') as potcar_file:
    for line in potcar_file:
        if 'TITEL' in line:
            print(line.strip())

print("\n----> ENMAX(s) in the POTCAR file is(are):\n")

with open('POTCAR', 'r') as potcar_file:
    for line in potcar_file:
        if 'ENMAX' in line:
            print(line.strip())

print("\n==========================================\n")
