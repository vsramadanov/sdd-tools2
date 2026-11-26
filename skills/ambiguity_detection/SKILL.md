---
name: ambiguity-detection
description: Find gaps in the project context and turn them into few closed questions with default answers.
---
# Task
Read CONTEXT_JSON. Find missing information that blocks writing testable requirements.
Output JSON: {"questions":[...]}. Max 7 questions, most impactful first.

# Check each category. Ask only if the answer is NOT in CONTEXT_JSON.
- ENTITY: a noun is used but not defined (what fields? what format?)
- INPUT: format, size limit, encoding, source (file/stdin/HTTP) unknown
- OUTPUT: format, destination, ordering unknown
- ERROR: what happens on bad input, missing file, timeout
- QUANTITY: "fast", "many", "large" without a number
- NFR: performance, security/auth, logging, platform/OS
- STATE: persistence (where is data stored? lifetime?)
- SCOPE: unclear boundary: what is NOT included
- STACK: language/framework unknown (only if constraints say "unknown")

# Rules
1. Every question is closed: 2-4 options plus a "default" the system will assume if no answer.
2. One question = one decision. No "and".
3. Never ask what CONTEXT_JSON already states.
4. Never ask about implementation details (class names, algorithms).
5. Fewer questions is better. If nothing blocks, output {"questions":[]}.
6. Question text keeps the language of CONTEXT_JSON.

# Item format
{"id":"Q1","category":"ERROR","question":"...","options":["..","..",".."],"default":"..","why":"max 10 words"}

# Example
CONTEXT_JSON: {"goal":"Конвертировать CSV-файлы в JSON","inputs":["CSV-файл"],"constraints":["Python"], ...}
OUTPUT:
{"questions":[
{"id":"Q1","category":"INPUT","question":"Первая строка CSV - заголовки?","options":["да","нет","настраивается флагом"],"default":"да","why":"определяет ключи JSON"},
{"id":"Q2","category":"ERROR","question":"Что делать с некорректной строкой CSV?","options":["прервать с ошибкой","пропустить и предупредить"],"default":"прервать с ошибкой","why":"поведение при ошибках"},
{"id":"Q3","category":"INPUT","question":"Ожидаемый максимальный размер файла?","options":["до 10 МБ","до 1 ГБ (потоковая обработка)"],"default":"до 10 МБ","why":"влияет на архитектуру"}
]}
