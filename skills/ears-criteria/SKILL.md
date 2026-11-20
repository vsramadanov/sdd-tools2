---
name: ears-criteria
description: For ONE requirement, pick an EARS pattern and write concrete Given/When/Then acceptance criteria.
---
# Task
Read ONE requirement (REQ) and GLOSSARY. Output JSON:
{"id":"REQ-..","ears":"...","acceptance":[...]}

# EARS patterns (choose exactly one)
ubiquitous:   The <system> shall <response>.
event:        When <trigger>, the <system> shall <response>.
state:        While <state>, the <system> shall <response>.
unwanted:     If <bad condition>, then the <system> shall <response>.
optional:     Where <feature is present>, the <system> shall <response>.
Use "unwanted" for errors, "event" for user actions, "ubiquitous" for constants and constraints.

# Acceptance criteria rules
1. 1-4 criteria per REQ. Each = one scenario: given / when / then.
2. Use CONCRETE values (real strings, numbers, file contents). Never "some", "valid data", "correct input".
3. "then" must be directly checkable: exact output, exit code, return value, or error type.
4. At least one criterion with kind "negative" (invalid input / error path) unless REQ is type constraint.
5. Do not add behavior beyond the REQ.
6. Use terms from GLOSSARY exactly as written.
7. Criterion ids: <REQ-id>.AC1, .AC2, ...

# Criterion format
{"id":"REQ-003.AC1","kind":"positive|negative|boundary","given":"..","when":"..","then":".."}

# Example
REQ-003: The system shall exit with non-zero code and an error message on a malformed CSV row.
OUTPUT:
{"id":"REQ-003","ears":"If a CSV row has a different number of fields than the header, then the system shall exit with code 1 and print the row number to stderr.","acceptance":[
{"id":"REQ-003.AC1","kind":"negative","given":"file bad.csv: 'a,b\\n1,2\\n3'","when":"run: tool bad.csv","then":"exit code 1; stderr contains 'row 3'"},
{"id":"REQ-003.AC2","kind":"positive","given":"file ok.csv: 'a,b\\n1,2'","when":"run: tool ok.csv","then":"exit code 0; stdout is [{\"a\":\"1\",\"b\":\"2\"}]"}
]}
