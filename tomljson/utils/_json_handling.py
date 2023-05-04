import json


def handleNonString(elem) -> bool:
    if isinstance(elem, str) or isinstance(elem, int) or isinstance(elem, bool):
        return True
    else:
        return False


def handleBrackets(elem) -> bool:
    if "[" in str(elem):
        return True
    else:
        return False


def handleChildTable(table_header: str, element) -> bool:
    formatted_title = table_header.strip("[]")
    if formatted_title in str(element):
        return True
    else:
        return False


def breakingPoints(element) -> bool:
    result = True
    if isinstance(element, str):
        if '[[' in element:
            result = False
    elif isinstance(element, list):
        if '{' in element:
            result = False

    return result


def gatherTableContent(table_header: str, index: int, listToIterate: list) -> dict:

    section_content = {}
    while breakingPoints(listToIterate[index]) == 1 or breakingPoints(listToIterate[index]) == 2:

        if index >= len(listToIterate) - 1 or breakingPoints(listToIterate[index]) == 0:
            break

        if breakingPoints(listToIterate[index]) == 2:
            if handleChildTable(table_header, listToIterate[index]):
                section_content[listToIterate[index]] = gatherTableContent(listToIterate[index], index + 1, listToIterate[index + 1:])

        else:
            section_content[listToIterate[index]] = listToIterate[index + 1]
            index += 2
        # elif handleChildTable(listToIterate[index], ):
        #     section_content[listToIterate[index]] = gatherTableContent(index + 1, listToIterate[index + 1:])
    return section_content


def fillTables(table_header: str, parserOutput: list):
    
    table_content = {}
    header_index = parserOutput.index(table_header)
    start_index = header_index + 1

    table_content[table_header] = gatherTableContent(table_header, start_index, parserOutput[start_index:])
        
    return table_content


def handleOutputToDict(parserOutput: list) -> dict:
    global_dict = {}

    for i, elem in enumerate(parserOutput):
        if isinstance(elem, str):
            if elem.startswith("["):
                # array of tables
                if "[[" in elem:
                    current_key = elem.strip("[[]]")
                    global_dict[current_key] = []
                else:
                    # table
                    if '.' not in elem:
                        current_key = elem.strip("[]")
                        global_dict[current_key] = fillTables(elem, parserOutput[i:])
            elif "=" in elem:
                verify_elem = parserOutput[i + 1]
                if isinstance(verify_elem, list):
                    if verify_elem[0] == "{":
                        current_key = (
                            elem.strip(" =")
                            if elem.find(" =") != -1
                            else elem.strip("=")
                        )
                        global_dict[current_key] = {}
                        for j in range(1, len(verify_elem) - 2, 2):
                            new_key = (
                                verify_elem[j].strip(" =")
                                if verify_elem[j].find(" =") != -1
                                else verify_elem[j].strip("=")
                            )
                            global_dict[current_key][new_key] = verify_elem[j + 1]
                    # else:
                    #     current_key = (
                    #         elem.strip(" =")
                    #         if elem.find(" =") != -1
                    #         else elem.strip("=")
                    #     )
                    #     global_dict[current_key] = verify_elem

    return global_dict

    # assignment of non string
    # if handleNonString(parserOutput[i + 1]):
    #     current_key = elem.strip(" =") if elem.find(" =") != -1 else elem.strip("=")
    #     global_dict[current_key] = parserOutput[i + 1]
    # # assigment of string
    # elif isinstance(parserOutput[i + 1], str) and '[' not in parserOutput[i+1]:
    #     current_key = elem.strip(" =") if elem.find(" =") != -1 else elem.strip("=")
    #     global_dict[current_key] = parserOutput[i + 1]
    # else:
    # assignment of array or inline table


def printType(result):
    for elem in result:
        print(f"{elem} => {type(elem)}")


# def handleNonString(elem) -> bool:
#     if isinstance(elem, str) or isinstance(elem, int) or isinstance(elem, bool):
#         return True
#     else:
#         return False


# def handleOutputToDict(parserOutput: list) -> dict:
#     global_dict = {}

#     for i, elem in enumerate(parserOutput):
#         if handleNonString(elem):
#             if isinstance(parserOutput[i - 1], str):
#                 current_key = (
#                     parserOutput[i - 1].strip(" =")
#                     if parserOutput[i - 1].find(" =") != -1
#                     else parserOutput[i - 1].strip("=")
#                 )
#                 global_dict[current_key] = elem
#         elif isinstance(elem, list):
#             check_elem = str(elem)
#             if check_elem.startswith("["):
#                 if '[[' in check_elem:
#                     current_key = check_elem.strip("[[]]")
#                     global_dict[current_key] = []
#                     j = i + 1
#                     while '[' not in parserOutput[j]:
#                         new_dict = {}
#                         formatted_key = parserOutput[j].strip(" =") if parserOutput[j].find(" =") != -1 else parserOutput[j].strip("=")
#                         new_dict[formatted_key] = parserOutput[j + 1]
#                         j += 2
#                     global_dict[current_key].append(new_dict)

