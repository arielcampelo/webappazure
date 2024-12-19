import spacy 
import datetime
import os 
import json 
import re 
import string 
import chardet

from ccodes import countryIsoCodes

from tokenizers import TextCatTokenizer
from tokenizers import NerBrTokenizer
from tokenizers import NerHkTokenizer





class Extractor (object):

    def __init__(self):
        self.__path = os.getcwd()
        # load textcat model for identifying the country
        self.nlp_textcat = spacy.load('xx_textcat_class')
        # load the tokenizer for textcat preprocessing
        self.textcat_tokenizer = TextCatTokenizer()
        self.ner_tokenizer = None
      
    
    def extract(self, text):
        entries = self.__parse_entry(text)
        extracted_entities = []
        for entry in entries:
            entities = self.__get_entities(entry)
            extracted_entities.append(entities)
        return extracted_entities

    def __get_entities(self, text):
        
        text = text.replace("sif","SIF")
        text = text.replace("Sif","SIF")
        search =  re.search("SIF",text)
        if not search == None:
            sifMAPA,text = self.extract_sif(text)
        else:
            sifMAPA = 'null'

        
        flag = {}
        flag['needHinTL'] = False
        warning = ''
        layers = {}
        
        # make entities dict
        entities = self.__make_out_dict()
        entities['sifMAPA'] = sifMAPA
        # get the country
        doc_country = self.nlp_textcat(self.textcat_tokenizer.tokenize(text))
        cat_probs = doc_country.cats
        country = max(cat_probs, key=cat_probs.get)
        model_prob = cat_probs[country]

        entities['country_model_prob'] = model_prob
        if float(model_prob)<0.70:
            layers['country confiability'] = model_prob
            flag['needHinTL'] = True
            entities['country_model_prob'] = 'low'
            

        # add the meta identified country
        meta_dict = {'country': country, 'country_prob': cat_probs[country]}
        entities['meta'] = meta_dict
        # load the ner org model for the identified country 
        choosen = self.__choose_ner_model(country)


        if choosen == 'NOT MODELED':
            layers['country'] = f'{country} does not have a model'
            flag['layers'] = layers
            entities['flag'] = str(flag)
            entities['name'] =  'null' 
            entities['address'] = 'null'
            entities['countryname'] = 'notModeled'
            entities['countryid'] = 'NM' 
            return entities
        
        # set the country iso code
        countryid = self.__get_countryid(country)
        entities['countryid'] = countryid
        
        # separate ORG from ADDRESS
        org = []
        add = []
        ner_tokenized_text = self.ner_tokenizer.tokenize(text)
        doc_org = self.nlp_ner_org(ner_tokenized_text)
        for token in doc_org:
            if token.ent_type_ == 'ORG':
                org.append(token.text)
            else:
                add.append(token.text)

                

        organization = ' '.join(org)
        address = ' '.join(add)
        # add identified entities
        entities['name'] = organization 
        entities['address'] = address
        # get details from ADDRESS
        doc_address = self.nlp_ner_address(address)
        for entity in doc_address.ents:
            if entity.label_ in  {'PCD','ZCD'}:
                entities['postcode'] += entity.text + ' '
            elif entity.label_ in  {'ADR','STR'}:
                entities['lineone'] += entity.text + ' '
            elif entity.label_ in {'BDT', 'CMP'}:
                entities['linetwo'] += entity.text + ' '
            elif entity.label_ in {'BID','BLD'}:
                entities['linethree'] += entity.text + ' '
            elif entity.label_ in {'SBD'}:
                entities['linefour'] += entity.text + ' '
            elif entity.label_ in {'CIT'}:
                entities['cityname'] += entity.text + ' '
            elif entity.label_ in {'CSD', 'REG'}:
                entities['citysubdivisionname'] += entity.text + ' '
            elif entity.label_ in {'CNT'}:
                entities['countryname'] = entity.text + ' '
            elif entity.label_ in {'CSB', 'STA'}:
                entities['countrysubdivisionname'] += entity.text + ' '
            elif entity.label_ in {'PHN', 'EML', 'PER', 'CTC', 'TAX','ATN'}:
                entities['contact'] += entity.text + ' '
        # strip 
        for k in entities:
            if k != 'meta':
                entities[k] = str(entities[k]).strip()

        entities['postcode'],layer = self.format_CEP(entities['postcode'],country)
        if layer != None:
            #warning += layer['warning']
            entities['postcode'] = 'error'

        if flag['needHinTL']:
            flag['layers'] = layers
            flag['warning'] = warning
        entities['flag'] = str(flag)
        # save log
        try:
            cod = str(chardet.detect(text))
        except:
            cod = 'None'
        data = entities
        data['text'] = text # to save raw data
        data['address_ents'] = self.doc2dict(doc_address)
        data['encoding'] = cod
        #self.save_to_logs(data)
        return entities
    
    def extract_sif(self,text):
        search =  re.search(r"SIF[: ]*[0-9]{1,4}",text)
        sif = search.group()
        text = text.replace(sif,'')
        return sif, text
        

    
    def __parse_entry(self, text):
        pattern1 = re.compile("POR CONTA E ORDEM DE", re.IGNORECASE)
        pattern2 = re.compile("ON BEHALF OF", re.IGNORECASE)
        match1 = pattern1.search(text)
        match2 = pattern2.search(text)
        if match1 and match2:
            begin_of_seq = match1.start()
            end_of_seq = match2.end()
            example1 = text[:begin_of_seq]
            example2 = text[end_of_seq:]
            return (self.__remove_punct_at_start(example1), self.__remove_punct_at_start(example2))
        elif match1:
            begin_of_seq = match1.start()
            end_of_seq = match1.end()
            example1 = text[:begin_of_seq]
            example2 = text[end_of_seq:]
            return (self.__remove_punct_at_start(example1), self.__remove_punct_at_start(example2))
        elif match2:
            begin_of_seq = match2.start()
            end_of_seq = match2.end()
            example1 = text[:begin_of_seq]
            example2 = text[end_of_seq:]
            return (self.__remove_punct_at_start(example1), self.__remove_punct_at_start(example2))
        else:
            return [self.__remove_punct_at_start(text)]
    
    def __remove_punct_at_start(self, s):
        while s and s[0] in string.punctuation:
            s = s[1:]
        return s.strip()
    
    def format_CEP(self,text,cnt):
        text = text.replace(' ','')
        text = re.sub(r"CEP[:]*","",text)
        if len(text)==0:
            return '',None

        if cnt == 'BRAZIL':
            text = re.sub(r"([0-9]{5})[-.]*([0-9]{3})",r"\1\2",text)

        layer = {}
        patterns = {'BRAZIL':r"[0-9]{5}[-]*[0-9]{3}",
                    'RUSSIA': r"[0-9]{6}",
                    'CHILE': r"[0-9]{7}"
                    }
        countrys = list(patterns)
        if cnt in countrys:
            search = re.search(patterns[cnt],text)
            if search == None:
                layer = 'erro'
                #layer['warning'] ='POSTCODE Format Error'
            else:
                layer = None
        else:
            layer = None
        

        return text.strip(),layer

        
    def __choose_ner_model(self, country):
        # load model
        if country == 'HONG KONG':
            self.ner_tokenizer = NerHkTokenizer()
            self.nlp_ner_org= spacy.load('en_ner_hk_org')
            self.nlp_ner_address = spacy.load('xx_ner_hk_address')
            return country
        elif country == 'BRAZIL':
            self.ner_tokenizer = NerBrTokenizer()
            self.nlp_ner_org= spacy.load('en_ner_br_org')
            self.nlp_ner_address = spacy.load('xx_ner_br_address')
            return country
        # elif country == 'CHILE':
        #     self.ner_tokenizer = NerClTokenizer()
        #     self.nlp_ner_org= spacy.load('en_ner_cl_org')
        #     self.nlp_ner_address = spacy.load('xx_ner_cl_address')
        #     return country
        # elif country == 'NETHERLANDS':
        #     self.ner_tokenizer = NerNlTokenizer()
        #     self.nlp_ner_org= spacy.load('en_ner_nl_org')
        #     self.nlp_ner_address = spacy.load('xx_ner_nl_address')
        #     return country
        # elif country == 'RUSSIA':
        #     self.ner_tokenizer = NerRuTokenizer()
        #     self.nlp_ner_org= spacy.load('en_ner_ru_org')
        #     self.nlp_ner_address = spacy.load('xx_ner_ru_address')
        #     return country
        # elif country == 'ITALY':
        #     self.ner_tokenizer = NerItTokenizer()
        #     self.nlp_ner_org= spacy.load('en_ner_it_org')
        #     self.nlp_ner_address = spacy.load('xx_ner_it_address')
        #     return country
        # elif country == 'GERMANY':
        #     self.ner_tokenizer = NerDeTokenizer()
        #     self.nlp_ner_org= spacy.load('en_ner_de_org')
        #     self.nlp_ner_address = spacy.load('xx_ner_de_address')
        #     return country
        # elif country == 'SPAIN':
        #     self.ner_tokenizer = NerEsTokenizer()
        #     self.nlp_ner_org= spacy.load('en_ner_es_org')
        #     self.nlp_ner_address = spacy.load('xx_ner_es_address')
        #     return country
        # elif country == 'EGYPT':
        #     self.ner_tokenizer = NerEgTokenizer()
        #     self.nlp_ner_org= spacy.load('en_ner_eg_org')
        #     self.nlp_ner_address = spacy.load('xx_ner_eg_address')
        #     return country
        # elif country == 'JORDANIA':
        #     self.ner_tokenizer = NerJoTokenizer()
        #     self.nlp_ner_org= spacy.load('en_ner_jo_org')
        #     self.nlp_ner_address = spacy.load('xx_ner_jo_address')
        #     return country
        # elif country == 'KOREA':
        #     self.ner_tokenizer = NerKrTokenizer()
        #     self.nlp_ner_org= spacy.load('xx_ner_kr_org')
        #     self.nlp_ner_address = spacy.load('xx_ner_kr_address')
        #     return country
        else:
            return 'NOT MODELED'
        

    
    def __get_countryid(self, country):
        # gets the iso code from a dict according to country name
        if country == 'HONG KONG':
            return 'HK'
        elif country == 'BRAZIL':
            return 'BR'
        elif country == 'CHILE':
            return 'CL'
        elif country == 'NETHERLANDS':
            return 'NL'
        elif country == 'RUSSIA':
            return 'RU'
        elif country == 'ITALY':
            return 'IT'
        elif country == 'GERMANY':
            return 'DE'
        elif country == 'SPAIN':
            return 'ES'
        elif country == 'EGYPT':
            return 'ES'
        elif country == 'JORDANIA':
            return 'JO'
        elif country == 'KOREA':
            return 'KR'
        else:
            return 'NM'
            
   
    def __make_out_dict(self):
        keys = [
            'name',
            'address',
            'postcode',
            'lineone',
            'linetwo',
            'linethree',
            'linefour',
            'linefive',
            'cityid',
            'cityname',
            'citysubdivisionname',
            'countryid',
            'countryname',
            'countrysubdivisionid',
            'countrysubdivisionname',
            'contact',
            'country_model_prob'
            ]
        out_dict = {}
        for k in keys:
            out_dict[k] = ''
        return out_dict
    
    def doc2dict(self, doc):
        dict_inst = {} 
        mapping = []
        for k in doc.to_json()['ents']:
            mapping.append([k['start'], k['end'], k['label']])
        dict_inst ['text'] = doc.to_json()['text']
        dict_inst ['label'] = mapping
        return dict_inst

    def save_to_logs(self, data):
        # Get the current date in the format YYYY-MM-DD
        now = datetime.datetime.now()
        date_str = now.strftime('%Y-%m-%d')
        
        # Create a directory for the logs if it doesn't exist
        logs_dir = os.path.join(os.getcwd(), 'logs')
        os.makedirs(logs_dir, exist_ok=True)
        
        # Create subdirectories for year, if it doesn't exist
        year_dir = os.path.join(logs_dir, str(now.year))
        os.makedirs(year_dir, exist_ok=True)
        
        # add date time
        time_str = now.strftime('%H-%M-%S-%f')
        data['time'] = date_str + '-' + time_str

        # set version
        data['version'] = '2.3.4'
        
        # Create a filename based on the  date 
        filename = os.path.join(year_dir, f'{date_str}.jsonl')
        
        # Save the data to the file as JSONL
        with open(filename, 'a', encoding='utf-8') as fh:
            fh.write(json.dumps(data) + '\n')
        #print(f'Saved {len(data)} items to {filename}')
