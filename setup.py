from setuptools import setup, find_packages

# Function to parse the dependencies from requirements.txt
def parse_requirements(file_name):
    with open(file_name, 'r') as f:
        return [line.strip() for line in f if line and not line.startswith('#')]

# Load dependencies from requirements.txt
requirements = parse_requirements('requirements.txt')

setup(
    name="prozees",
    version="0.0.0-dev",
    packages=find_packages(),
    install_requires=requirements,  # Uses requirements.txt for dependencies
)
