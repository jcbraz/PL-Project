import json


class Data:
    def __init__(self, name, value):
        self.name = name
        self.value = value

class TOMLTable:
    def __init__(self, name):
        self.name = name
        self.data = []
        self.children = []

    def addData(self, data):
        self.data.append(data)

    def addChild(self, child):
        self.children.append(child)
    
    def convertToDict(self):
        dict = {}
        for data in self.data:
            dict[data.name] = data.value
        for child in self.children:
            dict[child.name] = child.convertToDict()
        return dict
    
class ArrayTOMLTable:
    def __init__(self, name):
        self.name = name
        self.tables = []

    def addTable(self, data):
        self.tables.append(data)

    def convertToDict(self):
        dict = {}
        for table in self.tables:
            dict[table.name] = table.convertToDict()
        return dict
    
class Global:
    def __init__(self):
        self.data = []
        self.tables = []

    def addData(self, data):
        self.data.append(data)
    
    def addTable(self, table):
        self.tables.append(table)

    def convertToDict(self):
        dict = {}
        for data in self.data:
            dict[data.name] = data.value
        for table in self.tables:
            dict[table.name] = table.convertToDict()
        return dict

def isInlineTable(element) -> bool:
    result = False
    if isinstance(element, list):
        if '{' in element:
            result = True
    return result
    

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

def gatherInfoFromTable(table_header: str, listToIterate: list) -> TOMLTable:
    table = TOMLTable(table_header)
    for element in listToIterate:
        if breakingPoints(element):
            break
        else:
            if handleChildTable(table_header, element):
                child_table = gatherInfoFromTable(element, listToIterate[listToIterate.index(element)+1:])
                table.addChild(child_table)
            else:
                data_key = element.split("=")[0].strip()
                data_value = listToIterate[listToIterate.index(element)+1]
                data = Data(data_key, data_value)
                table.addData(data)
    return table


def injectInfoInClasses(parserOutput: list):

    global_storage = Global()

    for i, element in enumerate(parserOutput):
        if isinstance(element, str):
            if element.startswith("["):
                # ArrayTOMLTable
                if '[[' in element:
                    key = element[2:-2]
                    for j in range(i+1, len(parserOutput)):
                        if breakingPoints(parserOutput[j]):
                            break
                        else:
                            data_key = parserOutput[j].split("=")[0].strip()
                            data_value = parserOutput[j+1]
                            data = Data(data_key, data_value)
                            table = ArrayTOMLTable(key)
                            table.addTable(data)
                            global_storage.addTable(table)
                else:
                    # TOMLTable
                    key = element[1:-1]
                    table = gatherInfoFromTable(key, parserOutput[i+1:])
                    global_storage.addTable(table)
            else:
                # Data
                if isInlineTable(parserOutput[i+1:]):
                    # InlineTable
                    key = element.split("=")[0].strip()
                    inline_table_class = TOMLTable(key)
                    itable = parserOutput[i+1]
                    itable = itable[1:-1]
                    for k in range(0, len(itable), 2):
                        key = itable[k].split("=")[0].strip()
                        value = itable[k+1]
                        data = Data(key, value)
                        inline_table_class.addData(data)
                    global_storage.addTable(inline_table_class)
                else:
                    key = element.split("=")[0].strip()
                    value = parserOutput[i+1]
                    data = Data(key, value)
                    global_storage.addData(data)

    return global_storage.convertToDict()
                