#             if isinstance(parserOutput[i - 1], str):
#                 current_key = (
#                     parserOutput[i - 1].strip(" =")
#                     if parserOutput[i - 1].find(" =") != -1
#                     else parserOutput[i - 1].strip("=")
#                 )
#                 global_dict[current_key] = elem


# def parserOutputToDict(parserOutput: List[str]) -> dict:
#     global_dict = {}

#     for i, elem in enumerate(parserOutput):
#         stringElement = str(elem)
#         if stringElement.startswith("["):
#             # array
#             if "=" in parserOutput[i - 1]:
#                 current_key = (
#                     parserOutput[i - 1].strip(" =")
#                     if parserOutput[i - 1].find(" =") != -1
#                     else parserOutput[i - 1].strip("=")
#                 )
#                 global_dict[current_key] = stringElement
#             # array of tables
#             elif stringElement[2] == "[":
#                 current_key = stringElement.strip("[[]]")
#                 global_dict[current_key] = []
#                 j = i + 1
#                 while parserOutput[j].startswith("["):
#                     new_dict = {}
#                     formatted_key = parserOutput[j].strip(" =") if parserOutput[j].find(" =") != -1 else parserOutput[j].strip("=")
#                     new_dict[str(formatted_key)] = parserOutput[j + 1].strip()
#                     j += 2
#                 global_dict[current_key].append(new_dict)
#             # inline table
#             elif stringElement[1] == "{":
#                 current_key = (
#                     parserOutput[i - 1].replace(" =", "")
#                     if parserOutput[i - 1].find(" =") != -1
#                     else parserOutput[i - 1].replace("=", "")
#                 )
#                 global_dict[current_key] = {}
#                 j = i + 1
#                 while "}" not in parserOutput[j]:
#                     formatted_key = parserOutput[j].strip(" =") if parserOutput[j].find(" =") != -1 else parserOutput[j].strip("=")
#                     global_dict[current_key][str(formatted_key)] = parserOutput[j + 1].strip()
#                     j += 2
#             # table
#             else:
#                 current_key = stringElement.strip("[]")
#                 global_dict[current_key] = {}
#                 j = i + 1
#                 while not parserOutput[j].startswith("["):
#                     formatted_key = parserOutput[j]
#                     if formatted_key.find(" =") != -1:
#                         formatted_key = formatted_key.strip(" =")
#                     else:
#                         formatted_key = formatted_key.strip("=")
#                     global_dict[current_key][formatted_key] = str(parserOutput[j + 1])
#                     j += 2

#     return json.dumps(global_dict, indent=None)

# for item in parserOutput:
#     element = str(item)
#     if element.startswith('['):
#         current_key = element.strip('[]')
#         current_dict[current_key] = {}
#         current_dict = current_dict[current_key]
#     elif element.endswith('='):
#         current_key = element[:-2]
#     else:
#         current_dict[current_key] = element


# def fillTables(table_header: str, parserOutput: list):
#     table_content = {}
#     header_index = parserOutput.index(table_header)
#     start_index = header_index + 1

#     while start_index < len(parserOutput):
#         if start_index >= len(parserOutput) - 1:
#             break

#         key = parserOutput[start_index]
#         if handleChildTable(table_header, key):
#             # parse nested table
#             nested_table_header = key
#             nested_table_content = fillTables(nested_table_header, parserOutput)
#             table_content[nested_table_header] = nested_table_content
#             start_index = parserOutput.index(nested_table_header) + 1
#         elif isinstance(key, list):
#             # parse array of tables
#             array_table_header = table_header + key[0].strip("[]")
#             array_table_content = []
#             i = start_index + 1
#             while i < len(parserOutput):
#                 if parserOutput[i] == key:
#                     array_table_content.append(fillTables(array_table_header, parserOutput[start_index:i]))
#                     start_index = i + 1
#                 elif handleChildTable(array_table_header, parserOutput[i]):
#                     # parse nested table
#                     nested_table_header = array_table_header + parserOutput[i]
#                     nested_table_content = fillTables(nested_table_header, parserOutput[i+1:])
#                     array_table_content.append({nested_table_header: nested_table_content})
#                     break
#                 elif i == len(parserOutput) - 1:
#                     array_table_content.append(fillTables(array_table_header, parserOutput[start_index:]))
#                     start_index = len(parserOutput)
#                 i += 1
#             table_content[array_table_header] = array_table_content
#             start_index = i
#         else:
#             # parse key-value pair
#             value = parserOutput[start_index + 1]
#             if handleBrackets(value):
#                 # parse nested array
#                 nested_array = []
#                 i = start_index + 1
#                 while i < len(parserOutput):
#                     nested_array.append(parserOutput[i])
#                     if parserOutput[i] == "}":
#                         break
#                     i += 1
#                 value = nested_array
#             table_content[key] = value
#             start_index += 2

#     return table_content