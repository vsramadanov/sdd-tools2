---
name: architecture-repair
description: Fix ONE architecture violation with ONE operation from a closed list.
---
# Task
Read VIOLATION (code and facts) and EXCERPT (only the modules involved).
Output exactly one operation as JSON.

# Operations (choose one)
move_req:           {"op":"move_req","req":"REQ-..","from":"m1","to":"m2"}
split_module:       {"op":"split_module","module":"m","parts":[{"name":"..","responsibility":"..","reqs":[..]},{"name":"..","responsibility":"..","reqs":[..]}]}
merge_modules:      {"op":"merge_modules","modules":["m1","m2"],"into":"m1"}
add_module:         {"op":"add_module","name":"..","layer":"..","responsibility":"..","reqs":[..]}
drop_module:        {"op":"drop_module","module":"m"}
remove_dependency:  {"op":"remove_dependency","from":"m1","to":"m2"}
move_type:          {"op":"move_type","type":"..","from":"m1","to":"types"}
rename_module:      {"op":"rename_module","from":"..","to":".."}

# Rules
1. Make the smallest change that removes the violation.
2. Use only names that appear in VIOLATION or EXCERPT.
3. Each part of split_module gets a disjoint subset of the original REQs; all REQs must be assigned.
4. Cycle -> remove_dependency of the weakest edge, or move_type to "types".
5. Too many REQs / API items -> split_module (2 parts).
6. Orphan module with no REQ -> drop_module or merge_modules.
7. Never output text outside the JSON.

# Example
VIOLATION: OVERLOAD module=app reqs=[REQ-001..REQ-008] limit=6
EXCERPT: app: "Выполнение сценария"; REQ-001..003 read/validate input; REQ-004..008 format output
OUTPUT:
{"op":"split_module","module":"app","parts":[
{"name":"input_flow","responsibility":"Чтение и проверка входных данных","reqs":["REQ-001","REQ-002","REQ-003"]},
{"name":"output_flow","responsibility":"Форматирование и вывод результата","reqs":["REQ-004","REQ-005","REQ-006","REQ-007","REQ-008"]}
]}
