from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from langchain.chat_models import ChatOpenAI
from langchain.callbacks import get_openai_callback
from kor import create_extraction_chain, from_pydantic, JSONEncoder
from typing import List, Optional
from pydantic import BaseModel, Field

app = FastAPI()

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")


class EntityExtractionRequest(BaseModel):
    malware: Optional[List[str]] = Field(
        default=None,
        description="Malware names (e.g., 'LockBit, DarkSide, WannaCry')."
    )
    threat_actor: Optional[List[str]] = Field(
        default=None,
        description="Names of threat actors (e.g., 'BlueCharlie, APT28, Lazarus Group')."
    )
    software: Optional[List[str]] = Field(
        default=None,
        description="Software names (e.g., 'LockBit 2.0, Windows 10, OpenSSH')."
    )
    ttp: Optional[List[str]] = Field(
        default=None,
        description="Tactics, Techniques, and Procedures (e.g., 'spear-phishing, drive-by download, credential stuffing')."
    )
    os: Optional[List[str]] = Field(
        default=None,
        description="Operating System names (e.g., 'Windows, Linux, macOS')."
    )
    hardware: Optional[List[str]] = Field(
        default=None,
        description="Hardware names (e.g., 'iPhone, Netgate Firewall, Raspberry Pi')."
    )
    username: Optional[List[str]] = Field(
        default=None,
        description="Usernames (e.g., 'john_doe, admin, guest')."
    )
    organization: Optional[List[str]] = Field(
        default=None,
        description="Organization names (e.g., 'Insikt Group, OpenAI, Microsoft')."
    )
    sector: Optional[List[str]] = Field(
        default=None,
        description="Industry sectors (e.g., 'finance, healthcare, energy')."
    )
    geo_location: Optional[List[str]] = Field(
        default=None,
        description="Geographical locations (e.g., 'Russia, New York, Silicon Valley')."
    )
    exploit_name: Optional[List[str]] = Field(
        default=None,
        description="Exploit names (e.g., 'EternalBlue, Heartbleed, Shellshock')."
    )
    date: Optional[List[str]] = Field(
        default=None,
        description="Dates (e.g., 'March 2023, September 2022, Q2 2021')."
    )
    time: Optional[List[str]] = Field(
        default=None,
        description="Times (e.g., '10:00 AM, 23:45, midnight')."
    )


class TextInput(BaseModel):
    text: str


@app.post("/process-text")
async def process_text(text_input: TextInput):
    llm = ChatOpenAI(
        model_name="gpt-3.5-turbo",
        temperature=0,
        max_tokens=2000,
        model_kwargs={
            'frequency_penalty': 0,
            'presence_penalty': 0,
            'top_p': 1.0
        }
    )
    schema, validator = from_pydantic(EntityExtractionRequest)
    chain = create_extraction_chain(llm, schema, encoder_or_encoder_class="json", validator=validator)
    json_encoder = JSONEncoder(use_tags=True)

    with get_openai_callback() as cb:
        result = chain.invoke(text_input.text)
        print(f"Total Tokens: {cb.total_tokens}")
        print(f"Prompt Tokens: {cb.prompt_tokens}")
        print(f"Completion Tokens: {cb.completion_tokens}")
        print(f"Successful Requests: {cb.successful_requests}")
        print(f"Total Cost (USD): ${cb.total_cost}")
        # TODO: There should not be a need to decode this, this is broken
        return json_encoder.decode(result['text']['raw'])

    

@app.get("/")
async def read_root():
    return FileResponse('static/index.html', media_type='text/html')