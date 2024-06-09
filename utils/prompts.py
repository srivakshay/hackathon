
from utils import extract_table_names, read_domains


def get_spring_boot_prompt(spring_boot_version, java_version):
    return "Generate spring boot " + spring_boot_version + " and Java " + java_version + (
        "having \n 1. Application with REST endpoints"
        "\n 2. Exception handling, "
        "\n 3. Unit test cases"
        "\n 4. pom.xml")


def get_domain_prompt_from_mysql(schema, procname):
    domain_mappings = read_domains.get_mappings()
    tables = extract_table_names.get_from_mysql(schema, procname)
    return __generate_prompt(domain_mappings, tables)


def get_domain_prompt_from_file(filepath):
    domain_mappings = read_domains.get_mappings()
    tables = extract_table_names.get_table_names_from_file(filepath)
    return __generate_prompt(domain_mappings, tables)


def __generate_prompt(domain_mappings, tables):
    domain_tables = {}
    for table in tables:
        if domain_mappings[table] not in domain_tables:
            domain_tables[domain_mappings[table]] = [table]
        else:
            domain_tables[domain_mappings[table]].append(table)
    prompt = ""
    domain_tables_copy = domain_tables.copy()
    for domain in domain_tables:
        prompt += "Generate code with " + ",".join(domain_tables[domain]) + " as one spring boot application \n"
        domain_tables_copy.pop(domain)
        if len(domain_tables_copy) > 0:
            prompt += "and "
    return prompt


