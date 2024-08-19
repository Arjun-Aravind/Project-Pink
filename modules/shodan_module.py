import shodan
import os
import fileinput
import json
from datetime import datetime
from utils.mongo_utils import save_to_mongo

def filter_fields(result):
    """ Filter required fields from the result """
    return {
        "data": result.get("data"),
        "org": result.get("org"),
        "isp": result.get("isp"),
        "ip_str": result.get("ip_str"),
        "location": result.get("location"),
        "http": result.get("http"),
        "port": result.get("port"),
        "status": "Open"
    }

def search_shodan(organization, output_dir, shodan_api_key):
    api = shodan.Shodan(shodan_api_key)
    replace_org = "${organization}"  # Replace part in dork file for organization.

    with open(r'dorks.txt', 'r') as file:  # dorks.txt is the file which has all dorks.
        dorks = file.read()
        dorks = dorks.replace(replace_org, organization)

    with open(r'tmp.txt', 'w') as file:  # Just a temporary file for code, need to be always present in directory.
        file.write(dorks)

    for line in fileinput.FileInput(files="tmp.txt"):
        name = line.split("::")[0]
        dork = line.split("::")[1].strip()
        print(f"Using dork: {dork}")  # Print the dork being used

        try:
            print(f"Searching Shodan with dork: {dork}, page: 1")
            shodan_search = api.search(dork, page=1)
            total_results = shodan_search['matches']
            print(f"Page 1 results: {len(shodan_search['matches'])} matches")
        except shodan.APIError as e:
            print(f"Shodan API error: {e}")
            total_results = []

        for result in total_results:
            filtered_result = filter_fields(result)
            unique_fields = {
                "organization": organization,
                "dork": dork,
                "name": name,
                "ip_str": filtered_result["ip_str"]
            }
            save_to_mongo("shodan_results", unique_fields, filtered_result)

if __name__ == "__main__":
    config_file_path = 'config.json'
    with open(config_file_path) as config_file:
        config = json.load(config_file)

    organization = "Nykaa"  # Example organization name
    output_dir = os.path.join(os.getcwd(), "Recon")
    shodan_api_key = config["shodan_api_key"]

    search_shodan(organization, output_dir, shodan_api_key)
