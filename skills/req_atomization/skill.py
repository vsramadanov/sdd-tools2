from skills.common import Skill


class ReqAtomizationSkill(Skill):
    def __init__(self, llm: object = None):
        super().__init__(
            path_to_skill_md="skills/req_atomization/SKILL.md",
            llm=llm,
        )

    def invoke(self, context, decisions):
        return super().invoke(context, decisions)

    def fix(self, context, answers, previous_answer, problem):
        return super().fix(context, answers, previous_answer, problem)
