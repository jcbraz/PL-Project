from tomljson.parser._parser import _parser
from tomljson.utils._json_handle import injectInfoInClasses

result = _parser("../../model.toml")
print(injectInfoInClasses(result))