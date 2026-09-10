from dataclasses import dataclass


@dataclass
class PackageInfo:
    name: str
    version: str
    description: str
    repository: str
    url: str
