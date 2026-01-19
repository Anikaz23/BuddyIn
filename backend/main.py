import uvicorn
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from services.ai.openai_model import OpenAIModel
import json


openai_model = OpenAIModel()

class Resume(BaseModel):
    content: str


class JobDesc(BaseModel):
    description: str

class RefinedJobDesc(BaseModel):
    tools: List[str]
    hard_skills: List[str]
    soft_skills: List[str]
    bonus_skills: List[str]
    experience: str
    degree: str

app = FastAPI()

origin = [
    "https://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origin,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

memory_db = {"jobDesc": ""}

# routes
@app.get("/analyze", response_model=RefinedJobDesc)
def analyze_desc():
    if(not memory_db["jobDesc"]):
        return "No job description found.", status.HTTP_404_NOT_FOUND
    response = openai_model.parse_description(memory_db["jobDesc"])
    parsed_response = json.loads(response)
    return RefinedJobDesc(**parsed_response), status.HTTP_200_OK




@app.post("/analyze")
def receive_desc(job_desc: JobDesc):
    memory_db["jobDesc"] = job_desc.description
    return "Created", status.HTTP_201_CREATED

@app.post("/upload")
def upload_resume(resume: Resume):
    memory_db["resume"] = resume.content
    return "Created", status.HTTP_201_CREATED


# main program

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

