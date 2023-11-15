# CTF 2023 Challenges

This repository contains the challenges for Capture The Flag (CTF) 2023, and the workflows for their deployment.   

## Challenges

The CTF 2023 challenges are categorized into directories that match their respective challenge categories. For example, the `/web/coffee/` directory contains files for the "Coffee" challenge, which is classified as a Web challenge.

Each challenge is required to include a `ctfd.json` file, following the specifications provided in [ctfd-cli](https://github.com/eskildsen/ctfd-cli).

## Task Deployment
       
Challenges fall into two categories:

#### Tasks Requiring Web Access

These tasks can be hosted on a CTFd instance.

#### Tasks Without Web Access

These tasks are also hosted on a CTFd instance but do not require public web access.

Web tasks are defined using `docker-compose.yml` configuration files and are deployed on an Azure Virtual Machine. This VM runs Docker containers, ensuring a controlled and isolated environment for these challenges.

The CTFd instance itself is hosted on Azure.

## Workflows

This repository includes two GitHub workflows triggered by `PUSH` events to the `MAIN` branch. These workflows can be found in the `.github/workflows` directory:

1. **deploy-docker-containers-on-vm.yml**:
   - This workflow establishes an SSH connection to an Azure VM.
   - It fetches the current GitHub repository onto the VM.
   - The VM executes the `docker-compose-recurse.py` script, which scans the repository's files. When a `docker-compose.yml` file is found, the script uses Docker to build a container.
   - This workflow is activated by any `PUSH` to the `MAIN` branch, ensuring that all containers on the VM are redeployed with each push.
  
   Assumptions:
   a. There are no conflicts while performing `git pull` on the virtual machine
   b. If there are new tasks added, or the ports for already existing ones change, the ports are open on the networking section of Azure VM in Azure (manually add them)
   

3. **redeploy-ctfd-tasks.yml**:
   - This workflow runs the `ctfd.py` script, which is a modified version of the original script created by [ctfd-cli](https://github.com/eskildsen/ctfd-cli).
   - It triggers on any `PUSH` event to the `MAIN` branch.
   - The workflow identifies the files that changed between the current push and the previous version of the repository.
   - It notes the directories in the format `/category/task/` (e.g., `/web/coffee/`) where differences are present.
   - If a task is not already part of the CTFd instance, the script adds it.

## Scripts 
### `docker-compose-recurse.py`

Python script that finds all `docker-compose.yml` files in a directory and builds them using the "docker-compose up -d --build" command.

**Parameters:**

- `[optional] --path`: Path to the root directory to iterate through. Default: working directory.

### `ctfd.py`

Python script, modified from [ctfd-cli](https://github.com/eskildsen/ctfd-cli).

It iterates through the challenges in a directory, and compares them **by name** with the challenges already present in the CTFd instance.

If challenge is missing, it adds it.

If challenge is present, it updates it.

It also includes a function (commented) to remove a challenge from CTFd instance.

**Parameters:**

- `--token`: Admin's access token obtained from the CTFd instance's Settings -> Admin token.
- `--url`: URL to the CTFd instance.
- `path`: Path to the directory containing challenges.
- `[optional] --directories-to-include`: Comma and/or space-separated string containing directories of challenges to include in the update (ADD/UPDATE) (`category/task` format, e.g., `web/coffee` - include only one / !). Tasks in other directories will be skipped. This flag is primarily designed to be used by the GitHub workflow, where the workflow sets it to the list of tasks that were changed with the current push and, therefore, need to be redeployed.

