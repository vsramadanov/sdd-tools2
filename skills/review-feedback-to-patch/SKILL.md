---
name: review-feedback-to-patch
description: Translate a human review comment into architecture operations, or ask one closed question.
---
# Task
Read USER_COMMENT (free text) and ARCH_SUMMARY (module names, responsibilities, dependencies).
Output JSON: {"ops":[...],"understood":"...","unclear":null}

# Rules
1. Translate only what the comment says. Never add changes of your own.
2. Use operations from the architecture-repair list. Max 3 ops per call.
3. Names must exist in ARCH_SUMMARY, except new names the comment itself introduces.
4. "understood": restate the comment in one sentence, in the language of USER_COMMENT.
5. Comment is ambiguous, refers to unknown modules, or asks for something outside the operation list ->
   "ops": [] and "unclear": one closed question with 2-3 options.
6. A comment of approval or a question without a change request -> "ops": [].
7. Comment contradicts a REQ -> "ops": [] and "unclear": "Это изменит требование REQ-.. Вернуться на Этап 1?"

# Example
USER_COMMENT: "csv_parser и json_writer лучше слить в один модуль converter"
OUTPUT:
{"ops":[{"op":"merge_modules","modules":["csv_parser","json_writer"],"into":"converter"}],"understood":"Объединить csv_parser и json_writer в модуль converter.","unclear":null}
