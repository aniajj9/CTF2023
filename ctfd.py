import argparse
import configparser
import json
import os
import re
from codecs import BOM_UTF8
from pathlib import Path

import requests

SETTINGS_FILE = os.path.join(os.path.expanduser('~'), ".ctfd_settings")

config = configparser.ConfigParser()
session = requests.Session()


def lstrip_bom(val, bom=BOM_UTF8):
    if val.startswith(bom):
        return val[len(bom):]
    else:
        return val


def ensure_config_exists():
    if not os.path.exists(SETTINGS_FILE):
        config["integration"] = {"url": "", "admin_token": ""}
        store_config()


def store_config():
    with open(SETTINGS_FILE, "w+") as f:
        config.write(f)


def parse_arguments():
    stored_url = config.get("integration", "url")
    stored_token = config.get("integration", "admin_token")

    parser = argparse.ArgumentParser()
    parser.add_argument("--token", type=str, help="the access token for the API access", default=stored_token)
    parser.add_argument("--url", type=str,
                        help="url to the instance, e.g. https://demo.ctfd.io. Without trailing slash",
                        default=stored_url)
    parser.add_argument("--prompt-each", action="store_true",
                        help="signal to promp and ask for challenge creation for each individual challenge")
    parser.add_argument("--scoring", type=str, choices=["dynamic", "standard"],
                        help="specify scoring mechanism hereby overwriting individual challenge files")
    parser.add_argument("path", type=str, help="directory to traverse for challenges")
    parser.add_argument("--directories-to-include", type=str,
                        help="directories of challenges (eg. misc/reversed/) that should be added/updated",
                        default=False)

    parsed = parser.parse_args()

    if parsed.token != stored_token or parsed.url != stored_url:
        config["integration"]["admin_token"] = parsed.token
        config["integration"]["url"] = parsed.url
        store_config()

    if parsed.directories_to_include == "":
        parsed.directories_to_include = False
    if parsed.directories_to_include:
        # Split the input string into a list using both commas and spaces as separators
        parsed.directories_to_include = [item.strip() for item in re.split(r'[,\s]+', parsed.directories_to_include)]

    return parsed


# Check if challenge is defined in CTFD.json correctly
def validate_challenge_info(challenge):
    valid = True
    keys = ["title", "description", "flag"]

    for key in keys:
        value = challenge.get(key)
        if value is None:
            print(f"Missing property '{key}'")
            valid = False
        elif not isinstance(value, str) or len(value) == 0:
            print(f"Invalid property '{key}', must be a string with some content")
            valid = False

    keys_arrays = ['downloadable_files', 'tags']
    for key in keys_arrays:
        value = challenge.get(key)
        if value is not None and not isinstance(value, list):
            print(f"Invalid property '{key}', must be an array!")
            valid = False

    if challenge.get("downloadable_files"):
        for f in challenge["downloadable_files"]:
            file_path = Path(challenge["directory"], f)
            if not file_path.exists():
                print(f"File {file_path} was not found")
                valid = False

    return valid


# Get challenges from given directory (the directory contains folders of categories, those folders contain challenges)
def get_local_challenges(directory):
    dirs = next(os.walk(directory))[1]  # Get 1st lvl directory name (= name of category: web, misc, pwn etc.)
    ignore = [".git"]
    challenges = []

    for category in dirs:
        if category in ignore:
            continue

        if settings.directories_to_include:  # If specific directories are specified
            if category not in [element.split('/')[0] for element in
                                settings.directories_to_include]:  # Skip if category not in chosen
                continue

        challenge_dirs = next(os.walk(Path(directory, category)))[1] # Get folders with challenges

        for dir in challenge_dirs:

            if settings.directories_to_include:  # If specific directories are specified
                if dir not in [element.split('/')[-1] for element in
                               settings.directories_to_include]:  # Skip if category not in chosen
                    continue
            filename = Path(directory, category, dir, "ctfd.json")  # Find the CTFD.json file
            if not filename.exists():
                print(f"File " + str(filename) + " does not exist. Ignoring for now!")
                continue

            with open(filename, "rb") as f:
                info = json.loads(lstrip_bom(f.read()))
                info["category"] = category
                info["directory"] = Path(directory, category, dir)
                challenges.append(info)

    return challenges


