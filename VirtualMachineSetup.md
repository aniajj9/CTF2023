# Steps for setting up a Virtual Machine that hosts dockerized challenges
1. Install Docker
2. Install docker-compose (version >= 2)
3. Add user to docker group (sudo usermod -aG docker <your-username>)
4. Config github to use UNIX endings: git config --global core.autocrlf input, git config --global core.eol lf
6. Build all docker-compose files (run python3 docker-compose-recurse.py)
