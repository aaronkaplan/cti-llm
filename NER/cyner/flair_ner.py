from flair.data import Sentence
from flair.models import SequenceTagger
import logging
from .entity_extraction import EntityExtraction
from .entity import Entity


class Flair(EntityExtraction):
    """
    Entity extraction using Flair NER model
    """
    def __init__(self, config):
        super().__init__(config)
        self.tagger = SequenceTagger.load(config['model'])

    def train(self):
        pass

    def get_entities(self, text):
        sentence = Sentence(text)
        self.tagger.predict(sentence)
        pred = sentence.to_dict(tag_type='ner')
        entities = []
        for x in pred['entities']:
            if 'labels' in x:
                for label in x['labels']:
                    entities.append(Entity(x['start_pos'], x['end_pos'], x['text'], label['value'], label['confidence']))
            else:
                logging.warning("Label is missing for entity: %s" %s)

        return entities
