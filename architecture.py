from typing import TypedDict

import logging

from langgraph.graph import StateGraph, START, END
from langgraph.runtime import Runtime

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(name)s %(funcName)s: %(message)s",
)


class ArchitectureState(TypedDict):
    fsm_status: str
    llm_response: str


class ArchitectureSmContext(TypedDict):
    llm: object
    llm_skill_collection: dict


def parse_requirements(state: ArchitectureState,
                       runtime: Runtime[ArchitectureSmContext]) -> dict:
    return {}


def requirements_gate(state: ArchitectureState,
                      runtime: Runtime[ArchitectureSmContext]) -> dict:
    return {}


def module_decomposition(state: ArchitectureState,
                         runtime: Runtime[ArchitectureSmContext]) -> dict:
    return {}


def advance_module(state: ArchitectureState,
                   runtime: Runtime[ArchitectureSmContext]) -> dict:
    return {}


def req_to_module_mapping(state: ArchitectureState,
                          runtime: Runtime[ArchitectureSmContext]) -> dict:
    return {}


def req_to_module_mapping_gate(state: ArchitectureState,
                               runtime: Runtime[ArchitectureSmContext]) -> dict:
    return {}


def req_to_module_mapping_fix(state: ArchitectureState,
                              runtime: Runtime[ArchitectureSmContext]) -> dict:
    return {}


def module_counter(state: ArchitectureState,
                   runtime: Runtime[ArchitectureSmContext]) -> dict:
    return {}


def module_interface_sketch(state: ArchitectureState,
                            runtime: Runtime[ArchitectureSmContext]) -> dict:
    return {}


def module_interface_sketch_gate(state: ArchitectureState,
                                 runtime: Runtime[ArchitectureSmContext]) -> dict:
    return {}


def module_interface_sketch_fix(state: ArchitectureState,
                                runtime: Runtime[ArchitectureSmContext]) -> dict:
    return {}


def module_dependency_declaration(state: ArchitectureState,
                                  runtime: Runtime[ArchitectureSmContext]) -> dict:
    return {}


def module_dependency_declaration_gate(state: ArchitectureState,
                                       runtime: Runtime[ArchitectureSmContext]) -> dict:
    return {}


def module_dependency_declaration_fix(state: ArchitectureState,
                                      runtime: Runtime[ArchitectureSmContext]) -> dict:
    return {}


def combine_architecture_report(state: ArchitectureState,
                                runtime: Runtime[ArchitectureSmContext]) -> dict:
    return {}


def report_status(state: ArchitectureState,
                  runtime: Runtime[ArchitectureSmContext]) -> dict:
    return {}


def route_requirements_gate(state: ArchitectureState) -> str:
    return "FAILED" if False else "PASSED"


def route_req_to_module_mapping_gate(state: ArchitectureState) -> str:
    return "FAILED" if False else "PASSED"


def route_module_interface_sketch_gate(state: ArchitectureState) -> str:
    return "FAILED" if False else "PASSED"


def route_module_dependency_declaration_gate(state: ArchitectureState) -> str:
    return "FAILED" if False else "PASSED"


def route_advance_module(state: ArchitectureState) -> str:
    return "again" if state.get("fsm_status") == "again" else "next"


graph = StateGraph(state_schema=ArchitectureState,
                   context_schema=ArchitectureSmContext)

graph.add_node("parse_requirements", parse_requirements)
graph.add_node("requirements_gate", requirements_gate)

graph.add_node("module_decomposition", module_decomposition)

graph.add_node("req_to_module_mapping_advance_module", advance_module)
graph.add_node("req_to_module_mapping", req_to_module_mapping)
graph.add_node("req_to_module_mapping_gate", req_to_module_mapping_gate)
graph.add_node("req_to_module_mapping_fix", req_to_module_mapping_fix)
graph.add_node("req_to_module_mapping_counter", module_counter)

graph.add_node("interface_sketch_advance_module", advance_module)
graph.add_node("module_interface_sketch", module_interface_sketch)
graph.add_node("module_interface_sketch_gate", module_interface_sketch_gate)
graph.add_node("module_interface_sketch_fix", module_interface_sketch_fix)
graph.add_node("module_interface_sketch_counter", module_counter)

graph.add_node("dependency_declaration_advance_module", advance_module)
graph.add_node("module_dependency_declaration", module_dependency_declaration)
graph.add_node("module_dependency_declaration_gate",
               module_dependency_declaration_gate)
graph.add_node("module_dependency_declaration_fix",
               module_dependency_declaration_fix)
graph.add_node("module_dependency_declaration_counter", module_counter)

graph.add_node("combine_architecture_report", combine_architecture_report)
graph.add_node("report_status", report_status)

graph.add_edge(START, "parse_requirements")
graph.add_edge("parse_requirements", "requirements_gate")
graph.add_conditional_edges(
    "requirements_gate",
    route_requirements_gate,
    {"FAILED": "report_status", "PASSED": "module_decomposition"},
)
graph.add_edge("module_decomposition", "req_to_module_mapping_advance_module")

graph.add_conditional_edges(
    "req_to_module_mapping_advance_module",
    route_advance_module,
    {
        "PROCEED": "req_to_module_mapping",
        "FINISHED": "interface_sketch_advance_module"
    },
)
graph.add_edge("req_to_module_mapping", "req_to_module_mapping_gate")
graph.add_conditional_edges(
    "req_to_module_mapping_gate",
    route_req_to_module_mapping_gate,
    {
        "FAILED": "req_to_module_mapping_fix",
        "PASSED": "req_to_module_mapping_counter"
    },
)
graph.add_edge("req_to_module_mapping_fix", "req_to_module_mapping_gate")
graph.add_edge("req_to_module_mapping_counter",
               "req_to_module_mapping_advance_module")

graph.add_conditional_edges(
    "interface_sketch_advance_module",
    route_advance_module,
    {
        "PROCEED": "module_interface_sketch",
        "FINISHED": "dependency_declaration_advance_module"
    },
)
graph.add_edge("module_interface_sketch", "module_interface_sketch_gate")
graph.add_conditional_edges(
    "module_interface_sketch_gate",
    route_module_interface_sketch_gate,
    {
        "FAILED": "module_interface_sketch_fix",
        "PASSED": "module_interface_sketch_counter"
    },
)
graph.add_edge("module_interface_sketch_fix", "module_interface_sketch_gate")
graph.add_edge("module_interface_sketch_counter",
               "interface_sketch_advance_module")

graph.add_conditional_edges(
    "dependency_declaration_advance_module",
    route_advance_module,
    {
        "PROCEED": "module_dependency_declaration",
        "FINISHED": "combine_architecture_report"
    },
)
graph.add_edge("module_dependency_declaration",
               "module_dependency_declaration_gate")
graph.add_conditional_edges(
    "module_dependency_declaration_gate",
    route_module_dependency_declaration_gate,
    {"FAILED": "module_dependency_declaration_fix",
        "PASSED": "module_dependency_declaration_counter"},
)
graph.add_edge("module_dependency_declaration_fix",
               "module_dependency_declaration_gate")
graph.add_edge("module_dependency_declaration_counter",
               "dependency_declaration_advance_module")

graph.add_edge("combine_architecture_report", "report_status")
graph.add_edge("report_status", END)

app = graph.compile()
