from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any


@dataclass
class ModuleMapping:
    req: str
    primary: str
    secondary: list[str] = field(default_factory=list)
    reason: str = ""
    suggested_module: str | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ModuleMapping":
        return cls(
            req=data["req"],
            primary=data["primary"],
            secondary=list(data.get("secondary", [])),
            reason=data.get("reason", ""),
            suggested_module=data.get("suggested_module"),
        )

    def to_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {
            "req": self.req,
            "primary": self.primary,
            "secondary": list(self.secondary),
            "reason": self.reason,
        }
        if self.suggested_module is not None:
            result["suggested_module"] = self.suggested_module
        return result


@dataclass
class ReqToModuleMapping:
    mapping: list[ModuleMapping] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ReqToModuleMapping":
        return cls(
            mapping=[ModuleMapping.from_dict(m)
                     for m in data.get("mapping", [])],
        )

    @classmethod
    def from_json(cls, text: str) -> "ReqToModuleMapping":
        return cls.from_dict(json.loads(text))

    def to_dict(self) -> dict[str, Any]:
        return {"mapping": [m.to_dict() for m in self.mapping]}

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False)
