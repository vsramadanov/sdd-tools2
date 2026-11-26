import json
from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass(frozen=True)
class AcceptanceCriterion:
    id: str
    kind: str
    given: str
    when: str
    then: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AcceptanceCriterion":
        return cls(
            id=data["id"],
            kind=data["kind"],
            given=data["given"],
            when=data["when"],
            then=data["then"],
        )


@dataclass(frozen=True)
class Requirement:
    id: str
    ears: str
    acceptance: List[AcceptanceCriterion] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Requirement":
        return cls(
            id=data["id"],
            ears=data["ears"],
            acceptance=[
                AcceptanceCriterion.from_dict(item)
                for item in data.get("acceptance", [])
            ],
        )

    @classmethod
    def from_json(cls, text: str) -> "Requirement":
        return cls.from_dict(json.loads(text))
