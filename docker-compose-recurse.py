import os
import subprocess

# Function to recursively search for docker-compose.yml files
def find_docker_compose_files(directory):
    for root, dirs, files in os.walk(directory):
        if 'docker-compose.yml' in files:
            docker_compose_path = os.path.join(root, 'docker-compose.yml')
            yield docker_compose_path

# Function to run Docker Compose for a given file
def run_docker_compose(file_path):
    subprocess.run(['docker-compose', '-f', file_path, 'up', '-d'])

# Specify the root directory to start the search
root_directory = 'C:\\Users\\bduago\\OneDrive - Bankdata\\Skrivebord\\git\\CTF2023\\'

for docker_compose_file in find_docker_compose_files(root_directory):
    print(f"Running Docker Compose for: {docker_compose_file}")
    run_docker_compose(docker_compose_file)
