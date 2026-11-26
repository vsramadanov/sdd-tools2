---
name: adr-writing
description: Write ONE short architecture decision record from given facts only.
---
# Task
Read DECISION_FACTS. Output JSON only.

# Rules
1. Use only facts in DECISION_FACTS. Never invent reasons, benchmarks, or history.
2. No reason given -> write "Значение по умолчанию архетипа" (or the user's language equivalent) in "context".
3. Every text field: max 30 words.
4. consequences: max 3 items, each a concrete effect on the codebase or the team.
5. alternatives: only options listed in DECISION_FACTS. Else [].
6. title: max 8 words.

# Fields
id (given), title, status ("proposed"), context, decision, consequences[], alternatives[]

# Example
DECISION_FACTS: id=ADR-002; topic=json output; chosen=stdlib json; options=[stdlib json, orjson]; drivers=[REQ-004 no third-party deps]
OUTPUT:
{"id":"ADR-002","title":"JSON-вывод через стандартную библиотеку","status":"proposed","context":"REQ-004 запрещает сторонние зависимости.","decision":"Использовать модуль json стандартной библиотеки.","consequences":["Нет внешних зависимостей","Скорость сериализации ограничена возможностями stdlib"],"alternatives":["orjson"]}
