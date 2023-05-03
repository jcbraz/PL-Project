from tomljson.parser._parser import _parser
from tomljson.utils._json_handling import printType, handleOutputToDict

result = _parser("../../model.toml")
print(handleOutputToDict(result))
# printType(result)
# result = parserOutputToDict(result)

# with open("result.json", "w") as file:
#         file.write(str(result))