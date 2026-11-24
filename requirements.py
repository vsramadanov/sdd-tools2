from typing import TypedDict
from dataclasses import asdict
import json

from langgraph.graph import StateGraph, START, END
from langgraph.runtime import Runtime

from utils.types import Context
from utils.types import Requirement
from utils.types import AtomizedRequirement


class RequirementsState(TypedDict):
    initial_prompt: str
    answers: list[dict]
    context: Context
    all_requirements: list
    requirement: Requirement
    req_idx: int = 0
    req_atomization_gate_state: dict
    ears_criteria_gate_state: dict
    status: str
    llm_response: str


class RequirementsSmContext(TypedDict):
    llm: object
    llm_skill_collection: dict


def req_atomization(state: RequirementsState,
                    runtime: Runtime[RequirementsSmContext]) -> dict:
    llm_skill_collection = runtime.context.get("llm_skill_collection", None)
    skill = llm_skill_collection["req_atomization"]

    ctx = json.dumps(asdict(state["context"]), ensure_ascii=False)
    answers = ""
    response = skill.invoke(context=ctx, answers=answers)
    return {
        "llm_response": response,
    }


def req_atomization_gate(state: RequirementsState) -> dict:
    gate_state = state.get("req_atomization_gate_state", {})
    cnt = gate_state.get("counter", 0)
    return {
        "req_atomization_gate_state": {
            "passed": True,
            "reason": "",
            "counter": cnt,
        }
    }


def req_atomization_fix(state: RequirementsState,
                        runtime: Runtime[RequirementsSmContext]) -> dict:
    llm_skill_collection = runtime.context.get("llm_skill_collection", None)
    skill = llm_skill_collection["req_atomization"]

    message = state["req_atomization_gate_state"]["reason"]
    cnt = state["req_atomization_gate_state"]["counter"]

    ctx = json.dumps(asdict(state["context"]), ensure_ascii=False)
    answers = ""
    previous_responce = state["llm_response"]
    response = skill.invoke(context=ctx,
                            answers=answers,
                            previous_result=previous_responce,
                            problem=message)
    return {
        "llm_response": response,
    }


def parse_requirements(state: RequirementsState) -> dict:
    response = state["llm_response"]
    data = json.loads(response)
    reqs = [AtomizedRequirement.from_dict(item)
            for item in data["requirements"]]
    return {
        "all_requirements": reqs,
    }


def advance_requirement(state: RequirementsState) -> dict:
    idx = state.get("req_idx", 0)
    all_requirements = state["all_requirements"]
    return {
        "requirement": all_requirements[idx],
        "req_idx": idx,
    }


def ears_criteria(state: RequirementsState,
                  runtime: Runtime[RequirementsSmContext]) -> dict:
    llm_skill_collection = runtime.context.get("llm_skill_collection", None)
    skill = llm_skill_collection["ears_criteria"]

    req = json.dumps(asdict(state["requirement"]), ensure_ascii=False)
    glossary = ", ".join([
        json.dumps(asdict(item)) for item in state["context"].glossary
    ])
    response = skill.invoke(requirement=req,
                            glossary=glossary)
    return {
        "llm_response": response
    }


def ears_criteria_gate(state: RequirementsState) -> dict:
    gate_state = state.get("ears_criteria_gate_state", {})
    cnt = gate_state.get("counter", 0)

    return {
        "ears_criteria_gate_state": {
            "passed": True,
            "reason": "",
            "counter": cnt,
        }
    }


def ears_criteria_fix(state: RequirementsState,
                      runtime: Runtime[RequirementsSmContext]) -> dict:
    llm_skill_collection = runtime.context.get("llm_skill_collection", None)
    skill = llm_skill_collection["ears_criteria"]

    req = json.dumps(asdict(state["requirement"]), ensure_ascii=False)
    glossary = ", ".join([
        json.dumps(asdict(item)) for item in state["context"].glossary
    ])
    previous_responce = state["llm_response"]
    message = state["ears_criteria_gate_state"]["reason"]
    cnt = state["ears_criteria_gate_state"]["counter"]
    response = skill.invoke(requirement=req,
                            glossary=glossary,
                            previous_result=previous_responce,
                            problem=message,)
    return {
        "llm_response": response
    }


def req_counter(state: RequirementsState) -> dict:
    idx = state["req_idx"]
    return {
        "req_idx": idx + 1,
    }


def notify_status(state: RequirementsState) -> dict:
    return {}


def requirements_postprocess(state: RequirementsState) -> dict: ...


def route_req_atomization_gate(state: RequirementsState) -> str:
    return "PASS" if state["req_atomization_gate_state"]["passed"] else "FAILED"


def route_ears_criteria_gate(state: RequirementsState) -> str:
    return "PASS" if state["ears_criteria_gate_state"]["passed"] else "FAILED"


def route_extract_requirement(state: RequirementsState) -> str:
    idx = state["req_idx"]
    count = len(state["all_requirements"])
    return "PROCEED" if count > idx else "FINISH"


graph = StateGraph(state_schema=RequirementsState,
                   context_schema=RequirementsSmContext)

graph.add_node("req_atomization", req_atomization)
graph.add_node("req_atomization_gate", req_atomization_gate)
graph.add_node("req_atomization_fix", req_atomization_fix)
graph.add_node("parse_requirements", parse_requirements)
graph.add_node("advance_requirement", advance_requirement)
graph.add_node("ears_criteria", ears_criteria)
graph.add_node("ears_criteria_gate", ears_criteria_gate)
graph.add_node("ears_criteria_fix", ears_criteria_gate)
graph.add_node("req_counter", req_counter)
graph.add_node("requirements_postprocess", requirements_postprocess)
graph.add_node("notify_status", notify_status)


graph.add_edge(START, "req_atomization")
graph.add_edge("req_atomization", "req_atomization_gate")
graph.add_conditional_edges(
    "req_atomization_gate",
    route_req_atomization_gate,
    {
        "PASS": "parse_requirements",
        "FAILED": "req_atomization_fix",
    },
)
graph.add_edge("req_atomization_fix", "req_atomization_gate")
graph.add_edge("parse_requirements", "advance_requirement")
graph.add_edge("advance_requirement", "ears_criteria")
graph.add_edge("ears_criteria", "ears_criteria_gate")
graph.add_conditional_edges(
    "ears_criteria_gate",
    route_ears_criteria_gate,
    {
        "PASS": "req_counter",
        "FAILED": "ears_criteria_fix",
    },
)
graph.add_edge("ears_criteria_fix", "ears_criteria_gate")

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
