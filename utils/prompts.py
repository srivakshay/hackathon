from utils import extract_table_names, read_domains


def get_spring_boot_prompt(spring_boot_version, java_version):
    return "Convert stored procedure code into executable spring boot application coded with spring boot version " + spring_boot_version + " and Java " + java_version + (
        " having \n 1. Application with REST endpoints with separate Controller, Service and Repository layer all implementation should have migrated code"
        "\n 2. Exception handling, "
        "\n 3. Unit test cases"
        "\n 4. Code should have inbuilt sql queries"
        "\n 5. Open API Specification YAML file"
        "\n 6. pom.xml"
        "\n 7. for all applications")


def get_domain_prompt_from_mysql(schema, procname):
    domain_mappings = read_domains.get_mappings()
    tables = extract_table_names.get_from_mysql(schema, procname)
    return __generate_prompt(domain_mappings, tables)


def get_domain_prompt_from_file(filepath):
    domain_mappings = read_domains.get_mappings()
    tables = extract_table_names.get_table_names_from_file(filepath)
    return __generate_prompt(domain_mappings, tables)


def get_domain_ui_prompt_from_file(filepath):
    domain_mappings = read_domains.get_mappings()
    tables = extract_table_names.get_table_names_from_file(filepath)
    return __generate_ui_prompt(domain_mappings, tables)


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
        prompt += "Generate code with " + ",".join(
            domain_tables[domain]) + " as one spring boot application "
        domain_tables_copy.pop(domain)
        if len(domain_tables_copy) > 0:
            prompt += "and \n"

    prompt += "\nGenerate executable code with open api spec and pom.xml for all applications"
    return prompt


def __generate_ui_prompt(domain_mappings, tables):
    domain_tables = {}
    for table in tables:
        if domain_mappings[table] not in domain_tables:
            domain_tables[domain_mappings[table]] = [table]
        else:
            domain_tables[domain_mappings[table]].append(table)
    prompt = "There are " + str(len(domain_tables)) + " domain(s)" + " in this plsql code "
    domain_names = domain_tables.copy();
    for domain in domain_tables:
        domain_names.pop(domain)
        prompt += domain
        if len(domain_names) > 0:
            prompt += " and "
    prompt += ". "
    domain_tables_copy = domain_tables.copy()
    for domain in domain_tables:
        prompt += "Generating code with table(s) " + ",".join(
            domain_tables[domain]) + " as one spring boot application "
        domain_tables_copy.pop(domain)
        if len(domain_tables_copy) > 0:
            prompt += "and "
    return prompt
