import json
from typing import List


def parserOutputToDict(parserOutput: List[str]) -> dict:
    global_dict = {}

    for i, elem in enumerate(parserOutput):
        stringElement = str(elem)
        if stringElement.startswith("["):
            # array
            if "=" in parserOutput[i - 1]:
                current_key = (
                    parserOutput[i - 1].replace(" =", "")
                    if parserOutput[i - 1].find(" =") != -1
                    else parserOutput[i - 1].replace("=", "")
                )
                global_dict[current_key] = stringElement
            # array of tables
            elif stringElement[2] == "[":
                current_key = stringElement.strip("[[]]")
                global_dict[current_key] = []
                j = i + 1
                while parserOutput[j].startswith("["):
                    new_dict = {}
                    new_dict[parserOutput[j]] = parserOutput[j + 1]
                    j += 2
                global_dict[current_key].append(new_dict)
            # inline table
            elif stringElement[1] == "{":
                current_key = (
                    parserOutput[i - 1].replace(" =", "")
                    if parserOutput[i - 1].find(" =") != -1
                    else parserOutput[i - 1].replace("=", "")
                )
                global_dict[current_key] = {}
                j = i + 1
                while "}" not in parserOutput[j]:
                    global_dict[current_key][parserOutput[j]] = parserOutput[j + 1]
                    j += 2

            # table
            else:
                current_key = stringElement.strip("[]")
                global_dict[current_key] = {}
                j = i + 1
                while not parserOutput[j].startswith("["):
                    global_dict[current_key][parserOutput[j]] = parserOutput[j + 1]
                    j += 2

    return json.dumps(global_dict, indent=None)

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


# data = ['title =', 'TOML Example', '[owner]', 'name =', 'Tom Preston-Werner', 'dob =', '1979-05-27T07:32:00-08:00', '[[products]]', 'name =', 'Joybrau', 'flavour =', 'Lemon', '[database]', 'enabled =', True, 'ports =', [8000, 8001, 8002], 'temp_targets =', ['{', 'cpu =', 79.5, 'case =', 72.0, '}'], ['[servers]', '[servers.alpha]', 'ip =', '10.0.0.1', 'role =', 'frontend'], '[servers.beta]', 'ip =', '10.0.0.2', 'role =', 'backend', '[bananas]', 'name =', 'Chiquita', 'price =', 1.99, 'quantity =', 10, 'hosts =', ['alpha', 'omega']]

# finished_data = parserOutputToDict(data)
