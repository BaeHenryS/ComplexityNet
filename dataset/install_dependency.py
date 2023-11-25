import re
import subprocess
from stdlib_list import stdlib_list

# Get a list of all standard library modules for Python 3.9
stdlib_modules = set(stdlib_list("3.9"))

# Read the "code" mbpp.jsonl file
with open('mbpp.jsonl', 'r') as file:
    # Initialize a set to store the unique package names
    packages = set()

    # Loop through each line in the file
    for line in file:
        # Use regular expressions to find the package names
        matches = re.findall(r'import\s+(\w+)', line)
        
        # Add the package names to the set, excluding standard library modules
        packages.update(match for match in matches if match not in stdlib_modules)

# Function to install packages using pip
def install_package(package):
    try:
        # Try installing the package
        subprocess.run(["pip", "install", package], check=True)
    except subprocess.CalledProcessError:
        try:
            # If installation fails, try importing the package
            __import__(package)
            print(f"{package} is already available.")
        except ImportError:
            print(f"Failed to install and import {package}. It may not be a valid package.")



# Install the packages
for package in packages:
    install_package(package)
