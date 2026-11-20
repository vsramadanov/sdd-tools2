---
name: req-context-extraction
description: Extract goal, actors, IO, constraints and non-goals from a raw user prompt into fixed JSON.
---
# Task
Read USER_PROMPT. Fill the JSON fields. Output JSON only.

# Rules
1. Use only facts stated in USER_PROMPT. Never invent.
2. Not stated -> "unknown" (or [] for lists). Never guess.
3. Keep domain terms in the user's original language. Field names stay English.
4. Each list item: max 15 words.
5. non_goals: only if the user said "not / without / no need". Else [].
6. Implied but unsaid item -> prefix "[inferred] ".
7. glossary: only terms that appear in USER_PROMPT.

# Fields
goal: one sentence: what the system does, for whom
app_type: cli | rest_api | library | web_ui | desktop | bot | batch | other | unknown
actors: who uses the system or talks to it
inputs: data coming in
outputs: data going out
constraints: language, platform, libraries, performance, legal, deadlines
non_goals: explicitly excluded things
glossary: [{term, meaning}]

# Example
USER_PROMPT: Нужен CLI для конвертации CSV в JSON, без внешних зависимостей, на Python.
OUTPUT:
{"goal":"Конвертировать CSV-файлы в JSON из командной строки","app_type":"cli","actors":["пользователь CLI"],"inputs":["CSV-файл"],"outputs":["JSON"],"constraints":["Python","без внешних зависимостей"],"non_goals":[],"glossary":[]}
