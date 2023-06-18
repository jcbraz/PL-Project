# This file contains functions to format TOML strings, more specifically, remove unnecessary whitespace and sort the keys.

from tomlkit import parse, document, dumps
import re


def sort_toml(toml_str: str):
    toml_document = parse(toml_str)
    new_document = document()
    parent_pattern = re.compile(r"\[(\w+)\]")
    child_pattern = re.compile(r"\[\w+\.\w+\]")
    parent_buffer = []
    child_buffer = []
    table_queue = []

    lines = toml_str.split("\n")
    for line in lines:
        parent_match = re.match(parent_pattern, line)
        if parent_match:
            parent_buffer.append(parent_match.group(1))
        child_match = re.match(child_pattern, line)
        if child_match:
            child_buffer.append(child_match.group(0))

    for parent in parent_buffer:
        table_queue.append(parent)
        for child in child_buffer:
            parent_reference = child.split(".")[0]
            parent_reference = parent_reference.replace("[", "")
            if parent == parent_reference:
                table_queue.append(child[1:-1])

    for table in table_queue:
        if "." in table:
            parent, child = table.split(".")
            if parent not in new_document:
                new_document[parent] = {}
            new_document[parent][child] = toml_document[parent][child]
        else:
            new_document[table] = toml_document[table]

    return dumps(new_document)


def handleTableArrayFormat(toml_str: str):
    search_pattern = re.compile(r"=\s?\[")
    lines = toml_str.split("\n")

    for i in range(len(lines)):
        match = re.search(search_pattern, lines[i])
        if match:
            lines[i] = lines[i].replace("[", ".[")

    return "\n".join(lines)