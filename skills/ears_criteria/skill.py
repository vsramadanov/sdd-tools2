from skills.common import Skill


class EarsCriteriaSkill(Skill):
    def __init__(self, llm: object = None):
        super().__init__(
            path_to_skill_md="skills/ears_criteria/SKILL.md",
            llm=llm,
        )

    def invoke(self, requirement, glossary):
        return super().invoke(requirement, glossary)

    def fix(self, requirement, glossary, previous_answer, problem):
        return super().fix(requirement, glossary, previous_answer, problem)
