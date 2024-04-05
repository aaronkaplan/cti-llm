## This is a quick and dirty wrapper for any NER Code
# TODO: Connect this to some NER lib like cyner
from typing import List, Optional
import re

from pydantic import BaseModel, Field
from langchain.chat_models import ChatOpenAI
from langchain.callbacks import get_openai_callback

# Langchain offers caching. Let's use it. See: https://python.langchain.com/docs/modules/model_io/llms/llm_caching
from langchain.globals import set_llm_cache
# from langchain.cache import SQLiteCache
from langchain.cache import InMemoryCache     # alternative in memory DB

from kor import create_extraction_chain, from_pydantic, JSONEncoder
from django.db import transaction
import spacy

from .models import InputText, Metadata, Output, Entity


# caching
set_llm_cache(InMemoryCache())
# or:
# set_llm_cache(SQLiteCache(database_path="/app/cache/langchain.db"))


def find_substring_positions(text, substrings_with_labels):
    # Initialize an empty list to hold all the entities
    entities = []

    # Iterate over the category and substrings in the input
    for label, substrings in substrings_with_labels.items():
        # Create a regex pattern for each category, with case insensitivity
        pattern = "|".join(substring.replace(" ", "\s+") for substring in substrings)

        print(pattern)
        # Use re.finditer to find all occurrences of the substrings, with the IGNORECASE flag
        matches = re.finditer(pattern, text, re.IGNORECASE | re.M)

        # Add found entities with their start, end positions, and the category label
        for match in matches:
            entities.append(
                {
                    "start": match.start(),
                    "end": match.end(),
                    "label": label,
                    "mention": str(match),
                }
            )

    # Sort entities by their start position
    entities.sort(key=lambda x: x["start"])

    return entities


class EntityExtractionRequest(BaseModel):
    malware: Optional[List[str]] = Field(
        None, description="Malware names (e.g., 'LockBit, DarkSide, WannaCry')."
    )
    threat_actor: Optional[List[str]] = Field(
        None,
        description="Names of threat actors (e.g., 'BlueCharlie, APT28, Lazarus Group').",
    )
    software: Optional[List[str]] = Field(
        None, description="Software names (e.g., 'LockBit 2.0, Windows 10, OpenSSH')."
    )
    ttp: Optional[List[str]] = Field(
        None,
        description="Tactics, Techniques, and Procedures (e.g., 'spear-phishing, drive-by download, credential stuffing').",
    )
    os: Optional[List[str]] = Field(
        None, description="Operating System names (e.g., 'Windows, Linux, macOS')."
    )
    hardware: Optional[List[str]] = Field(
        None,
        description="Hardware names (e.g., 'iPhone, Netgate Firewall, Raspberry Pi').",
    )
    username: Optional[List[str]] = Field(
        None, description="Usernames (e.g., 'john_doe, admin, guest')."
    )
    organization: Optional[List[str]] = Field(
        None,
        description="Organization names (e.g., 'Insikt Group, OpenAI, Microsoft').",
    )
    sector: Optional[List[str]] = Field(
        None, description="Industry sectors (e.g., 'finance, healthcare, energy')."
    )
    geo_location: Optional[List[str]] = Field(
        None,
        description="Geographical locations (e.g., 'Russia, New York, Silicon Valley').",
    )
    exploit_name: Optional[List[str]] = Field(
        None, description="Exploit names (e.g., 'EternalBlue, Heartbleed, Shellshock')."
    )
    date: Optional[List[str]] = Field(
        None, description="Dates (e.g., 'March 2023, September 2022, Q2 2021')."
    )
    time: Optional[List[str]] = Field(
        None, description="Times (e.g., '10:00 AM, 23:45, midnight')."
    )


class EntityExtractor:
    def __init__(self, text_input: str) -> None:
        self.nlp = spacy.load(
            "en_core_web_sm", exclude=["ner", "parser", "tagger", "lemmatizer"]
        )
        self.text_input = text_input
        llm = ChatOpenAI(
            model_name="gpt-3.5-turbo",
            temperature=0,
            max_tokens=2000,
            model_kwargs={"frequency_penalty": 0, "presence_penalty": 0, "top_p": 1.0},
        )
        schema, validator = from_pydantic(EntityExtractionRequest)
        self.chain = create_extraction_chain(
            llm, schema, encoder_or_encoder_class="json", validator=validator
        )
        self.json_encoder = JSONEncoder(use_tags=True)

        self.ents = None
        self.doc = None
        self.ent_positions = None
        self.id = 0

    def extract(self):
        return {
            "text": self.text_input,
            "ents": self.get_ent_positions(),
            "tokens": self.get_token(),
            "entities": self.get_entities(),
        }

    def get_entities(self):
        if not self.ents:
            with get_openai_callback() as cb:
                result = self.chain.invoke(self.text_input)
                ents = self.json_encoder.decode(result["text"]["raw"])

                with transaction.atomic():
                    # Save the input text
                    input_obj = InputText.objects.create(input_text=self.text_input)
                    self.id = input_obj.id

                    # Save the metadata
                    Metadata.objects.create(
                        input_text=input_obj,
                        full_prompt=self.chain.prompt.format_prompt(
                            text="[user input]"
                        ).to_string(),
                        total_tokens=cb.total_tokens,
                        prompt_tokens=cb.prompt_tokens,
                        completion_tokens=cb.completion_tokens,
                        successful_requests=cb.successful_requests,
                        total_cost=cb.total_cost,
                    )

                    # Save the output
                    Output.objects.create(
                        input_text=input_obj, output_data=ents
                    )  # Ensure this is in a format suitable for your JSONField

            self.ents = ents

        return self.ents

    def get_ent_positions(self):
        if not self.ent_positions:
            ent_positions_with_id = []
            for entity in find_substring_positions(self.text_input, self.get_entities()):
                ent_object = Entity.objects.create(
                    input_text_id=self.id,
                    mention=entity["mention"],
                    entity_class=entity["label"],
                    start=entity["start"],
                    end=entity["end"],
                )
                entity["id"] = ent_object.id
                ent_positions_with_id.append(entity)
            self.ent_positions = ent_positions_with_id
        return self.ent_positions

    def get_doc(self) -> List[str]:
        if not self.doc:
            self.doc = self.nlp(self.text_input)
        return self.doc

    def get_token(self):
        token_list = []
        for token in self.get_doc():
            token_list.append(
                {"id": token.i, "start": token.idx, "end": token.idx + len(token)}
            )
        return token_list

    def get_spans(self):
        ent_spans = []
        for ent in self.get_ent_positions():
            span = self.get_doc().char_span(
                ent["start"],
                ent["end"],
                label=ent["label"],
                alignment_mode="expand",
            )
            ent_spans.append(span)
        return ent_spans
