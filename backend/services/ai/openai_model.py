from openai import OpenAI
from services.ai.base import baseModel
from os import getenv
from dotenv import load_dotenv

load_dotenv()

api_key = getenv("OPENAI_KEY")


class OpenAIModel(baseModel):
    def __init__(self):
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-5-mini"
        return


    def parse_description(self, description: str) -> list:

        res = self.client.responses.create(
            model=self.model,
            instructions=self.PARSE_DESC_SYSTEM_PROMPT,
            input=f"{self.PARSE_DESC_USER_PROMPT}\n{description}",
            reasoning={"effort":"minimal"}
        )

        return res.output_text

    def match_resume(self, experience: str, degree: str, resume: str) -> dict:

        res = self.client.responses.create(
            model=self.model,
            instructions=self.MATCH_RESUME_SYSTEM_PROMPT,
            input=f"{self.MATCH_RESUME_USER_PROMPT}\nExperience Required: {experience}\nDegree Required: {degree}\nResume: {resume}",
            reasoning={"effort":"minimal"}
        )

        return res.output_text
