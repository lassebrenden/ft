#!/usr/bin/env python3


"""
Configuration
"""


# Import packages
import json
import math
import os
import requests
import shutil
import time

# Define constants
LICENSE_TYPES = [
    "ALTINVAIF",
    "BANK",
    "DEPOTNY",
    "FINANSKONS",
    "FOAVALIN",
]
LICENSE_TYPE_STRING = "&".join(
    [f"licenceTypes={license_type}" for license_type in LICENSE_TYPES]
)
API_URL = f"https://api.finanstilsynet.no/registry/v1/legal-entities/filter?{LICENSE_TYPE_STRING}"
MAX_REQUESTS_PER_SECOND = 5
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(ROOT_PATH, "data")
TEMP_PATH = os.path.join(ROOT_PATH, "tmp")

# Ensure directories exist
os.makedirs(DATA_PATH, exist_ok=True)
os.makedirs(TEMP_PATH, exist_ok=True)


"""
Definitions
"""


# Generate date string
def get_datestr():
    return time.strftime("%Y%m%d")


# Load most recent data file
def load_data(term="ft_data"):
    try:
        files = sorted(
            (
                f
                for f in os.listdir(DATA_PATH)
                if f.startswith(term) and "latest" not in f and f.endswith(".json")
            ),
            reverse=True,
        )
        if not files:
            raise FileNotFoundError(
                f"No matching files found in {DATA_PATH} for term '{term}'"
            )
        file_path = os.path.join(DATA_PATH, files[0])
        print(f"Loading data from {files[0]}...")
        with open(file_path, mode="r", encoding="utf8") as infile:
            return json.load(infile)
    except Exception as e:
        print(f"Error loading data: {e}")
        return None


# Lookup entity by ID
def lookup_entity(data, entity_id):
    return next((item for item in data if item["legalEntityId"] == entity_id), None)


# Make initial request to the API to get the total number of pages
def data_length():
    response = requests.get(API_URL)
    response_json = response.json()
    total_hits = response_json.get("total", 0)
    per_page = response_json.get("hitsReturned", 0)
    if per_page == 0:
        return 0
    pages = math.ceil(total_hits / per_page)
    return pages


# Pull data from the API
def pull_data():
    start = time.time()
    length = data_length()
    for page in range(1, length + 1):
        print(f"Pulling page {page} of {length}...")
        timer = time.time()
        response = requests.get(f"{API_URL}&page={page}")
        response.raise_for_status()  # Raise an error for HTTP failures
        file_path = os.path.join("tmp", f"ft_data_{page}.json")
        with open(file_path, mode="w", encoding="utf8") as outfile:
            json.dump(response.json(), outfile, indent=2)
        elapsed = time.time() - timer
        sleep_time = max(0, (1 / MAX_REQUESTS_PER_SECOND) - elapsed)
        time.sleep(sleep_time)  # Only sleep if needed
    print(f"Finished pulling data in {time.time() - start:.2f} seconds.")


# Merge data from the API
def merge_data():
    start = time.time()
    tmp_files = [
        f
        for f in os.listdir(TEMP_PATH)
        if f.startswith("ft_data") and f.endswith(".json")
    ]
    if not tmp_files:
        print("No temporary data files found to merge.")
        return
    tmp_data = []
    for index, page in enumerate(tmp_files):
        print(f"Merging page {index + 1} of {len(tmp_files)}...")
        with open(f"{TEMP_PATH}/{page}", mode="r", encoding="utf8") as infile:
            infile_json = json.load(infile)
            tmp_data.extend(infile_json.get("legalEntities", []))
    with open(
        f"{DATA_PATH}/ft_data_{get_datestr()}.json", mode="w", encoding="utf8"
    ) as outfile:
        json.dump(tmp_data, outfile, indent=2)
    print(f"Finished merging data in {time.time() - start:.2f} seconds.")


# Export entities from data files
def export_entities():
    start = time.time()
    data = load_data()
    if not data:
        print("No data loaded. Export aborted.")
        return
    report_data = []
    for index, item in enumerate(data, start=1):
        print(f"Processing entity {index} of {len(data)}...")
        report_data.append(
            {
                "entity_id": item.get("legalEntityId"),
                "entity_ft_id": item.get("finanstilsynetId"),
                "entity_vat_id": item.get("organisationNumber"),
                "entity_name": item.get("name", "").upper(),
                "entity_type": item.get("legalEntityType", "").upper(),
                "entity_location": "|".join(
                    address["postalLocation"].upper()
                    for address in item.get("addresses", [])
                    if "postalLocation" in address and address["postalLocation"]
                ),
                "entity_licenses": "|".join(
                    license["licenceType"]["code"]
                    for license in item.get("licences", [])
                    if "licenceType" in license and "code" in license["licenceType"]
                ),
                "entity_services": "|".join(
                    str(service["serviceId"])
                    for license in item.get("licences", [])
                    for service in license.get("services", [])
                    if "serviceId" in service
                ),
                "entity_lookup": f"https://www.finanstilsynet.no/virksomhetsregisteret/detalj/?id={item.get('legalEntityId')}",
            }
        )
    output_file = os.path.join(DATA_PATH, f"ft_entities_{get_datestr()}.json")
    with open(output_file, mode="w", encoding="utf8") as outfile:
        json.dump(report_data, outfile, indent=2)
    print(f"Finished exporting entities in {time.time() - start:.2f} seconds.")


