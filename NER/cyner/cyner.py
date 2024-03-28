import sys
import os

from .entity_extraction_factory import EntityExtractionFactory as eef
from .entity import Entity

class CyNER(): 
    def __init__(self, transformer_model=None, use_heuristic=True, flair_model='ner', spacy_model=None, priority='HTFS'):

        self.transformer_model = None
        if transformer_model:
            self.transformer_ner = eef.get_entity_extraction_model('transformers', {'model': transformer_model})

        self.heuristic_ner = None
        if use_heuristic:
            self.heuristic_ner = eef.get_entity_extraction_model('heuristics', {})
        self.flair_ner = None
        if flair_model:
            self.flair_ner = eef.get_entity_extraction_model('flair', {'model': flair_model})
        self.spacy_ner = None
        if spacy_model:
            self.spacy_ner = eef.get_entity_extraction_model('spacy', {'model': spacy_model})
        self.priority = priority
        
    def get_model_corresponding_to_priority(self, letter):
        if letter.upper() == 'H':
            return self.heuristic_ner
        elif letter.upper() == 'T':
            return self.transformer_ner
        elif letter.upper() == 'F':
            return self.flair_ner
        elif letter.upper() == 'S':
            return self.spacy_ner
        else:
            raise ValueError('Unknown letter in priority, must be in [HTFS]')
            
    def construct_priority_model_list(self):
        models = []
        
        for letter in self.priority:
            m = self.get_model_corresponding_to_priority(letter)
            if m is not None:
                models.append(m)
        return models
    
    def check_overlap(self, entities, candidate):
        for e in entities:
            if candidate.start >= e.start and candidate.start < e.end:
                return True
            if candidate.end -1 >= e.start and candidate.end <= e.end:
                return True
            if candidate.start <= e.start and candidate.end >= e.end:
                return True
        return False
    
    def merge_entities(self,cur_entities, candidate_entities):
        for candidate in candidate_entities:
            if not self.check_overlap(cur_entities, candidate):
                cur_entities.append(candidate)
        return cur_entities
    
    def get_entities(self, text):
        merged_entities = []
        models = self.construct_priority_model_list()
        
        for model in models:
            entities = model.get_entities(text)
            merged_entities = self.merge_entities(merged_entities, entities)

        self.merged_entities = merged_entities
        return merged_entities

    def get_stix_entities(self):

        """
            Map them to STIX objects
        """
        stix_entities= []
        for e in self.merged_entities:
            stix_e = Entity(e.start,e.end,e.text,e.entity_type,e.confidence)

            if e.entity_type == "MISC": 
                continue
            elif e.entity_type == "Location"  or e.entity_type == "LOC": 
                # we don't know this can be a region, country, city, etc
                stix_e.entity_type = "location"
                stix_entities.append(stix_e)
            elif e.entity_type == "Malware": 
                stix_e = "malware.name"
                stix_entities.append(stix_e)
            elif e.entity_type == "Organization" or e.entity_type=="ORG": 
                # we don't know this can be a region, country, city, etc
                stix_e.entity_type = "location"
                stix_entities.append(stix_e)
            elif e.entity_type == "Person" or e.entity_type == "PER": 
                # we don't know this can be a region, country, city, etc
                stix_e.entity_type = "identity.name"
                stix_entities.append(stix_e)
            elif e.entity_type == "Domain": 
                # we don't know this can be a region, country, city, etc
                stix_e.entity_type = "domain-name.value"
                stix_entities.append(stix_e)
            elif e.entity_type.lower() == "filename": 
                stix_e.entity_type = "file.name"
                stix_entities.append(stix_e)
            elif e.entity_type.lower() == "email": 
                stix_e.entity_type = "email.value"
                stix_entities.append(stix_e)
            else:
                continue
            
        return stix_entities
