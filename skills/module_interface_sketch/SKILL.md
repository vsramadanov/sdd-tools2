---
name: module-interface-sketch
description: Describe the public API of ONE module in words, tied to its requirements.
---
# Task
Read MODULE (name, responsibility), ITS_REQS, LOWER_API (public API of modules in lower layers), TYPES (known entities).
Output JSON only. No code, no language-specific types.

# Rules
1. Each API item must serve at least one REQ in ITS_REQS. Cite ids in "reqs".
2. Every REQ in ITS_REQS must appear in at least one API item.
3. Max 7 items. Fewer is better. One item = one action.
4. name: snake_case verb_noun, English (parse_row, read_file).
5. inputs / outputs: short phrases using TYPES terms. New entity -> list it in "owns_types".
6. errors: named failure kinds (file_not_found, malformed_row). [] if none.
7. Do not call or describe modules outside LOWER_API.
8. Do not add API for "future use".

# Item format
{"name":"..","purpose":"max 12 words","inputs":"..","outputs":"..","errors":[..],"reqs":[..]}

# Example
MODULE: csv_parser - Parsing CSV rows into records by header
ITS_REQS: REQ-002 use first row as keys; REQ-003 error on malformed row
LOWER_API: types: Record(fields), ParseError(row_number)
OUTPUT:
{"module":"csv_parser","owns_types":[],"public_api":[
{"name":"parse_rows","purpose":"Convert CSV rows into records by header","inputs":"list of CSV rows","outputs":"list of Record","errors":["malformed_row"],"reqs":["REQ-002","REQ-003"]}
]}
