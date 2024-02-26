import os
import subprocess

def is_homebrew_installed():
    """Check if Homebrew is installed."""
    return subprocess.run(["which", "brew"], stdout=subprocess.PIPE).returncode == 0

def is_fswatch_installed():
    """Check if fswatch is installed."""
    return subprocess.run(["which", "fswatch"], stdout=subprocess.PIPE).returncode == 0


def install_homebrew():
    """Install Homebrew."""
    print("Installing Homebrew...")
    os.system('/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"')

def install_fswatch():
    """Install fswatch using Homebrew."""
    print("Installing fswatch...")
    os.system("brew install fswatch")

def create_print_script(script_path):
    """Create a bash script to handle printing of changed files."""
    print_script_content = """#!/bin/bash

# The file to be printed is passed as an argument to this script
file_to_print="$1"

# Check if the file is a PDF before printing
if [[ $file_to_print == *.pdf ]]
then
    echo "Printing: $file_to_print"
    lpr "$file_to_print"
else
    echo "The file is not a PDF, skipping: $file_to_print"
fi
"""
    with open(script_path, 'w') as file:
        file.write(print_script_content)
    os.chmod(script_path, 0o755)
    print(f"Print script created at {script_path}")

def main():
    # Check if Homebrew is installed, install if not
    if not is_homebrew_installed():
        install_homebrew()
    
    # Install fswatch
    install_fswatch()

    # Path where the print script will be saved
    script_path = os.path.expanduser("~/print_changed_files.sh")
    
    # Create the print handling script
    create_print_script(script_path)

dir = 
~/print_changed_files.sh
    print(f"fswatch -o {dir} | xargs -n1 -I{} {script} {}")

if __name__ == "__main__":
    main()

