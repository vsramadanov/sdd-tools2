---
name: module-decomposition
description: Adjust an archetype skeleton into a final module list with one-sentence responsibilities.
---
# Task
Read SKELETON (modules of the archetype), REQ_DIGEST, GLOSSARY, LIMITS.
Output JSON: {"modules":[...],"dropped":[...]}.

# Rules
1. Keep every skeleton module with fixed=true.
2. A skeleton module with fixed=false that no REQ needs -> move its name to "dropped".
3. Add a new module only if a group of REQs fits no existing module. Max 3 added modules.
4. Module = ONE responsibility. Responsibility: one sentence, max 15 words, no "and" joining two duties.
5. name: snake_case, 1-2 English words, a noun. Forbidden: utils, common, helpers, misc, manager, base, core.
6. layer: only a layer listed in SKELETON.layers.
7. Shared entities and error types belong to "types", not to feature modules.
8. Do not exceed LIMITS.max_modules.
9. responsibility text uses the language of GLOSSARY / REQ_DIGEST.

# Item format
{"name":"..","layer":"..","responsibility":"..","origin":"skeleton|added"}

# Example
SKELETON: cli(entry,fixed) app(app,fixed) types(domain,fixed) io(infra,optional)
REQ_DIGEST: REQ-001 read CSV from file; REQ-002 keys from header row; REQ-003 exit 1 on bad row; REQ-005 write JSON to stdout
OUTPUT:
{"modules":[
{"name":"cli","layer":"entry","responsibility":"Argument parsing and returning the exit code","origin":"skeleton"},
{"name":"app","layer":"app","responsibility":"Executing the conversion scenario from input to output","origin":"skeleton"},
{"name":"types","layer":"domain","responsibility":"Shared data types and errors","origin":"skeleton"},
{"name":"io","layer":"infra","responsibility":"Reading the file and writing to stdout","origin":"skeleton"},
{"name":"csv_parser","layer":"domain","responsibility":"Parsing CSV rows into records by header","origin":"added"}
],"dropped":[]}
