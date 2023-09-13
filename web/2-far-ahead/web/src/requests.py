import subprocess

def get(url):
    try:
        return subprocess.check_output(["curl", "-s", "-q", "--url", url], shell=False, stderr=subprocess.STDOUT)
    except Exception as err:
        return None
