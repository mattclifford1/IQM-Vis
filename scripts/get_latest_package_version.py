'''Get the latest version of a PyPi package'''
# Author: Matt Clifford <matt.clifford@bristol.ac.uk>
import urllib.request
import sys
import json
from packaging.version import Version

def versions(package_name):
    json_url = f"https://pypi.org/pypi/{package_name}/json"
    with urllib.request.urlopen(json_url) as url:
        data = json.load(url)
    versions = data["releases"].keys()
    return sorted(versions, key=Version, reverse=True)[0]


if __name__ == '__main__':
    sys.stdout.flush()
    print(versions("IQM-Vis"))
