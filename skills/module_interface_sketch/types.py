from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any


@dataclass
class ApiItem:
    name: str
    purpose: str
    inputs: str
    outputs: str
    errors: list[str] = field(default_factory=list)
    reqs: list[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ApiItem":
        return cls(
            name=data["name"],
            purpose=data["purpose"],
            inputs=data["inputs"],
            outputs=data["outputs"],
            errors=list(data.get("errors", [])),
            reqs=list(data.get("reqs", [])),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "purpose": self.purpose,
            "inputs": self.inputs,
            "outputs": self.outputs,
            "errors": list(self.errors),
            "reqs": list(self.reqs),
        }


@dataclass
class ModuleInterfaceSketch:
    module: str
    owns_types: list[str] = field(default_factory=list)
    public_api: list[ApiItem] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ModuleInterfaceSketch":
        return cls(
            module=data["module"],
            owns_types=list(data.get("owns_types", [])),
            public_api=[ApiItem.from_dict(i)
                        for i in data.get("public_api", [])],
        )

    @classmethod
    def from_json(cls, text: str) -> "ModuleInterfaceSketch":
        return cls.from_dict(json.loads(text))

    def to_dict(self) -> dict[str, Any]:
        return {
            "module": self.module,
            "owns_types": list(self.owns_types),
            "public_api": [i.to_dict() for i in self.public_api],
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False)
