from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Literal


Origin = Literal["skeleton", "added"]


@dataclass
class Module:
    name: str
    layer: str
    responsibility: str
    origin: Origin

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Module":
        return cls(
            name=data["name"],
            layer=data["layer"],
            responsibility=data["responsibility"],
            origin=data["origin"],
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "layer": self.layer,
            "responsibility": self.responsibility,
            "origin": self.origin,
        }


@dataclass
class ModuleDecomposition:
    modules: list[Module] = field(default_factory=list)
    dropped: list[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ModuleDecomposition":
        return cls(
            modules=[Module.from_dict(m) for m in data.get("modules", [])],
            dropped=list(data.get("dropped", [])),
        )

    @classmethod
    def from_json(cls, text: str) -> "ModuleDecomposition":
        return cls.from_dict(json.loads(text))

    def to_dict(self) -> dict[str, Any]:
        return {
            "modules": [m.to_dict() for m in self.modules],
            "dropped": list(self.dropped),
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False)
