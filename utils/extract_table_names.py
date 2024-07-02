import mysql.connector
import re

from utils import file_reader


def __get_stored_procedure_code(cursor, schema, procname):
    cursor.execute(f"SHOW CREATE PROCEDURE " + schema + "." + procname)
    result = cursor.fetchone()
    return result[2] if result else None


def __extract_table_names(procedure_code):
    # Regular expression to find table names in various SQL statements
    pattern = re.compile(
        r'\b(?:FROM|JOIN|UPDATE|TABLE|DELETE FROM|INSERT INTO)\s+`?(\w+)`?',
        re.IGNORECASE
    )
    return set(match.group(1) for match in pattern.finditer(procedure_code))


def get_table_names_from_file(filepath):
    proc_code = file_reader.get_data_from_file(filepath)
    return list(__extract_table_names(proc_code))


def get_file_content(filepath):
    return file_reader.get_data_from_file(filepath)


def get_from_mysql(schema, procname):
    # MySQL connection details
    config = {
        'user': 'root',
        'password': 'root',
        'host': 'localhost',
    }

    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        procedure_code = __get_stored_procedure_code(cursor, schema, procname)
        if procedure_code:
            table_names = __extract_table_names(procedure_code)
            return list(table_names)
        else:
            print(f"Procedure {procname} not found.")

    finally:
        cursor.close()
        conn.close()


def get_body_mysql(schema, procname):
    # MySQL connection details
    config = {
        'user': 'root',
        'password': 'root',
        'host': 'localhost',
    }

    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        procedure_code = __get_stored_procedure_code(cursor, schema, procname)
        if procedure_code:
            return procedure_code
        else:
            print(f"Procedure {procname} not found.")

    finally:
        cursor.close()
        conn.close()
