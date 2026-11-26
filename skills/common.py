from langchain_llama_cpp import ChatLlama
from langchain_core.messages import SystemMessage
from langchain_core.messages import HumanMessage


class Skill:
    def __init__(self, path_to_skill_md: str, llm: object = None):
        self.llm = llm if llm is not None else ChatLlama(
            model="ccore/Qwen3.5-4B-3D-Coder-Q8_0.gguf",
            base_url="http://server.lan:8080/",
            api_key="no-api-key",
            temperature=0.1,
        )
        self.skill_decripton = open(path_to_skill_md, "rt").read()

    def invoke(self, **kwargs):
        human_message_content = "\n".join([
            f"{key.replace("_", " ")}: {val}" for key, val in kwargs.items()
        ])
        resp = self.llm.invoke([
            SystemMessage(content=self.skill_decripton),
            HumanMessage(content=human_message_content),
        ])

        return resp

    def fix(self, **kwargs):
        self.invoke(**kwargs)
