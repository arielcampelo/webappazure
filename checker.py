import os 
import spacy 
import datetime
import json 



class Checker (object):

    def __init__(self):
        self.erros_dict = {
    "1001": "Invalid input format",
    "1002": "Required label not extracted",
    "1003": "Order in extracted labels is incorrect",
    "1004": "Data type conversion error",
    "1005": "Missing required data",
    "1006": "Extracted format incorrect",
    "1007": "Missing model to specific task",
    "1008": "Confidence too low"
  }


    
    def pre_check(self,text):
        if type(text) != type("string"):
            return 1001
        if len(text) <10:
            return 1005
        return
    
    def pos_check(self,entities):
        
        if entities['countryname'] == 'notModeled':
            return 1007
        
        if entities['country_model_prob'] == 'low':
            return 1008
        
        if entities['postcode'] == 'error':
            return 1006

        if entities['address'] == '' :
            return 1002
        
        return None
    
    # def extract_flag(self,text):
    #     tokenized_text = self.ner_tokenizer.tokenize(text)
    #     doc = self.nlp(tokenized_text)
    #     flag = self.get_flag(doc)    
    #     return flag
    
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
        data['version'] = '2.0.0'
        
        # Create a filename based on the date 
        filename = os.path.join(year_dir, f'{date_str}.jsonl')
        
        # Save the data to the file as JSONL
        with open(filename, 'a', encoding='utf-8') as fh:
            fh.write(json.dumps(data) + '\n')
        #print(f'Saved {len(data)} items to {filename}')
