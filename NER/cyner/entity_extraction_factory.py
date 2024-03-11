from .entity_extraction import EntityExtraction

class EntityExtractionFactory:
    def __init__(self):
        pass

    @staticmethod
    def get_entity_extraction_model(name: str, config: dict) -> EntityExtraction:
        name = name.lower()
        if name == 'flair':
            # a big dependency only import when needed
            from .flair_ner import Flair
            return Flair(config)
        elif name == 'spacy':
            from .spacy_ner import Spacy
            # this is instaleld already
            return Spacy(config)
        elif name == 'heuristics':
            from .heuristics_ner import HeuristicsNER
            return HeuristicsNER(config)
        elif name == 'transformers':
            from .transformers_ner import TransformersNER
            return TransformersNER(config)
        else:
            raise ValueError('Unknown entity extraction model')
