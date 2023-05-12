import re
import pandas as pd
import json


class BreakPoints:
    def __init__(self):
        self.tables = []
        self.global_info = {}

    def setBreakPoints(self, data):
        table_pattern = re.compile(r"\[+\w+(?:\.\w+)*\]+")
        self.tables = re.findall(table_pattern, str(data))

    def getTables(self):
        return self.tables

    def getInlineTables(self):
        return self.inline_tables
    
    def getGlobalInfo(self):
        return self.global_info

    def getTablesIndexes(self, data: list):
        indexes = []
        for table in self.tables:
            indexes.append(data.index(table))
        return indexes


def handleInlineTables(data):
    result = []
    i = 0
    while i < len(data):
        value = data[i]
        if isinstance(value, list) and value[0] == "{" and value[-1] == "}":
            result.pop(i - 1)
            result.append(f"[{data[i - 1].split('=')[0].strip()}]")
            result.extend(value[1:-1])
            i += 1
        else:
            result.append(value)
        i += 1
    return result


def injectTablesContent(data: list) -> dict:
    breakpoints = BreakPoints()
    breakpoints.setBreakPoints(data)

    table_content = {}
    table_indexes = breakpoints.getTablesIndexes(data)
    table_count = len(table_indexes)

    for i in range(0, table_count - 1):
        table_content[breakpoints.getTables()[i]] = data[
            table_indexes[i] + 1 : table_indexes[i + 1]
        ]

    # Handle the last table
    table_content[breakpoints.getTables()[table_count - 1]] = data[
        table_indexes[table_count - 1] + 1 :
    ]

    return table_content


def arrangeTablesIntoDF(tables_dict: dict) -> pd.DataFrame:
    new_data = {}
    for key, values in tables_dict.items():
        for i in range(0, len(values), 2):
            column_key = key
            if column_key not in new_data:
                new_data[column_key] = []
            variable = values[i].split("=")[0].strip()
            new_data[column_key].append(f"{variable}={values[i+1]}")

    return pd.DataFrame.from_dict(new_data, orient="index")


def extractInfoFromRow(row: pd.Series) -> dict:
    info = {}
    for element in row:
        if isinstance(element, str):
            variable, value = element.split("=")
            info[variable.strip()] = value.strip()
    return info


def extractInfoFromDF(df: pd.DataFrame) -> dict:
    results = {}
    for i in range(len(df) - 1):
        result = extractInfoFromRow(df.iloc[i])
        if "[[" in df.index[i]:
            results[df.index[i]] = result
        else:
            results[df.index[i].strip("[").strip("]")] = result

    # Handle the last row
    result = extractInfoFromRow(df.iloc[-1])
    results[df.index[-1].strip("[]")] = result

    return results


def handleNestedTables(input_dict):
    keys_to_remove = []
    keys_copy = list(input_dict.keys())

    for key in keys_copy:
        if "." in key:
            parent_key, nested_key = key.split(".", 1)
            parent_key = parent_key.strip("[").strip(
                "]"
            )  # Remove brackets from parent_key
            nested_key = nested_key.strip("[").strip(
                "]"
            )  # Remove brackets from nested_key
            if parent_key in input_dict:
                input_dict[parent_key][nested_key] = input_dict[key]
            else:
                input_dict[parent_key] = {nested_key: input_dict[key]}
            keys_to_remove.append(key)

    for key in keys_to_remove:
        del input_dict[key]

    return input_dict


def handleArrayTables(input_dict: dict):
    return_dict = {}

    for key, value in input_dict.items():
        if "[[" in key:
            new_key = key.strip("[").strip("]")
            new_value = [{k: v} for k, v in value.items()]
            return_dict[new_key] = new_value
        else:
            return_dict[key] = value

    return return_dict


def handleGlobalInfo(input_dict: dict, data: list) -> dict:
    updated_dict = {}

    breakpoints = BreakPoints()
    breakpoints.setBreakPoints(data)
    for i in range(0, breakpoints.getTablesIndexes(data)[0], 2):
        updated_dict[data[i].split("=")[0].strip()] = data[i+1]
    
    updated_dict.update(input_dict)
    return updated_dict


def convertOutputToJson(data: list):
    data = handleInlineTables(data)
    tables_dict = injectTablesContent(data)
    df = arrangeTablesIntoDF(tables_dict)
    results = extractInfoFromDF(df)
    results = handleNestedTables(results)
    results = handleArrayTables(results)
    updated_results = handleGlobalInfo(results, data)
    return updated_results


# Convert results to json
def writeJsonFile(data: dict, file_name: str):
    with open(f"tomljson/outputs/{file_name}.json", "w") as f:
        json.dump(convertOutputToJson(data), f, indent=4)
