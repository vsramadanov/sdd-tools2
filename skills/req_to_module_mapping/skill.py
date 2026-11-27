from skills.common import Skill


class ReqToModuleMappingSkill(Skill):
    def __init__(self, llm: object = None):
        super().__init__(
            path_to_skill_md="skills/req_to_module_mapping/SKILL.md",
            llm=llm,
        )

    def invoke(self, requirement, modules):
        return super().invoke(requirement, modules)

    def fix(self, requirement, modules, previous_answer, problem):
        return super().fix(requirement, modules, previous_answer, problem)