# Get all deployed challenges
def get_ctfd_challenges(url, access_token):
    auth_headers = {"Authorization": f"Token {access_token}"}
    return requests.get(url + "/api/v1/challenges?view=admin", json=True, headers=auth_headers).json()["data"]


def get_challenge_id_by_name(challenges, challenge_name):
    for challenge in challenges:
        if challenge["name"] == challenge_name:
            return challenge["id"]
    return None


def create_challenge(challenge, directory, url, access_token, scoring=None):
    auth_headers = {"Authorization": f"Token {access_token}"}

    data = {
        "name": challenge["title"],
        "category": challenge["category"],
        "description": challenge["description"],
        "type": challenge.get("type", "dynamic"),
        "value": challenge.get("points", 0),
        "state": "hidden",
        "initial": 500,
        "decay": 15,
        "minimum": 100,
    }

    if scoring in ["dymamic", "standard"]:
        data["type"] = scoring

    if data["type"] == "standard":
        del data["initial"], data["decay"], data["minimum"]
    elif data["type"] == "dynamic":
        del data["value"]

    if challenge.get("connection_info"):
        data["connection_info"] = challenge.get("connection_info")

    r = session.post(url + "/api/v1/challenges", json=data, headers=auth_headers)
    r.raise_for_status()

    challenge_data = r.json()
    challenge_id = challenge_data["data"]["id"]

    # Create flags
    data = {"content": challenge["flag"], "type": "static", "challenge_id": challenge_id}
    r = session.post(url + f"/api/v1/flags", json=data, headers=auth_headers)
    r.raise_for_status()

    # Create tags
    if challenge.get("tags"):
        for tag in challenge["tags"]:
            r = session.post(
                url + f"/api/v1/tags", json={"challenge_id": challenge_id, "value": tag},
                headers=auth_headers
            )
            r.raise_for_status()

    # Upload files
    if challenge.get("downloadable_files") and challenge.get("directory"):
        files = []
        for f in challenge["downloadable_files"]:
            file_path = Path(challenge["directory"], f)
            if file_path.exists():
                file_object = ("file", file_path.open(mode="rb"))
                files.append(file_object)
            else:
                print(f"File {file_path} was not found", fg="red")
                raise Exception(f"File {file_path} was not found")

        data = {"challenge_id": challenge_id, "type": "challenge"}

        r = session.post(url + f"/api/v1/files", files=files, data=data, headers=auth_headers)
        r.raise_for_status()

    # Set challenge state
    if challenge.get("state"):
       data = {"state": "hidden"}
       if challenge["state"] in ["hidden", "visible"]:
           data["state"] = challenge["state"]
       r = session.patch(f"/api/v1/challenges/{challenge_id}", json=data)
       r.raise_for_status()


def delete_challenge_by_id(challenge_id):
    auth_headers = {"Authorization": f"Token {settings.token}"}
    r = session.delete(settings.url + f"/api/v1/challenges/{challenge_id}", json={}, headers=auth_headers)
    r.raise_for_status()


def delete_challenge_by_name(challenges, challenge_name):
    challenge_id = get_challenge_id_by_name(challenges, challenge_name)
    if challenge_id is not None:
        delete_challenge_by_id(challenge_id)
    else:
        raise AttributeError(f"No challenge with name {challenge_name}")


def get_flag_id_by_challenge_id(challenge_id, session, url, auth_headers):
    flags_url = f"{url}/api/v1/challenges/{challenge_id}/flags"
    response = session.get(flags_url, headers=auth_headers)
    response.raise_for_status()

    data = response.json()
    flags = []
    if data.get("success") and data.get("data"):
        # Find the first flag entry and return its ID
        for flag_entry in data["data"]:
            flags.append(flag_entry.get("id"))

    return flags


