#!/usr/bin/env python3
import os
import subprocess
import argparse

# Function to recursively search for docker-compose.yml files
def find_docker_compose_files(directory):
    for root, dirs, files in os.walk(directory):
        if 'docker-compose.yml' in files:
            docker_compose_path = os.path.join(root, 'docker-compose.yml')
            yield docker_compose_path

# Function to run Docker Compose for a given file
def run_docker_compose(file_path):
    subprocess.run(['docker-compose', '-f', file_path, 'up', '-d', '--build'])

def main(root_directory):
    # Set execute permissions for all .sh files
    subprocess.run(['find', root_directory, '-type', 'f', '-name', '*.sh', '-exec', 'chmod', '+x', '{}', ';'])

    for docker_compose_file in find_docker_compose_files(root_directory):
        print(f"Running Docker Compose for: {docker_compose_file}")
        run_docker_compose(docker_compose_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Search for and run Docker Compose files.")
    parser.add_argument("--path", default=os.getcwd(), help="Root directory to start the search (default: current working directory)")
    args = parser.parse_args()
    main(args.path)
