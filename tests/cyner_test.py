import unittest

import cyner

class TestCynerMethods(unittest.TestCase):
    @unittest.skip("reason for skipping")
    def test_cyner_heuristics(self):

        print("Using regexes")
        model = cyner.CyNER(use_heuristic=True,priority="H")

        text = """Example email abcd@gmail.com. 
        Example website www.google.com. 
        A sample file name xy_2.exe. 
        A file hash 446833e3f8b04d4c3c2d2288e456328266524e396adbfeba3769d00727481e80"""

        print(text)


        entities = model.get_entities(text)

        checks = []
        for e in entities:
            print(e)
    @unittest.skip("reason for skipping")
    def test_cyner_flair(self):
        print("Using flair with regexes")

        text = """
        Example email abcd@gmail.com. Example website www.google.com. A sample file name xy_2.exe. 
        A file hash 446833e3f8b04d4c3c2d2288e456328266524e396adbfeba3769d00727481e80. 
        The company Google. The CEO of the company Google Alphabet Inc. is Mr. Sundar Pichai"""


        print(text)

        model = cyner.CyNER(use_heuristic=True, flair_model='ner',priority="HF")

        entities = model.get_entities(text)


        checks = []
        for e in entities:
            print(e)

    @unittest.skip("reason for skipping")
    def test_cyner_flair(self):
        print("Using flair with regexes")

        text = """
        Example email abcd@gmail.com. Example website www.google.com. A sample file name xy_2.exe. 
        A file hash 446833e3f8b04d4c3c2d2288e456328266524e396adbfeba3769d00727481e80. 
        The company Google. The CEO of the company Google Alphabet Inc. is Mr. Sundar Pichai"""


        print(text)

        model = cyner.CyNER(use_heuristic=True, flair_model='ner',priority="HF")

        entities = model.get_entities(text)


        checks = []
        for e in entities:
            print(e)
    @unittest.skip("reason for skipping")
    def test_cyner_spacy(self):
        print("Using flair with regexes")

        text = """
        Example email abcd@gmail.com. Example website www.google.com. A sample file name xy_2.exe. 
        A file hash 446833e3f8b04d4c3c2d2288e456328266524e396adbfeba3769d00727481e80. 
        The company Google. The CEO of the company Google Alphabet Inc. is Mr. Sundar Pichai"""


        print(text)

        model = cyner.CyNER(use_heuristic=True, spacy_model='ner',priority="HS")

        entities = model.get_entities(text)


        checks = []
        for e in entities:
            print(e)

    @unittest.skip("reason for skipping")
    def test_cyner_spacy(self):
        print("Using flair with regexes")

        text = """
        Example email abcd@gmail.com. Example website www.google.com. A sample file name xy_2.exe. 
        A file hash 446833e3f8b04d4c3c2d2288e456328266524e396adbfeba3769d00727481e80. 
        The company Google. The CEO of the company Google Alphabet Inc. is Mr. Sundar Pichai"""


        print(text)

        model = cyner.CyNER(use_heuristic=True, spacy_model="en_core_web_sm",priority="HS")

        entities = model.get_entities(text)


        checks = []
        for e in entities:
            print(e)

    def test_pretrained(self):
        print("Using pretrained")

        text = """ Proofpoint report mentions that the German-language messages were turned off once the UK messages were established, 
        indicating a conscious effort to spread FluBot 446833e3f8b04d4c3c2d2288e456328266524e396adbfeba3769d00727481e80 in Android phones.
        """

        print(text)

        model = cyner.CyNER(transformer_model='xlm-roberta-large', use_heuristic=False, flair_model=None, spacy_model=None,model_dir="/home/robomotic/cti-llm/NER/ckpt_large/model.safetensors")

        entities = model.get_entities(text)


        checks = []
        for e in entities:
            print(e)
            
        """
        model = cyner.CyNER(transformer_model='xlm-roberta-large', use_heuristic=True, flair_model=None, spacy_model=None,model_dir="/home/robomotic/cti-llm/NER/logs/xlm-roberta-base")

        entities = model.get_entities(text)


        checks = []
        for e in entities:
            print(e)

        
        model = cyner.CyNER(transformer_model='xlm-roberta-large', use_heuristic=True, flair_model="ner",model_dir="/home/robomotic/cti-llm/NER/logs/xlm-roberta-base")

        entities = model.get_entities(text)


        checks = []
        for e in entities:
            print(e)
        """
if __name__ == '__main__':
    unittest.main()



