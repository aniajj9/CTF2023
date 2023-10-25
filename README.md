# CTF 2023 Challenges

This repository contains the challenges for Capture The Flag (CTF) 2023, and the workflows for their deployment.

## Challenges

The CTF 2023 challenges are categorized into directories that match their respective challenge categories. For example, the `/web/coffee/` directory contains files for the "Coffee" challenge, which is classified as a Web challenge.

Each challenge is required to include a `ctfd.json` file, following the specifications provided in [ctfd-cli](https://github.com/eskildsen/ctfd-cli).

## Task Deployment

Challenges fall into two categories:

### Tasks Requiring Web Access

These tasks can be hosted on a CTFd instance.

### Tasks Without Web Access

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

2. **redeploy-ctfd-tasks.yml**:
   - This workflow runs the `ctfd.py` script, which is a modified version of the original script created by [ctfd-cli](https://github.com/eskildsen/ctfd-cli).
   - It triggers on any `PUSH` event to the `MAIN` branch.
   - The workflow identifies the files that changed between the current push and the previous version of the repository.
   - It notes the directories in the format `/category/task/` (e.g., `/web/coffee/`) where differences are present.
   - If a task is not already part of the CTFd instance, the script adds it.
