from skills.common import Skill


class ModuleDecompositonSkill(Skill):
    def __init__(self, llm: object = None):
        super().__init__(
            path_to_skill_md="skills/module_decomposition/SKILL.md",
            llm=llm,
        )

    def invoke(self, skeleton, req_digest, glossary):
        return super().invoke(skeleton, req_digest, glossary)

    def fix(self, skeleton, req_digest, glossary, previous_answer, problem):
        return super().fix(skeleton, req_digest, glossary, previous_answer, problem)
