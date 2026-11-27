---
name: req-to-module-mapping
description: Assign ONE requirement to the module that owns its behavior.
---
# Task
Read ONE requirement (REQ) and MODULES (name: responsibility).
Output JSON only.

# Rules
1. primary = the module that makes the decision or performs the main action of the REQ.
2. secondary = modules that only supply data or perform I/O for it. Max 2. Often [].
3. Use only names from MODULES. Never invent a module.
4. REQ about exit codes, arguments, endpoints, UI -> entry-layer module.
5. REQ of type constraint (stack, dependencies, platform) -> primary "_global".
6. No module fits -> primary "NONE" and suggested_module (snake_case name, 1-2 words).
7. reason: max 10 words.

# Fields
req, primary, secondary, reason, suggested_module (only when NONE)

# Example
REQ-003 (functional): The system shall exit with non-zero code and print row number on a malformed CSV row.
MODULES: cli: arguments, exit code | app: run conversion scenario | csv_parser: parse CSV rows into records | io: read file, write stdout | types: shared types and errors
OUTPUT:
{"req":"REQ-003","primary":"csv_parser","secondary":["cli"],"reason":"parser detects the error, cli returns the code"}
