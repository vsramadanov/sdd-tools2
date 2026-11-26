---
name: dependency-declaration
description: Choose which allowed modules ONE module calls, and which of their API items it uses.
---
# Task
Read MODULE (name, responsibility, public_api) and CANDIDATES (allowed modules with their API names).
Output JSON only.

# Rules
1. Choose only from CANDIDATES. Others are forbidden by architecture rules.
2. Depend on a candidate only if MODULE's API needs its functions to do its work.
3. "uses" lists API names that exist in that candidate. Never invent names.
4. No dependency needed -> "depends_on": []. This is common and fine.
5. Max 4 dependencies. Prefer fewer.
6. Shared types from "types" are always allowed and need no "uses" entry.
7. why: max 10 words.

# Item format
{"module":"..","uses":[".."],"why":".."}

# Example
MODULE: app - Выполнение сценария конвертации от входа до выхода; API: run_conversion
CANDIDATES: io: [read_file, write_stdout] | csv_parser: [parse_rows] | json_writer: [serialize_records]
OUTPUT:
{"module":"app","depends_on":[
{"module":"io","uses":["read_file","write_stdout"],"why":"ввод и вывод сценария"},
{"module":"csv_parser","uses":["parse_rows"],"why":"разбор прочитанных строк"},
{"module":"json_writer","uses":["serialize_records"],"why":"формирование JSON"}
]}
