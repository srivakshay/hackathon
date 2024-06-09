import json


def get_mappings():
    domain_mappings = {}
    data = json.load(open('../domains.json'))
    for domain in data["domain_mappings"]:
        for table in domain["tables"]:
            domain_mappings[table] = domain["domain"]
    return domain_mappings
