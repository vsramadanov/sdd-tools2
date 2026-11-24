import json
import unittest

from langchain_core.messages import AIMessage
from langchain_core.language_models.fake_chat_models import GenericFakeChatModel

from requirements import app

from utils.types import Context
from test.mock_skill import MockLlmSkills


class TestRequirementsGraph(unittest.TestCase):
    def read_json(self, filename) -> str:
        with open(filename, "rt") as fd:
            raw = fd.read()
            return json.dumps(json.loads(raw))

    def test_smoketest(self):
        ctx = self.read_json("test/data/context.json")
        all_reqs = self.read_json("test/data/requirements.json")
        req1 = self.read_json("test/data/REQ-001.json")
        req2 = self.read_json("test/data/REQ-002.json")

        glossary = ctx[ctx.find("glossary")+12:-2]
        req1idx = all_reqs.find("REQ-001")
        req2idx = all_reqs.find("REQ-002")
        atomized_req1 = all_reqs[req1idx-8:req2idx-10]
        atomized_req2 = all_reqs[req2idx-8:-2]

        mock = MockLlmSkills(
            requests=[
                {"context": ctx, "answers": ""},
                {"requirement": atomized_req1, "glossary": glossary},
                {"requirement": atomized_req2, "glossary": glossary},
            ],
            responses=[
                all_reqs,
                req1,
                req2,
            ],
        )
        app.invoke(
            input={
                "initial_prompt": "hello",
                "context": Context.from_json(ctx),
                "answers": [{"Q": "hello", "A": "world"},],
            },
            context={
                "llm": GenericFakeChatModel(messages=iter([])),
                "llm_skill_collection": {
                    "req_atomization": mock,
                    "ears_criteria": mock,
                }
            },
        )
