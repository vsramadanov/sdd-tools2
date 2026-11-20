---
name: req-atomization
description: Turn project context and user answers into a flat list of atomic, testable requirements.
---
# Task
Read CONTEXT_JSON and ANSWERS (id -> chosen option; use "default" if unanswered).
Output JSON: {"requirements":[...]}. Max 12 items.

# Rules
1. Text form: "The system shall <verb> <object> [condition]." Write in the language of CONTEXT_JSON; keep "The system shall" pattern translated naturally.
2. ONE behavior per requirement. If text contains "and" / "or" joining two actions -> split.
3. Each requirement must be verifiable by a test. Replace vague words with numbers or concrete values.
   Forbidden: fast, easy, user-friendly, robust, efficient, appropriate, etc, as needed, support (alone), handle (alone).
4. Cover systematically:
   - each input -> one requirement on accepted format
   - each input -> one requirement on invalid input behavior
   - each output -> one requirement on output format
   - each constraint -> one requirement of type "constraint"
5. Every ANSWER becomes at least one requirement.
6. Do not add features absent from CONTEXT_JSON and ANSWERS.
7. ids: REQ-001, REQ-002, ... in order.

# Fields
id, type: functional | nfr | constraint | interface
priority: must | should | could (default must)
text, source: user | answer:Qn | inferred

# Example
CONTEXT: CSV->JSON CLI, Python, no deps. ANSWERS: Q1=да, Q2=прервать с ошибкой.
OUTPUT:
{"requirements":[
{"id":"REQ-001","type":"functional","priority":"must","text":"Система должна читать CSV-файл, путь к которому передан первым аргументом.","source":"user"},
{"id":"REQ-002","type":"functional","priority":"must","text":"Система должна использовать первую строку CSV как имена ключей JSON-объектов.","source":"answer:Q1"},
{"id":"REQ-003","type":"functional","priority":"must","text":"Система должна завершаться с ненулевым кодом и сообщением об ошибке при некорректной строке CSV.","source":"answer:Q2"},
{"id":"REQ-004","type":"constraint","priority":"must","text":"Система не должна использовать сторонние зависимости, кроме стандартной библиотеки Python.","source":"user"}
]}
