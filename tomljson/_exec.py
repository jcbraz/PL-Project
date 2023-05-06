from tomljson.parser._parser import _parser
from tomljson.utils._json_handle import writeJsonFile

result = _parser("../../model.toml")
writeJsonFile(result, "model")