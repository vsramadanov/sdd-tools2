---
name: library-selection
description: Choose external libraries from an allowlist, only where a requirement needs one.
---
# Task
Read REQ_DIGEST, CONSTRAINTS, ALLOWLIST (purpose -> candidate libraries for the chosen language).
Output JSON: {"libraries":[...],"unmet":[...]}.

# Rules
1. Prefer the standard library. Add a library only if a REQ clearly needs a capability the stdlib lacks.
2. Choose only names present in ALLOWLIST. Never invent a library.
3. If CONSTRAINTS forbid dependencies -> {"libraries":[],"unmet":[]}.
4. One library per purpose. Pick the first candidate unless CONSTRAINTS say otherwise.
5. Need exists, ALLOWLIST has no candidate -> put it in "unmet" (purpose + REQ ids). Do not substitute.
6. Every library must cite the REQ ids that need it.

# Item formats
libraries: {"purpose":"..","name":"..","reqs":["REQ-001"]}
unmet: {"purpose":"..","reqs":["REQ-005"]}

# Example
CONSTRAINTS: ["Python"]. REQ_DIGEST: REQ-001 read YAML config; REQ-002 print table to stdout.
ALLOWLIST: yaml_parse: [pyyaml] | table_output: [rich, tabulate] | http_client: [httpx]
OUTPUT:
{"libraries":[{"purpose":"yaml_parse","name":"pyyaml","reqs":["REQ-001"]},{"purpose":"table_output","name":"rich","reqs":["REQ-002"]}],"unmet":[]}
