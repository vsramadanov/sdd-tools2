---
name: req-atomization
description: Turn project context and user DECISIONS into a flat list of atomic, testable requirements.
---
# Task
Read CONTEXT_JSON and DECISIONS (id -> chosen option; use "default" if unanswered).
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
6. Do not add features absent from CONTEXT_JSON and DECISIONS.
7. ids: REQ-001, REQ-002, ... in order.

# Fields
id, type: functional | nfr | constraint | interface
priority: must | should | could (default must)
text, source: user | answer:Qn | inferred

# Example
CONTEXT: CSV->JSON CLI, Python, no deps. DECISIONS: Q1=yes, Q2=exit with error.
OUTPUT:
{"requirements":[
{"id":"REQ-001","type":"functional","priority":"must","text":"The system shall read a CSV file whose path is passed as the first argument.","source":"user"},
{"id":"REQ-002","type":"functional","priority":"must","text":"The system shall use the first CSV row as the key names of JSON objects.","source":"answer:Q1"},
{"id":"REQ-003","type":"functional","priority":"must","text":"The system shall exit with a non-zero code and an error message on a malformed CSV row.","source":"answer:Q2"},
{"id":"REQ-004","type":"constraint","priority":"must","text":"The system shall not use third-party dependencies other than the Python standard library.","source":"user"}
]}
