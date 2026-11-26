import json
from dataclasses import dataclass
from typing import Any, Dict


@dataclass(frozen=True)
class Requirement:
    id: str
    type: str
    priority: str
    text: str
    source: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Requirement":
        return cls(
            id=data["id"],
            type=data["type"],
            priority=data["priority"],
            text=data["text"],
            source=data["source"],
        )

    @classmethod
    def from_json(cls, text: str) -> "Requirement":
        return cls.from_dict(json.loads(text))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "type": self.type,
            "priority": self.priority,
            "text": self.text,
            "source": self.source,
        }
