---
name: archetype-selection
description: Pick exactly one application archetype from a given list.
---
# Task
Read CONTEXT_JSON and ARCHETYPES. Choose the single best archetype.
Output JSON only.

# Rules
1. Choose only an id from ARCHETYPES. Never invent an id.
2. If app_type in CONTEXT_JSON matches an archetype, choose it.
3. Decide by "use_when" text and by goal, inputs, outputs. Ignore tech preferences.
4. Several archetypes fit equally -> pick the simpler one, confidence "medium".
5. Nothing fits -> "none", confidence "low".
6. confidence: high = goal clearly matches use_when; medium = partly; low = guess.

# Fields
archetype: id | "none"
confidence: high | medium | low
runner_up: id | null
reason: max 15 words

# Example
CONTEXT_JSON: {"goal":"Конвертировать CSV в JSON","app_type":"cli","inputs":["CSV-файл"],"outputs":["JSON"]}
ARCHETYPES: cli_tool: "runs from shell, reads args, writes stdout/file" | rest_service: "long-running HTTP server with endpoints" | library: "imported by other code, no entry point"
OUTPUT:
{"archetype":"cli_tool","confidence":"high","runner_up":"library","reason":"запуск из командной строки, вход и выход через файлы"}