def get_tag_id_by_challenge_id(challenge_id, session, url, auth_headers):
    flags_url = f"{url}/api/v1/challenges/{challenge_id}/tags"
    response = session.get(flags_url, headers=auth_headers)

    response.raise_for_status()

    data = response.json()
    tags = []
    if data.get("success") and data.get("data"):

        for tag_entry in data["data"]:
            tags.append(tag_entry.get("id"))

    return tags


def get_files_by_challenge_id(challenge_id, session, url, auth_headers):
    files_url = f"{url}/api/v1/challenges/{challenge_id}/files"
    response = session.get(files_url, headers=auth_headers)
    response.raise_for_status()
    data = response.json()

    if data.get("success") and data.get("data"):
        return data["data"]
    return []


def delete_file_by_id(file_id, session, url, auth_headers):
    file_url = f"{url}/api/v1/files/{file_id}"
    response = session.delete(file_url, headers=auth_headers)
    response.raise_for_status()
    print(f"File with ID {file_id} deleted successfully.")


def delete_files_by_challenge_id(challenge_id, session, url, auth_headers):
    files = get_files_by_challenge_id(challenge_id, session, url, auth_headers)
    for file_info in files:
        file_id = file_info.get("id")
        if file_id:
            delete_file_by_id(file_id, session, url, auth_headers)


def get_challenge_by_id(challenge_id, session, url, auth_headers):
    challenge_url = f"{url}/api/v1/challenges/{challenge_id}?view=admin"

    response = requests.get(challenge_url, headers=auth_headers, json=True)
    response.raise_for_status()
    data = response.json()
    if data.get("success") and data.get("data"):
        return data["data"]
    return None


def update_challenge(challenge_info, url, access_token):
    # Get challenge that we are updating, and its info from the URL
    existing_challenge = get_challenge_id_by_name(existing_challenges, challenge_info["title"])

    if existing_challenge:
        auth_headers = {"Authorization": f"Token {access_token}"}
        existing_challenge_details = get_challenge_by_id(existing_challenge, session, url, auth_headers)

        data = {
            "name": challenge_info["title"],
            "category": challenge_info["category"],
            "description": challenge_info["description"],
            "type": challenge_info.get("type", existing_challenge_details["type"]),
            "value": challenge_info.get("points", existing_challenge_details["value"]),
            "state": challenge_info.get("state", existing_challenge_details["state"]),
            "initial": challenge_info.get("initial", existing_challenge_details["initial"]),
            "decay": challenge_info.get("decay", existing_challenge_details["decay"]),
            "minimum": challenge_info.get("minimum", existing_challenge_details["minimum"])
        }

        if challenge_info.get("type") in ["dynamic", "standard"]:
            data["type"] = challenge_info["type"]

        if data["type"] == "standard":
            del data["initial"], data["decay"], data["minimum"]
        elif data["type"] == "dynamic":
            del data["value"]

        if challenge_info.get("connection_info"):
            data["connection_info"] = challenge_info["connection_info"]

        # Update challenge details
        update_url = f"{url}/api/v1/challenges/{existing_challenge}"
        r = session.patch(update_url, json=data, headers=auth_headers)
        r.raise_for_status()

        # Remove all old flags and add new one
        existing_flag_ids = get_flag_id_by_challenge_id(existing_challenge, session, url, auth_headers)
        if len(existing_flag_ids) > 0:
            for existing_flag_id in existing_flag_ids:
                flag_data = {"content": challenge_info["flag"], "type": "static", "challenge_id": existing_challenge}
                flag_url = f"{url}/api/v1/flags/{existing_flag_id}"
                r = session.patch(flag_url, json=flag_data, headers=auth_headers)
                r.raise_for_status()
                print(f"Flag for challenge '{challenge_info['title']}' updated successfully.")
        else:
            print(f"No existing flag found for challenge '{challenge_info['title']}'.")

        # Delete existing tags and post new ones
        existing_tag_ids = get_tag_id_by_challenge_id(existing_challenge, session, url, auth_headers)
        if len(existing_tag_ids) > 0:
            for existing_tag_id in existing_tag_ids:
                tag_url = f"{url}/api/v1/tags/{existing_tag_id}"
                r = session.delete(tag_url, headers=auth_headers)
                r.raise_for_status()
                print(f"Tags for challenge '{challenge_info['title']}' deleted successfully.")
        else:
            print(f"No existing tags found for challenge '{challenge_info['title']}'.")

        # Create new tags
        if challenge_info.get("tags"):
            for tag in challenge_info["tags"]:
                r = session.post(
                    url + f"/api/v1/tags", json={"challenge_id": existing_challenge, "value": tag},
                    headers=auth_headers
                )
                r.raise_for_status()

            print(f"Tags for challenge '{challenge_info['title']}' created successfully.")

        # Update downloadable files if provided
        if challenge_info.get("downloadable_files") and challenge_info.get("directory"):
            # Delete existing files
            delete_files_by_challenge_id(existing_challenge, session, url, auth_headers)
            # Upload new files
            files = []
            for f in challenge_info["downloadable_files"]:
                file_path = Path(challenge_info["directory"], f)
                if file_path.exists():
                    file_object = ("file", file_path.open(mode="rb"))
                    files.append(file_object)
                else:
                    print(f"File {file_path} was not found", fg="red")
                    raise Exception(f"File {file_path} was not found")

            file_data = {"challenge_id": existing_challenge, "type": "challenge"}
            r = session.post(f"{url}/api/v1/files", files=files, data=file_data, headers=auth_headers)
            r.raise_for_status()
        print(f"Challenge '{challenge_info['title']}' updated successfully.")
    else:
        print(f"No existing challenge found with the name '{challenge_info['title']}'.")