# Export funds from data files
def export_funds():
    start = time.time()
    data = load_data()
    if not data:
        print("No data loaded. Export aborted.")
        return
    report_data = []
    for index, item in enumerate(data, start=1):
        print(f"Processing entity {index} of {len(data)}...")
        for license in item.get("licences", []):
            if license.get("licenceType", {}).get("code") != "ALTINVAIF":
                continue
            if any(
                role.get("description", {}).get("english") == "Main fund"
                for role in (license.get("roles") or [])
            ):
                continue
            item_data = {
                "fund_id": item.get("legalEntityId"),
                "fund_ft_id": item.get("finanstilsynetId"),
                "fund_vat_id": item.get("organisationNumber"),
                "fund_name": item.get("name", "").upper(),
                "fund_registered": license.get("registeredDate", "")[:10],
                "fund_authority_name": license.get("supervisoryAuthority", {})
                .get("legalEntityName", "")
                .upper(),
                "fund_authority_country": license.get("supervisoryAuthority", {})
                .get("country", {})
                .get("iso3"),
                "manager_id": None,
                "manager_name": None,
                "manager_country": None,
                "depositary_id": None,
                "depositary_name": None,
                "depositary_country": None,
            }
            for role in license.get("roles") or []:  # Ensure roles is always a list
                if role.get("description", {}).get("english") == "Fund manager":
                    for entity in role.get("relatedEntities", []):
                        item_data["manager_id"] = entity.get("legalEntityId")
                        item_data["manager_name"] = entity.get(
                            "legalEntityName", ""
                        ).upper()
                        item_data["manager_country"] = entity.get("country", {}).get(
                            "iso3"
                        )
                        manager_data = lookup_entity(data, entity["legalEntityId"])
                        if manager_data:
                            for license in manager_data.get("licences", []):
                                for role in license.get("roles") or []:
                                    if (
                                        role.get("description", {}).get("english")
                                        == "Depositar"
                                    ):
                                        for entity in role.get("relatedEntities", []):
                                            item_data["depositary_id"] = entity.get(
                                                "legalEntityId"
                                            )
                                            item_data["depositary_name"] = entity.get(
                                                "legalEntityName", ""
                                            ).upper()
                                            item_data["depositary_country"] = (
                                                entity.get("country", {}).get("iso3")
                                            )
            report_data.append(item_data)
    output_file = os.path.join(DATA_PATH, f"ft_funds_{get_datestr()}.json")
    with open(output_file, mode="w", encoding="utf8") as outfile:
        json.dump(report_data, outfile, indent=2)
    print(f"Finished exporting funds in {time.time() - start:.2f} seconds.")


# Export managers from data files
def export_managers():
    start = time.time()
    data = [
        i for i in load_data("ft_funds") if i.get("fund_authority_country") == "NOR"
    ]
    full_data = load_data()
    if not data:
        print("No Norwegian fund managers found. Export aborted.")
        return
    report_data = {}
    for index, item in enumerate(data, start=1):
        print(f"Processing entity {index} of {len(data)}...")
        manager_id = item.get("manager_id")
        if not manager_id or manager_id in report_data:
            continue
        report_data[manager_id] = {
            "manager_id": manager_id,
            "manager_name": item.get("manager_name"),
            "manager_country": item.get("manager_country"),
            "number_of_funds": sum(
                1 for i in data if i.get("manager_id") == manager_id
            ),
            "depositary_id": None,
            "depositary_name": None,
            "depositary_country": None,
            "entity_lookup": f"https://www.finanstilsynet.no/virksomhetsregisteret/detalj/?id={manager_id}",
        }
        manager_data = lookup_entity(full_data, manager_id)
        if manager_data:
            for license in manager_data.get("licences", []):
                for role in (
                    license.get("roles") or []
                ):  # Ensures roles is always a list
                    if role.get("description", {}).get("english") == "Depositar":
                        for entity in role.get("relatedEntities", []):
                            report_data[manager_id].update(
                                {
                                    "depositary_id": entity.get("legalEntityId"),
                                    "depositary_name": entity.get(
                                        "legalEntityName", ""
                                    ).upper(),
                                    "depositary_country": entity.get("country", {}).get(
                                        "iso3"
                                    ),
                                }
                            )
                            break  # Stop after first valid depositary
    output_file = os.path.join(DATA_PATH, f"ft_managers_{get_datestr()}.json")
    with open(output_file, mode="w", encoding="utf8") as outfile:
        json.dump(list(report_data.values()), outfile, indent=2)
    print(f"Finished exporting managers in {time.time() - start:.2f} seconds.")


# Copy most recent data files to "latest" files
def export_latest():
    file_types = ["ft_data", "ft_entities", "ft_funds", "ft_managers"]
    for file_type in file_types:
        files = sorted(
            (
                f
                for f in os.listdir(DATA_PATH)
                if f.startswith(file_type)
                and f.endswith(".json")
                and not f.endswith("_latest.json")
            ),
            reverse=True,
        )
        if not files:
            print(f"No files found for {file_type}, skipping...")
            continue
        src_file = os.path.join(DATA_PATH, files[0])
        dst_file = os.path.join(DATA_PATH, f"{file_type}_latest.json")
        print(f"Copying {files[0]} to {dst_file}...")
        shutil.copyfile(src_file, dst_file)


"""
Run application
"""


def main():
    pull_data()
    merge_data()
    export_entities()
    export_funds()
    export_managers()
    export_latest()


if __name__ == "__main__":
    main()
