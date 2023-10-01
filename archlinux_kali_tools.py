import requests
from time import sleep

KALI_TOOLS_URL = "https://www.kali.org/tools/all-tools/pages.json"
ARCH_PACKAGE_QUERY_URL = "https://archlinux.org/packages/search/json/"
SLEEP = 0.1  # small sleep time to avoid hitting a rate-limit on archlinux.org

# color escape codes
RED = "\033[0;31m"
GREEN = "\033[0;32m"
ORANGE = "\033[0;33m"
BLUE = "\033[0;34m"
NONE = "\033[0m"


def init_packages_list(filename: str) -> list[str]:
    try:
        with open(filename, "r") as f:
            packages = f.read().splitlines()
            return packages
    except IOError:
        return []


def write_results(filename: str, packages: list[str]) -> None:
    with open(filename, "w+") as f:
        packages.sort()
        for package in packages:
            f.write(f"{package}\n")


if __name__ == "__main__":
    tools = requests.get(KALI_TOOLS_URL).json()
    tools = [tool["value"] for tool in tools if "type" not in tool.keys()]
    tools.sort()

    available = init_packages_list("./available")
    missing = init_packages_list("./missing")
    ignored = init_packages_list("./ignored")

    count = 1
    for tool in tools:
        # prevent querying for packages with known status
        if tool in available:
            print(f"[+] {GREEN}{tool:<30}{NONE} ({count} of {len(tools)})")
            count += 1
            continue
        elif tool in missing:
            print(f"[-] {tool:<30} ({count} of {len(tools)})")
            count += 1
            continue
        elif tool in ignored:
            print(f"[i] {BLUE}{tool:<30}{NONE} ({count} of {len(tools)})")
            count += 1
            continue

        # query for any tools of unknown status
        try:
            pkgs_query_result = requests.get(
                ARCH_PACKAGE_QUERY_URL, params={"name": tool}
            ).json()
        except requests.exceptions.RequestException as e:
            print(f"Error while querying for tool {tool}: {e}")
            exit(1)
        else:
            if len(pkgs_query_result["results"]) != 0:
                print(f"[+] {GREEN}{tool:<30}{NONE} ({count} of {len(tools)})")
                available.append(tool)
            else:
                print(f"[-] {ORANGE}{tool:<30}{NONE} ({count} of {len(tools)})")
                missing.append(tool)
        sleep(SLEEP)
        count += 1

    # write results
    write_results(filename="./available", packages=available)
    write_results(filename="./missing", packages=missing)

    # create the install script
    with open("./install.sh", "w+") as f:
        f.write(f"""#!/bin/sh\nsudo pacman -S --needed {" ".join(available)}\n""")
