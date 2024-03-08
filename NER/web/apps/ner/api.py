
from django.conf import settings
from django.db import transaction

from ninja import Router
from typing import List, Optional
from pydantic import BaseModel, Field
from langchain.chat_models import ChatOpenAI
from langchain.callbacks import get_openai_callback
from kor import create_extraction_chain, from_pydantic, JSONEncoder

from .models import InputText, Metadata, Output


router = Router()

class EntityExtractionRequest(BaseModel):
    malware: Optional[List[str]] = Field(None, description="Malware names (e.g., 'LockBit, DarkSide, WannaCry').")
    threat_actor: Optional[List[str]] = Field(None, description="Names of threat actors (e.g., 'BlueCharlie, APT28, Lazarus Group').")
    software: Optional[List[str]] = Field(None, description="Software names (e.g., 'LockBit 2.0, Windows 10, OpenSSH').")
    ttp: Optional[List[str]] = Field(None, description="Tactics, Techniques, and Procedures (e.g., 'spear-phishing, drive-by download, credential stuffing').")
    os: Optional[List[str]] = Field(None, description="Operating System names (e.g., 'Windows, Linux, macOS').")
    hardware: Optional[List[str]] = Field(None, description="Hardware names (e.g., 'iPhone, Netgate Firewall, Raspberry Pi').")
    username: Optional[List[str]] = Field(None, description="Usernames (e.g., 'john_doe, admin, guest').")
    organization: Optional[List[str]] = Field(None, description="Organization names (e.g., 'Insikt Group, OpenAI, Microsoft').")
    sector: Optional[List[str]] = Field(None, description="Industry sectors (e.g., 'finance, healthcare, energy').")
    geo_location: Optional[List[str]] = Field(None, description="Geographical locations (e.g., 'Russia, New York, Silicon Valley').")
    exploit_name: Optional[List[str]] = Field(None, description="Exploit names (e.g., 'EternalBlue, Heartbleed, Shellshock').")
    date: Optional[List[str]] = Field(None, description="Dates (e.g., 'March 2023, September 2022, Q2 2021').")
    time: Optional[List[str]] = Field(None, description="Times (e.g., '10:00 AM, 23:45, midnight').")

class TextInput(BaseModel):
    text: str

@router.post("/process-text")
def process_text(request, text_input: TextInput):
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

        with transaction.atomic():
            # Save the input text
            input_obj = InputText.objects.create(input_text=text_input.text)
            
            # Save the metadata
            Metadata.objects.create(
                input_text=input_obj,
                full_prompt=chain.prompt.format_prompt(text="[user input]").to_string(),  
                total_tokens=cb.total_tokens,
                prompt_tokens=cb.prompt_tokens,
                completion_tokens=cb.completion_tokens,
                successful_requests=cb.successful_requests,
                total_cost=cb.total_cost
            )
            
            # Save the output
            Output.objects.create(
                input_text=input_obj,
                output_data=json_encoder.decode(result['text']['raw'])  # Ensure this is in a format suitable for your JSONField
            )
        
        return json_encoder.decode(result['text']['raw'])  # PLUS ID