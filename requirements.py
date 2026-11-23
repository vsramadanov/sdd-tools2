from typing import TypedDict
from langgraph.graph import StateGraph, START, END


class RequirementsState(TypedDict, total=False):
    req_atomization_gate_status: dict
    ears_criterion_gate_status: dict


def req_atomization(state: RequirementsState) -> RequirementsState: ...
def req_atomization_gate(state: RequirementsState) -> RequirementsState: ...
def req_atomization_fix(state: RequirementsState) -> RequirementsState: ...
def extract_requirements(state: RequirementsState) -> RequirementsState: ...
def advance_requirement(state: RequirementsState) -> RequirementsState: ...
def ears_criterion(state: RequirementsState) -> RequirementsState: ...
def ears_criterion_gate(state: RequirementsState) -> RequirementsState: ...
def ears_criterion_fix(state: RequirementsState) -> RequirementsState: ...
def req_counter(state: RequirementsState) -> RequirementsState: ...
def notify_status(state: RequirementsState) -> RequirementsState: ...


def requirements_postprocess(
    state: RequirementsState) -> RequirementsState: ...


def route_req_atomization_gate(state: RequirementsState) -> str:
    return "PASS" if state["req_atomization_gate_status"] else "FAILED"


def route_ears_criterion_gate(state: RequirementsState) -> str:
    return "PASS" if state["ears_criterion_gate_status"] else "FAILED"


def route_extract_requirement(state: RequirementsState) -> str:
    return "PROCEED" if state[""] else "FINNISH"


graph = StateGraph(RequirementsState)

graph.add_node("req_atomization", req_atomization)
graph.add_node("req_atomization_gate", req_atomization_gate)
graph.add_node("req_atomization_fix", req_atomization_gate)
graph.add_node("extract_requirements", extract_requirements)
graph.add_node("advance_requirement", advance_requirement)
graph.add_node("ears_criterion", ears_criterion)
graph.add_node("ears_criterion_gate", ears_criterion_gate)
graph.add_node("ears_criterion_fix", ears_criterion_gate)
graph.add_node("req_counter", req_counter)
graph.add_node("requirements_postprocess", requirements_postprocess)
graph.add_node("notify_status", notify_status)


graph.add_edge(START, "req_atomization")
graph.add_edge("req_atomization", "req_atomization_gate")
graph.add_conditional_edges(
    "req_atomization_gate",
    route_req_atomization_gate,
    {
        "PASS": "extract_requirements",
        "FAILED": "req_atomization_fix",
    },
)
graph.add_edge("req_atomization_fix", "req_atomization_gate")
graph.add_edge("extract_requirements", "advance_requirement")
graph.add_edge("advance_requirement", "ears_criterion")
graph.add_edge("ears_criterion", "ears_criterion_gate")
graph.add_conditional_edges(
    "ears_criterion_gate",
    route_ears_criterion_gate,
    {
        "PASS": "req_counter",
        "FAILED": "ears_criterion_fix",
    },
)
graph.add_edge("ears_criterion_fix", "ears_criterion_gate")

graph.add_conditional_edges(
    "req_counter",
    route_extract_requirement,
    {
        "PROCEED": "advance_requirement",
        "FINISH": "requirements_postprocess",
    },
)
graph.add_edge("requirements_postprocess", "notify_status")
graph.add_edge("notify_status", END)

app = graph.compile()