if __name__ == "__main__":
    ensure_config_exists()
    config.read(SETTINGS_FILE)

    settings = parse_arguments()

    if settings.url.endswith("/"):
        print("Instance url must not include a trailing slash!")
        exit(1)

    is_fully_configured = len(settings.token) > 0 and len(settings.url) > 0
    if is_fully_configured:
        existing_challenges = get_ctfd_challenges(settings.url, settings.token)
        existing_challenge_names = [c["name"] for c in existing_challenges]

        print("[+] Existing challenges:")
        [print(" - " + name) for name in existing_challenge_names]

    print("[+] Local challenges")
    challenges = get_local_challenges(settings.path)
    challenges.sort(key=lambda x: x["title"])  # sort them alphabetically
    for chal in challenges:
        print(chal["title"])

    print("[+] Validating challenges")
    for chal in challenges:
        validate_challenge_info(chal)

    if not is_fully_configured:
        print("System is not configured with url and access_token. Skipping creation")
        exit(1)

    print("[+] New challenges")
    for chal in challenges:
        if chal["title"] not in existing_challenge_names:
            print("-", chal["title"])

    print(settings.directories_to_include)
    # choice = input("Do you want to import the new challenges? (y/N) ").lower().strip()
    # if choice == "y":
    if True:
        print("[+] Creating challenges")
        for chal in challenges:
            if chal["title"] not in existing_challenge_names:
                if not settings.prompt_each:
                    create_challenge(chal, None, settings.url, settings.token, settings.scoring)
                    continue
                if input("Import challenge '{}'? (y/N) ".format(chal['title'])).lower() == "y":
                    create_challenge(chal, None, settings.url, settings.token, settings.scoring)
                    print("-", chal["title"], "imported")
            elif chal["title"] in existing_challenge_names:
                if not settings.prompt_each:
                    update_challenge(chal, settings.url, settings.token)
                    continue
                if input("Update challenge '{}'? (y/N) ".format(chal['title'])).lower() == "y":
                    update_challenge(chal, settings.url, settings.token)
                    print("-", chal["title"], "refreshed")
