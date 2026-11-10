from hashlib import md5
from os import sep, walk
from tomllib import load
from typing import Any, Literal, TypeAlias

from pydantic import BaseModel

HashAlgo: TypeAlias = Literal["md5", "sha1", "sha2"]

class ConfigModel (BaseModel):
    path: str
    hash : list[HashAlgo]

def get_config() -> ConfigModel:
    with open(file=
              "configs/config.toml", mode='rb'
            ) as data_file:
        toml_code: dict[str, Any] = load(data_file)
        config_model: ConfigModel = ConfigModel.model_validate(obj=toml_code)
        return config_model


def main()->None:
    index:dict[str,str] = {}
    config: ConfigModel = get_config()
    for subdir, _, files in walk(top=config.path):
        for file in files:
            filepath: str = subdir + sep + file
            with open (file=filepath, mode='rb') as data_file:
                hash: str = md5(data=data_file.read()).hexdigest()
                index[hash] = filepath

    input_line: str = ""
    while (True):
        input_line:str = input()
        if input_line == 'q':
            break
        print(index[input_line])

main()