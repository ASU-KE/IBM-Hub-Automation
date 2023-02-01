# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

import requests
import argparse
import sys
import json
from auth import get_access_token

API_URL = "https://api-qcon.quantum-computing.ibm.com/api"

parser = argparse.ArgumentParser(description="Retrieve backend information from one Project and copy to another in the same Group")
parser.add_argument('hub', type=str, help="The Hub to retreive backend information from")
parser.add_argument('group', type=str, help="Name of the group to retrieve backends from")
parser.add_argument('from_proj', type=str, help="Name of the project to retrieve backends from")
parser.add_argument('to_proj', type=str, help="Name of the project to copy backends to")

args = parser.parse_args()

hub = args.hub
group = args.group
from_project = args.from_proj
to_project = args.to_proj

access_token = get_access_token()
headers = {'X-Access-Token': access_token}

# Setting both the from and to URLs 
from_url = f'{API_URL}/Network/{hub}/Groups/{group}/Projects/{from_project}/devices'
to_url = f'{API_URL}/Network/{hub}/Groups/{group}/Projects/{to_project}/devices'

# Make API request/handle errors to populate the from project backend list
try:
    response = requests.get(url=from_url, headers=headers)
    response.raise_for_status()  # Checks if the request returned an error
except requests.HTTPError as http_err:
    sys.exit(f"Could not retrieve backend information in {s} due to HTTPError: {http_err}")
except Exception as err:
    sys.exit(f"Could not retrieve backend information in {s} due to: {err}")

data = response.json()

print(data)
sys.exit(0)

# Populate the backends list with just the backend names
backends = []
for obj in data:
	backends.append(obj['backend_name'])
# print(backends)

priority = 1000

for obj in backends:       
    try:
        response = requests.post(to_url, headers=headers, json={'name': obj, 'priority': priority})
        s = f'{hub} (group: {group} and project: {to_project})'
        response.raise_for_status()
    except requests.HTTPError as http_err:
        sys.exit(f"Could not edit backends in {s} due to HTTPError: {http_err}")
    except Exception as err:
        sys.exit(f"Could not edit backends in {s} due to: {err}")

# try:
# 	if action == 'add':
# 		if project is not None:
# 			url = f'{API_URL}/Network/{hub}/Groups/{group}/Projects/{project}/devices'
# 		else:
# 			url = f'{API_URL}/Network/{hub}/Groups/{group}/devices'

# 		response = requests.post(url, headers=headers, json={'name': backend, 'priority': priority})
# 	else:
# 		if project is not None:
# 			url = f'{API_URL}/Network/{hub}/Groups/{group}/Projects/{project}/devices/{backend}'
# 		else:
# 			url = f'{API_URL}/Network/{hub}/Groups/{group}/devices/{backend}'

# 		response = requests.delete(url, headers=headers)

# 	s = f'{hub} (group: {group} and project: {project})'
# 	response.raise_for_status()
# except requests.HTTPError as http_err:
# 	sys.exit(f"Could not edit backends in {s} due to HTTPError: {http_err}")
# except Exception as err:
# 	sys.exit(f"Could not edit backends in {s} due to: {err}")