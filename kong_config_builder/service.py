from typing import List, Optional
from dataclasses import dataclass
from kong_config_builder.base import BaseYamlObject
from kong_config_builder.plugin import Plugin


@dataclass
class Route(BaseYamlObject):
    name: str
    paths: List[str]
    strip_path: bool = False


@dataclass
class Service(BaseYamlObject):
    name: str
    host: str
    routes: List[Route]
    plugins: Optional[List[Plugin]] = None
