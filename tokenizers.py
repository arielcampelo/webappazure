import re 
import string 
import html 

class TextCatTokenizer(object):
    
    def __init__(self):
        pass

    def tokenize(self, text):
        punct = string.punctuation
        text = text.replace('\t', ' ')
        text = text.replace('\r', ' ')
        text = text.replace('\n', ' ')
        text = text.replace('#13;', '')
        text = text.replace('sif', 'SIF')
        text = text.replace('Sif', 'SIF')
        for c in punct:
            text = text.replace(c, ' ')
        text = re.sub('([0-9]+)', ' ', text)
        text = re.sub(' +', ' ', text)
        s = []
        for token in text.split(' '):
            if len(token.strip())!=0:
                s.append(token.strip())
        text = ' '.join(s)
        
        # Fix amp;
        text = text.replace('FLAT Camp ; D', 'FLAT C & D')
        text = text.replace(' amp ; ', ' & ')
        text = text.replace(' amp; ', ' & ')

        text = re.sub(' +', ' ', text.upper())
        return text

class NerHkTokenizer(object):

    def __init__(self):
        pass  

    def tokenize(self, text):
        punct = string.punctuation
        text = text.replace('\t', ' ')
        text = text.replace('\r', ' ')
        text = text.replace('\n', ' ')
        text = text.replace('#13;', '')
        text = text.replace('sif', 'SIF')
        text = text.replace('Sif', 'SIF')
        # separa a vírgula no final, precedida por qualquer caractere
        text = re.sub(r'(.*?),$', r'\1 ,', text)
        # separa a vírgula entre letras
        text = re.sub(r'(?<=[a-zA-Z]),', r' , ', text)
        # separa a vírgula precedida de ponto
        text = text.replace('.,', '. , ')
        # separa a vírgula sempre que iniciar a palavra
        text = re.sub(r',([a-zA-Z0-9])', r', \1', text)
        # vírgula seguida de espaço
        text = text.replace(', ', ' , ')
        # - 
        text = re.sub(r'(?<!\s)-|-(?!\s)', r' - ', text)
        # /
        text = re.sub(r'(?<=^)/|/(?=\s|$)', r' / ', text)
        text = re.sub(r'/(?=\s|$)', r' / ', text)
        
        # LIMITED.
        text = text.replace('LIMITED', ' LIMITED ')
        text = text.replace('LIMITED.', ' LIMITED .')
        text = text.replace('LIMITED', ' LIMITED ')
        text = text.replace('LTD', ' LTD ')
        text = text.replace('LTDA', ' LTDA ')
        text = text.replace('Ltd', ' Ltd ')
        text = text.replace('Ltda', ' Ltda ')
        text = text.replace('Limited', ' Limited ')
        text = text.replace('COMPANY', ' COMPANY ')
        text = text.replace('Company', ' Company ')
        text = text.replace('GROUP', ' GROUP ')
        # preserve terms
        terms = [
        'No.', 'NO.', 'nO.', 'no.','Nº.', 'NOS.', 'S/N°',
        ' HK', 'HK ', ' H.K.', 'H.K ', ' HK.', 'HK. ',
        'S.A.', 'E-MAIL:', 'e-mail', 'Email:', 'email', 'EMAIL', 'Tel:', 'TEL:', 'TEL.:', 'FAX:','fax', 'Fax:'
        'PLAZA', 'ADDRESS:', 'Add.:', 'ADD.:',
        'ATTN.:', 'ATTN:', 'Attn.:',
        'N.T.', 'NT.',
        'Bldg.', 'Blk.', 'BLDG.', 'bldg.',
        'Rd.', 'RD.', 'ROD.',
        'TRADING:', 'WEBSITE:'
        ]
        for term in terms:
            text = text.replace(term, ' ' + term + ' ')

        
        text = text.replace(' LTD . ', ' LTD. ')
        text = text.replace(' LTDA . ', ' LTDA. ')
        text = text.replace('/FAX', '/ FAX')
        text = text.replace('FAX', ' FAX')
        text = text.replace('.:', '.: ')
        text = text.replace(':', ': ')
        text = text.replace(';', ' ; ')
        

        text = re.sub (r"\(\s*(\d+)\s*\)", r"(\1)", text)
        text = re.sub (r"\(\s*([+-]?\d+)\s*\)", r"(\1)", text)
        text = text.replace('TEL :', 'TEL: ')
        text = text.replace('FAX :', 'FAX: ')
        text = text.replace('EMAIL :', 'EMAIL: ')
        text = text.replace('E - MAIL', 'E-MAIL')
        text = text.replace('e - mail', 'e-mail')
        text = text.replace('E - mail', 'E-mail')
        text = text.replace('MAIL :', 'MAIL: ')
        text = text.replace('PHONE :', 'PHONE: ')
        text = text.replace('ADDRESS :', 'ADDRESS: ')
        text = text.replace('ATTN :', 'ATTN: ')
        text = text.replace(' TERRITORIES.', ' TERRITORIES . ')

        text = text.replace('Tell:', ' Tel: ')
        text = text.replace('HongKong', ' Hong Kong ')
        text = text.replace('Kong.', ' Kong . ')
        text = text.replace('KONG.', ' KONG . ')
        text = text.replace('CENTRAL.', ' CENTRAL . ')
        text = text.replace('STREET-', ' STREET - ')
        text = text.replace('Street-', ' Street - ')
        text = text.replace('WEST-', ' WEST - WEST ')
        text = text.replace('Center.', ' Center . ')
        text = text.replace('CENTRE.', ' CENTRE . ')
        text = text.replace('IND.CENTRE', ' IND. CENTRE ')
        text = text.replace('LOG.CENTER.G/F', 'LOG. CENTER . G/F')
        
        text = re.sub (r"\(\s*([A-Za-z\.]+)\s*\)", r"(\1)", text)
       
        # separeate dot ending numbers
        text = re.sub(r'(\d+)\.\s*', r'\1 . ', text)
        # HONG KONG
        text = text.replace('HONG', ' HONG ')
        text = text.replace('KONG', ' KONG ')
        # KOWLOON
        text = text.replace('KOWLOON', ' KOWLOON ')
        # ()
        text = text.replace('(', ' (')
        text = text.replace(')', ') ')
        text = text.replace('( ', '(')
        text = text.replace(' )', ')')
        # []
        text = text.replace('[', ' [')
        text = text.replace(']', '] ')
        text = text.replace('[ ', '[')
        text = text.replace(' ]', ']')

        # /
        text = text.replace('/ ', ' / ')

        # Fix amp;
        text = text.replace('FLAT Camp ; D', 'FLAT C & D')
        text = text.replace(' amp ; ', ' & ')
        text = text.replace(' amp; ', ' & ')

        # remove duplicate spaces
        text = re.sub(' +', ' ', text)
        return text  

class NerBrTokenizer(object):

    def __init__(self):
        pass  

    def tokenize(self, text):
        punct = string.punctuation
        text = text.replace('\t', ' ')
        text = text.replace('\r', ' ')
        text = text.replace('\n', ' ')
        text = text.replace('#13;', '')
        text = text.replace('sif', 'SIF')
        text = text.replace('Sif', 'SIF')
        # separa a vírgula no final, precedida por qualquer caractere
        text = re.sub(r'(.*?),$', r'\1 ,', text)
        # separa a vírgula entre letras
        text = re.sub(r'(?<=[a-zA-Z]),', r' , ', text)
        # separa a vírgula precedida de ponto
        text = text.replace('.,', '. , ')
        # separa a vírgula sempre que iniciar a palavra
        text = re.sub(r',([a-zA-Z0-9])', r', \1', text)
        # vírgula seguida de espaço
        text = text.replace(', ', ' , ')
        # - 
        text = re.sub(r'(?<!\s)-|-(?!\s)', r' - ', text)
        # /
        text = re.sub(r'(?<=^)/|/(?=\s|$)', r' / ', text)
        text = re.sub(r'/(?=\s|$)', r' / ', text)
        
        # LIMITED.
        text = text.replace('LIMITED', ' LIMITED ')
        text = text.replace('LIMITED.', ' LIMITED .')
        text = text.replace('LIMITED', ' LIMITED ')
        text = text.replace('LTDA', ' LTDA ')
        text = text.replace('Ltda', ' Ltda ')
        text = text.replace('Limited', ' Limited ')
        text = text.replace('COMPANY', ' COMPANY ')
        text = text.replace('Company', ' Company ')
        text = text.replace('GROUP', ' GROUP ')
        # preserve terms
        terms = [
        'No.', 'NO.', 'nO.', 'no.','Nº.', 'NOS.', 'S/N°',
        ' HK', 'HK ', ' H.K.', 'H.K ', ' HK.', 'HK. ',
        'S.A.', 'E-MAIL:', 'e-mail', 'Email:', 'email', 'EMAIL', 'Tel:', 'TEL:', 'TEL.:', 'FAX:','fax', 'Fax:'
        'PLAZA', 'ADDRESS:', 'Add.:', 'ADD.:',
        'ATTN.:', 'ATTN:', 'Attn.:',
        'N.T.', 'NT.',
        'Bldg.', 'Blk.', 'BLDG.', 'bldg.',
        'Rd.', 'RD.', 'ROD.',
        'TRADING:', 'WEBSITE:'
        ]
        for term in terms:
            text = text.replace(term, ' ' + term + ' ')

        
        text = text.replace(' LTD . ', ' LTD. ')
        text = text.replace(' LTDA . ', ' LTDA. ')
        text = text.replace('/FAX', '/ FAX')
        text = text.replace('FAX', ' FAX')
        text = text.replace('.:', '.: ')
        text = text.replace(':', ': ')
        text = text.replace(';', ' ; ')
        

        text = re.sub (r"\(\s*(\d+)\s*\)", r"(\1)", text)
        text = re.sub (r"\(\s*([+-]?\d+)\s*\)", r"(\1)", text)
        text = text.replace('TEL :', 'TEL: ')
        text = text.replace('FAX :', 'FAX: ')
        text = text.replace('EMAIL :', 'EMAIL: ')
        text = text.replace('E - MAIL', 'E-MAIL')
        text = text.replace('e - mail', 'e-mail')
        text = text.replace('E - mail', 'E-mail')
        text = text.replace('MAIL :', 'MAIL: ')
        text = text.replace('PHONE :', 'PHONE: ')
        text = text.replace('ADDRESS :', 'ADDRESS: ')
        text = text.replace('ATTN :', 'ATTN: ')
        text = text.replace(' TERRITORIES.', ' TERRITORIES . ')

        text = text.replace('Tell:', ' Tel: ')
        text = text.replace('HongKong', ' Hong Kong ')
        text = text.replace('Kong.', ' Kong . ')
        text = text.replace('KONG.', ' KONG . ')
        text = text.replace('CENTRAL.', ' CENTRAL . ')
        text = text.replace('STREET-', ' STREET - ')
        text = text.replace('Street-', ' Street - ')
        text = text.replace('WEST-', ' WEST - WEST ')
        text = text.replace('Center.', ' Center . ')
        text = text.replace('CENTRE.', ' CENTRE . ')
        text = text.replace('IND.CENTRE', ' IND. CENTRE ')
        text = text.replace('LOG.CENTER.G/F', 'LOG. CENTER . G/F')
        
        text = re.sub (r"\(\s*([A-Za-z\.]+)\s*\)", r"(\1)", text)
        # remove duplicate spaces
        text = re.sub(' +', ' ', text)
        # separeate dot ending numbers
        text = re.sub(r'(\d+)\.\s*', r'\1 . ', text)
        # HONG KONG
        text = text.replace('HONG', ' HONG ')
        text = text.replace('KONG', ' KONG ')
        # KOWLOON
        text = text.replace('KOWLOON', ' KOWLOON ')
        # ()
        text = text.replace('(', ' (')
        text = text.replace(')', ') ')
        text = text.replace('( ', '(')
        text = text.replace(' )', ')')
        # []
        text = text.replace('[', ' [')
        text = text.replace(']', '] ')
        text = text.replace('[ ', '[')
        text = text.replace(' ]', ']')
        # /
        text = text.replace('/ ', ' / ')
        # BRAZIL
        text = text.replace('Brasil.', 'Brasil .')
        text = text.replace('BRASIL.', 'BRASIL .')
        # juntar números 9 . 9 -> 9.9
        text = re.sub(r'(\d+)\s*\.\s*(\d+)',r'\1.\2' , text)
        # juntar números 9 - 9 -> 9-9
        text = re.sub(r'(\d+)\s*\-\s*(\d+)',r'\1.\2' , text)
        # LTDA
        text = text.replace('Ltda . ', 'Ltda. ')
        text = text.replace('LTDA . ', 'LTDA. ')
        text = text.replace('SUL /LESTE', 'SUL/LESTE')
        

        # retokenize
        text = text.replace('/', ' / ')
        text = text.replace('S / A', 'S/A')
        text = text.replace('S / N', 'S/N')
        text = text.replace('S / Nº', 'S/Nº')
        text = text.replace('S / nº', ' S/nº')
        text = text.replace('/SIF', '/ SIF')
        text = text.replace('AV.SEN.', ' AV. SEN. ')
        text = re.sub(r"(\d+)\s*,\s*(\d+)", r"\1,\2", text)
        text = re.sub(r"SALA (\d+) - ([A-Z]) ", r"SALA \1-\2 ", text)
            
        # fix CEP
        text = text.replace('CEP: 35.700 . 178', 'CEP:35.700.178')
        result = re.search(r"CEP:\s*\d{2}\.\d{3}\s*\.\s*\d{3}", text)
        if result:
            w_cep = result.group()
            r_cep = w_cep.replace(' ', '')
            text = text.replace(w_cep, r_cep)
       
        # Fix amp;
        text = text.replace('FLAT Camp ; D', 'FLAT C & D')
        text = text.replace(' amp ; ', ' & ')
        text = text.replace(' amp; ', ' & ')

        # remove duplicate spaces
        text = re.sub(' +', ' ', text)

        text = text.replace('LTD A ', 'LTDA ')
        
        return text  
    
class NerClTokenizer(object):

    def __init__(self):
        pass  

    def tokenize(self, text):
        punct = string.punctuation
        text = text.replace('\t', ' ')
        text = text.replace('\r', ' ')
        text = text.replace('\n', ' ')
        text = text.replace('#13;', '')
        text = text.replace('sif', 'SIF')
        text = text.replace('Sif', 'SIF')
        # separa a vírgula no final, precedida por qualquer caractere
        text = re.sub(r'(.*?),$', r'\1 ,', text)
        # separa a vírgula entre letras
        text = re.sub(r'(?<=[a-zA-Z]),', r' , ', text)
        # separa a vírgula precedida de ponto
        text = text.replace('.,', '. , ')
        # separa a vírgula sempre que iniciar a palavra
        text = re.sub(r',([a-zA-Z0-9])', r', \1', text)
        # vírgula seguida de espaço
        text = text.replace(', ', ' , ')
        # - 
        text = re.sub(r'(?<!\s)-|-(?!\s)', r' - ', text)
        # /
        text = re.sub(r'(?<=^)/|/(?=\s|$)', r' / ', text)
        text = re.sub(r'/(?=\s|$)', r' / ', text)
        
        # LIMITED.
        text = text.replace('LIMITED', ' LIMITED ')
        text = text.replace('LIMITED.', ' LIMITED .')
        text = text.replace('LIMITED', ' LIMITED ')
        text = text.replace('LTDA', ' LTDA ')
        text = text.replace('Ltda', ' Ltda ')
        text = text.replace('Limited', ' Limited ')
        text = text.replace('COMPANY', ' COMPANY ')
        text = text.replace('Company', ' Company ')
        text = text.replace('GROUP', ' GROUP ')
        text = text.replace('S.A.', ' S.A. ')
        
        # preserve terms
        terms = [
        'No.', 'NO.', 'nO.', 'no.','Nº.', 'NOS.', 'S/N°',
        ' HK', 'HK ', ' H.K.', 'H.K ', ' HK.', 'HK. ',
        'S.A.', 'E-MAIL:', 'e-mail', 'Email:', 'email', 'EMAIL', 'Tel:', 'TEL:', 'TEL.:', 'FAX:','fax', 'Fax:'
        'PLAZA', 'ADDRESS:', 'Add.:', 'ADD.:',
        'ATTN.:', 'ATTN:', 'Attn.:',
        'N.T.', 'NT.',
        'Bldg.', 'Blk.', 'BLDG.', 'bldg.',
        'Rd.', 'RD.', 'ROD.',
        'TRADING:', 'WEBSITE:'
        ]

        for term in terms:
            text = text.replace(term, ' ' + term + ' ')

        text = text.replace(' LTD . ', ' LTD. ')
        text = text.replace(' LTDA . ', ' LTDA. ')
        text = text.replace('/FAX', '/ FAX')
        text = text.replace('FAX', ' FAX')
        text = text.replace('.:', '.: ')
        text = text.replace(':', ': ')
        text = text.replace(';', ' ; ')
        

        text = re.sub (r"\(\s*(\d+)\s*\)", r"(\1)", text)
        text = re.sub (r"\(\s*([+-]?\d+)\s*\)", r"(\1)", text)
        text = text.replace('TEL :', 'TEL: ')
        text = text.replace('FAX :', 'FAX: ')
        text = text.replace('EMAIL :', 'EMAIL: ')
        text = text.replace('E - MAIL', 'E-MAIL')
        text = text.replace('e - mail', 'e-mail')
        text = text.replace('E - mail', 'E-mail')
        text = text.replace('MAIL :', 'MAIL: ')
        text = text.replace('PHONE :', 'PHONE: ')
        text = text.replace('ADDRESS :', 'ADDRESS: ')
        text = text.replace('ATTN :', 'ATTN: ')
        text = text.replace(' TERRITORIES.', ' TERRITORIES . ')

        text = text.replace('Tell:', ' Tel: ')
        text = text.replace('HongKong', ' Hong Kong ')
        text = text.replace('Kong.', ' Kong . ')
        text = text.replace('KONG.', ' KONG . ')
        text = text.replace('CENTRAL.', ' CENTRAL . ')
        text = text.replace('STREET-', ' STREET - ')
        text = text.replace('Street-', ' Street - ')
        text = text.replace('WEST-', ' WEST - WEST ')
        text = text.replace('Center.', ' Center . ')
        text = text.replace('CENTRE.', ' CENTRE . ')
        text = text.replace('IND.CENTRE', ' IND. CENTRE ')
        text = text.replace('LOG.CENTER.G/F', 'LOG. CENTER . G/F')
        
       
        # remove duplicate spaces
        text = re.sub(' +', ' ', text)
       
        # HONG KONG
        text = text.replace('HONG', ' HONG ')
        text = text.replace('KONG', ' KONG ')
        # KOWLOON
        text = text.replace('KOWLOON', ' KOWLOON ')
        # ()
        text = text.replace('(', ' (')
        text = text.replace(')', ') ')
        text = text.replace('( ', '(')
        text = text.replace(' )', ')')
        # []
        text = text.replace('[', ' [')
        text = text.replace(']', '] ')
        text = text.replace('[ ', '[')
        text = text.replace(' ]', ']')
        # /
        text = text.replace('/ ', ' / ')
        # BRAZIL
        text = text.replace('Brasil.', 'Brasil .')
        text = text.replace('BRASIL.', 'BRASIL .')
        # CHILE
        text = text.replace('Chile.', ' Chile . ')
        text = text.replace('N°', ' N° ')
        text = text.replace('CHILE.', ' CHILE . ')

        text = text.replace(' - K', '-K')
        # juntar números 9 . 9 -> 9.9
        text = re.sub(r'(\d+)\s*\.\s*(\d+)',r'\1.\2' , text)
        # juntar números 9 - 9 -> 9-9
        text = re.sub(r'(\d+)\s*\-\s*(\d+)',r'\1.\2' , text)
        # LTDA
        text = text.replace('Ltda . ', 'Ltda. ')
        text = text.replace('LTDA . ', 'LTDA. ')
        text = text.replace('SUL /LESTE', 'SUL/LESTE')

        # retokenize
        text = text.replace('/', ' / ')
        text = text.replace('S / A', 'S/A')
        text = text.replace('S / N', 'S/N')
        text = text.replace('S / Nº', 'S/Nº')
        text = text.replace('S / nº', ' S/nº')
        text = text.replace('/SIF', '/ SIF')
        text = text.replace('AV.SEN.', ' AV. SEN. ')
        
        # Fix amp;
        text = text.replace('FLAT Camp ; D', 'FLAT C & D')
        text = text.replace(' amp ; ', ' & ')
        text = text.replace(' amp; ', ' & ')

        # remove duplicate spaces
        text = re.sub(' +', ' ', text)
        return text  

class NerNlTokenizer(object):

    def __init__(self):
        pass  

    def tokenize(self, text):
        punct = string.punctuation
        text = text.replace('\t', ' ')
        text = text.replace('\r', ' ')
        text = text.replace('\n', ' ')
        text = text.replace('#13;', '')
        text = text.replace('sif', 'SIF')
        text = text.replace('Sif', 'SIF')
        # separa a vírgula no final, precedida por qualquer caractere
        text = re.sub(r'(.*?),$', r'\1 ,', text)
        # separa a vírgula entre letras
        text = re.sub(r'(?<=[a-zA-Z]),', r' , ', text)
        # separa a vírgula precedida de ponto
        text = text.replace('.,', '. , ')
        # separa a vírgula sempre que iniciar a palavra
        text = re.sub(r',([a-zA-Z0-9])', r', \1', text)
        # vírgula seguida de espaço
        text = text.replace(', ', ' , ')
        # - 
        text = re.sub(r'(?<!\s)-|-(?!\s)', r' - ', text)
        # /
        text = re.sub(r'(?<=^)/|/(?=\s|$)', r' / ', text)
        text = re.sub(r'/(?=\s|$)', r' / ', text)
        
        # LIMITED.
        text = text.replace('LIMITED', ' LIMITED ')
        text = text.replace('LIMITED.', ' LIMITED .')
        text = text.replace('LIMITED', ' LIMITED ')
        text = text.replace('LTDA', ' LTDA ')
        text = text.replace('Ltda', ' Ltda ')
        text = text.replace('Limited', ' Limited ')
        text = text.replace('COMPANY', ' COMPANY ')
        text = text.replace('Company', ' Company ')
        text = text.replace('GROUP', ' GROUP ')
        text = text.replace('S.A.', ' S.A. ')
        
        # preserve terms
        terms = [
        'No.', 'NO.', 'nO.', 'no.','Nº.', 'NOS.', 'S/N°',
        ' HK', 'HK ', ' H.K.', 'H.K ', ' HK.', 'HK. ',
        'S.A.', 'E-MAIL:', 'e-mail', 'Email:', 'email', 'EMAIL', 'Tel:', 'TEL:', 'TEL.:', 'FAX:','fax', 'Fax:'
        'PLAZA', 'ADDRESS:', 'Add.:', 'ADD.:',
        'ATTN.:', 'ATTN:', 'Attn.:',
        'N.T.', 'NT.',
        'Bldg.', 'Blk.', 'BLDG.', 'bldg.',
        'Rd.', 'RD.', 'ROD.',
        'TRADING:', 'WEBSITE:'
        ]

        for term in terms:
            text = text.replace(term, ' ' + term + ' ')

        text = text.replace(' LTD . ', ' LTD. ')
        text = text.replace(' LTDA . ', ' LTDA. ')
        text = text.replace('/FAX', '/ FAX')
        text = text.replace('FAX', ' FAX')
        text = text.replace('.:', '.: ')
        text = text.replace(':', ': ')
        text = text.replace(';', ' ; ')
        

        text = re.sub (r"\(\s*(\d+)\s*\)", r"(\1)", text)
        text = re.sub (r"\(\s*([+-]?\d+)\s*\)", r"(\1)", text)
        text = text.replace('TEL :', 'TEL: ')
        text = text.replace('FAX :', 'FAX: ')
        text = text.replace('EMAIL :', 'EMAIL: ')
        text = text.replace('E - MAIL', 'E-MAIL')
        text = text.replace('e - mail', 'e-mail')
        text = text.replace('E - mail', 'E-mail')
        text = text.replace('MAIL :', 'MAIL: ')
        text = text.replace('PHONE :', 'PHONE: ')
        text = text.replace('ADDRESS :', 'ADDRESS: ')
        text = text.replace('ATTN :', 'ATTN: ')
        text = text.replace(' TERRITORIES.', ' TERRITORIES . ')

        text = text.replace('Tell:', ' Tel: ')
        text = text.replace('HongKong', ' Hong Kong ')
        text = text.replace('Kong.', ' Kong . ')
        text = text.replace('KONG.', ' KONG . ')
        text = text.replace('CENTRAL.', ' CENTRAL . ')
        text = text.replace('STREET-', ' STREET - ')
        text = text.replace('Street-', ' Street - ')
        text = text.replace('WEST-', ' WEST - WEST ')
        text = text.replace('Center.', ' Center . ')
        text = text.replace('CENTRE.', ' CENTRE . ')
        text = text.replace('IND.CENTRE', ' IND. CENTRE ')
        text = text.replace('LOG.CENTER.G/F', 'LOG. CENTER . G/F')
        
       
        # remove duplicate spaces
        text = re.sub(' +', ' ', text)
       
        # HONG KONG
        text = text.replace('HONG', ' HONG ')
        text = text.replace('KONG', ' KONG ')
        # KOWLOON
        text = text.replace('KOWLOON', ' KOWLOON ')
        # ()
        text = text.replace('(', ' (')
        text = text.replace(')', ') ')
        text = text.replace('( ', '(')
        text = text.replace(' )', ')')
        # []
        text = text.replace('[', ' [')
        text = text.replace(']', '] ')
        text = text.replace('[ ', '[')
        text = text.replace(' ]', ']')
        # /
        text = text.replace('/ ', ' / ')
        # BRAZIL
        text = text.replace('Brasil.', 'Brasil .')
        text = text.replace('BRASIL.', 'BRASIL .')
        # CHILE
        text = text.replace('Chile.', ' Chile . ')
        text = text.replace('N°', ' N° ')
        text = text.replace('CHILE.', ' CHILE . ')
        # NETHERLANDS
        text = text.replace('Netherlands.', 'Netherlands .')
        text = text.replace('NETHERLANDS.', 'NETHERLANDS .')
        text = text.replace('.The Netherlands', '. The Netherlands')
        text = text.replace('NE Woudenberg.', 'NE Woudenberg .')
        text = text.replace('Rotterdam.', 'Rotterdam .')
        text = text.replace('.Tel.:', '. Tel.:')
        text = text.replace('.Approval Number:', '. Approval Number:')
        text = text.replace('HOLLAND.', 'HOLLAND .')
        text = text.replace('Building.Handweg', 'Building. Handweg')
        
        


        # juntar números 9 . 9 -> 9.9
        text = re.sub(r'(\d+)\s*\.\s*(\d+)',r'\1.\2' , text)
        # juntar números 9 - 9 -> 9-9
        text = re.sub(r'(\d+)\s*\-\s*(\d+)',r'\1.\2' , text)
        # LTDA
        text = text.replace('Ltda . ', 'Ltda. ')
        text = text.replace('LTDA . ', 'LTDA. ')
        text = text.replace('SUL /LESTE', 'SUL/LESTE')

        # retokenize
        text = text.replace('/', ' / ')
        text = text.replace('S / A', 'S/A')
        text = text.replace('S / N', 'S/N')
        text = text.replace('S / Nº', 'S/Nº')
        text = text.replace('S / nº', ' S/nº')
        text = text.replace('/SIF', '/ SIF')
        text = text.replace('AV.SEN.', ' AV. SEN. ')
        text = text.replace('NO. :', 'NO.:')
        text = text.replace(' c / o ', ' c/o ')
        text = text.replace(' C / O ', ' C/O ')
        text = text.replace(' A / S. ', ' A/S. ')
        text = text.replace(' LTD.T / A ',' LTD.T/A ')
        text = text.replace(' p / a: ', ' p/a: ')
        text = text.replace("' - '", " ' - ' ")
        text = text.replace('ROTTERDAM.', 'ROTTERDAM .')
        text = text.replace('.Phone:', '. Phone:')
        text = text.replace('VOORBURG.', 'VOORBURG .')
        text = text.replace('Holland.', 'Holland .')
        text = text.replace('EXPEDITIEBEDRIJF.WAALHAVEN', 'EXPEDITIEBEDRIJF. WAALHAVEN')
        text = text.replace("BV'BOBINESTRAAT", "BV 'BOBINESTRAAT")
        text = text.replace('B.V.ABEL', 'B.V. ABEL')
        text = text.replace('.THE NETHERLANDS', '. THE NETHERLANDS')
        text = text.replace('RB.ZOETERMEER.', 'RB. ZOETERMEER.')
        text = text.replace('APPROVAL NUMBER:', ' APPROVAL NUMBER:')
        

        # Fix amp;
        text = text.replace('FLAT Camp ; D', 'FLAT C & D')
        text = text.replace(' amp ; ', ' & ')
        text = text.replace(' amp; ', ' & ')

        # remove duplicate spaces
        text = re.sub(' +', ' ', text)
        return text  
    
class NerRuTokenizer(object):

    def __init__(self):
        pass  

    def tokenize(self, text):
        punct = string.punctuation
        text = text.replace('\t', ' ')
        text = text.replace('\r', ' ')
        text = text.replace('\n', ' ')
        text = text.replace('#13;', '')
        text = text.replace('sif', 'SIF')
        text = text.replace('Sif', 'SIF')

        # find UNICODE chars and transform them
        matches = list(set(re.findall('&#\d{2,4} *;', text)))
        for m in matches:
            text = text.replace(m, html.unescape(m))

        #text = text.replace('&#1054;',html.unescape('&#1054;'))
        # separa a vírgula no final, precedida por qualquer caractere
        text = re.sub(r'(.*?),$', r'\1 ,', text)
        # separa a vírgula entre letras
        text = re.sub(r'(?<=[a-zA-Z]),', r' , ', text)
        # separa a vírgula precedida de ponto
        text = text.replace('.,', '. , ')
        # separa a vírgula sempre que iniciar a palavra
        text = re.sub(r',([a-zA-Z0-9])', r', \1', text)
        # vírgula seguida de espaço
        text = text.replace(', ', ' , ')
        # - 
        text = re.sub(r'(?<!\s)-|-(?!\s)', r' - ', text)
        # /
        text = re.sub(r'(?<=^)/|/(?=\s|$)', r' / ', text)
        text = re.sub(r'/(?=\s|$)', r' / ', text)
        
        # LIMITED.
        text = text.replace('LIMITED', ' LIMITED ')
        text = text.replace('LIMITED.', ' LIMITED .')
        text = text.replace('LIMITED', ' LIMITED ')
        text = text.replace('LTDA', ' LTDA ')
        text = text.replace('Ltda', ' Ltda ')
        text = text.replace('Limited', ' Limited ')
        text = text.replace('COMPANY', ' COMPANY ')
        text = text.replace('Company', ' Company ')
        text = text.replace('GROUP', ' GROUP ')
        # preserve terms
        terms = [
        'No.', 'NO.', 'nO.', 'no.','Nº.', 'NOS.', 'S/N°',
        ' HK', 'HK ', ' H.K.', 'H.K ', ' HK.', 'HK. ',
        'S.A.', 'E-MAIL:', 'e-mail', 'Email:', 'email', 'EMAIL', 'Tel:', 'TEL:', 'TEL.:', 'FAX:','fax', 'Fax:'
        'PLAZA', 'ADDRESS:', 'Add.:', 'ADD.:',
        'ATTN.:', 'ATTN:', 'Attn.:',
        'N.T.', 'NT.',
        'Bldg.', 'Blk.', 'BLDG.', 'bldg.',
        'Rd.', 'RD.', 'ROD.',
        'TRADING:', 'WEBSITE:'
        ]
        for term in terms:
            text = text.replace(term, ' ' + term + ' ')

        
        text = text.replace(' LTD . ', ' LTD. ')
        text = text.replace(' LTDA . ', ' LTDA. ')
        text = text.replace('/FAX', '/ FAX')
        text = text.replace('FAX', ' FAX')
        text = text.replace('.:', '.: ')
        text = text.replace(':', ': ')
        text = text.replace(';', ' ; ')
        

        text = re.sub (r"\(\s*(\d+)\s*\)", r"(\1)", text)
        text = re.sub (r"\(\s*([+-]?\d+)\s*\)", r"(\1)", text)
        text = text.replace('TEL :', 'TEL: ')
        text = text.replace('FAX :', 'FAX: ')
        text = text.replace('EMAIL :', 'EMAIL: ')
        text = text.replace('E - MAIL', 'E-MAIL')
        text = text.replace('e - mail', 'e-mail')
        text = text.replace('E - mail', 'E-mail')
        text = text.replace('MAIL :', 'MAIL: ')
        text = text.replace('PHONE :', 'PHONE: ')
        text = text.replace('ADDRESS :', 'ADDRESS: ')
        text = text.replace('ATTN :', 'ATTN: ')
        text = text.replace(' TERRITORIES.', ' TERRITORIES . ')

        text = text.replace('Tell:', ' Tel: ')
        text = text.replace('HongKong', ' Hong Kong ')
        text = text.replace('Kong.', ' Kong . ')
        text = text.replace('KONG.', ' KONG . ')
        text = text.replace('CENTRAL.', ' CENTRAL . ')
        text = text.replace('STREET-', ' STREET - ')
        text = text.replace('Street-', ' Street - ')
        text = text.replace('WEST-', ' WEST - WEST ')
        text = text.replace('Center.', ' Center . ')
        text = text.replace('CENTRE.', ' CENTRE . ')
        text = text.replace('IND.CENTRE', ' IND. CENTRE ')
        text = text.replace('LOG.CENTER.G/F', 'LOG. CENTER . G/F')
        
        text = re.sub (r"\(\s*([A-Za-z\.]+)\s*\)", r"(\1)", text)
        # remove duplicate spaces
        text = re.sub(' +', ' ', text)
        # separeate dot ending numbers
        text = re.sub(r'(\d+)\.\s*', r'\1 . ', text)
        # HONG KONG
        text = text.replace('HONG', ' HONG ')
        text = text.replace('KONG', ' KONG ')
        # KOWLOON
        text = text.replace('KOWLOON', ' KOWLOON ')
        # ()
        text = text.replace('(', ' (')
        text = text.replace(')', ') ')
        text = text.replace('( ', '(')
        text = text.replace(' )', ')')
        # []
        text = text.replace('[', ' [')
        text = text.replace(']', '] ')
        text = text.replace('[ ', '[')
        text = text.replace(' ]', ']')
        # /
        text = text.replace('/ ', ' / ')
        
        # RUSSIA 
        text = text.replace('PETERSBURG/RUSSIA', ' PETERSBURG / RUSSIA ')
        text = text.replace('KALININGRAD/RUSSIA', ' KALININGRAD / RUSSIA ')
        text = text.replace('/RUSSIAN FEDERATION', ' / RUSSIAN FEDERATION ')
        text = text.replace('RUSSIAN FEDERATION', ' RUSSIAN FEDERATION ')
        text = text.replace('REGION/RUSSIA', ' REGION / RUSSIA ')
        text = text.replace('/RUSSIA', ' / RUSSIA ')
        text = text.replace('PETERSBURG/', ' PETERSBURG / ')
        text = text.replace('ST.PETERSBURG', 'ST. PETERSBURG')
        text = text.replace('RUSSIA.', 'RUSSIA .')
        text = text.replace('NAB.OKTYABRSKAYA', 'NAB. OKTYABRSKAYA')
        text = text.replace('St.Petersburg', 'St. Petersburg')
        text = re.sub(r'([Dd]\.)([0-9]+)', r'\1 \2',text)
        text = re.sub(r'(POM\.)([0-9]+)', r'\1 \2',text)
        text = re.sub(r'(KORP\.)([0-9]+)', r'\1 \2',text)
        text = re.sub(r'(korp\.)([0-9]+)', r'\1 \2',text)
        text = re.sub(r'(KOMN\.)([0-9]+)', r'\1 \2',text)
        text = re.sub(r'(komn\.)([0-9]+)', r'\1 \2',text)
        text = re.sub(r'(OF\.)([0-9]+)', r'\1 \2',text)
        text = re.sub(r'(of\.)([0-9]+)', r'\1 \2',text)
        text = re.sub(r'(ST\.)([0-9]+)', r'\1 \2',text)
        text = re.sub(r'(STR\.)([0-9]+)', r'\1 \2',text)
        text = re.sub(r'(APP\.)([0-9]+)', r'\1 \2',text)
        text = re.sub(r'(H\.)([0-9]+)', r'\1 \2',text)
        text = re.sub(r'(h\.)([0-9]+)', r'\1 \2',text)
        text = re.sub(r'(APT\.)([0-9]+)', r'\1 \2',text)
        text = re.sub(r'(apt\.)([0-9]+)', r'\1 \2',text)
        text = re.sub(r'(SQ\.)([0-9]+)', r'\1 \2',text)
        text = re.sub(r'(R\.)([0-9]+)', r'\1 \2',text)
        text = re.sub(r'(B\.)([0-9]+)', r'\1 \2',text)
        text = re.sub(r'(b\.)([0-9]+)', r'\1 \2',text)
        text = text.replace('LIT.A.', 'LIT. A.')
        text = text.replace('LIT.A', 'LIT. A')
        text = text.replace('LIT.D', 'LIT. D')
        text = text.replace('LIT.V', 'LIT. V')
        text = text.replace('lit.A.', 'lit. A.')
        text = text.replace('VN.TER.G.MUNICIPALNY', 'VN. TER. G. MUNICIPALNY')
        text = text.replace('VN.TER.G.','VN. TER. G.')
        text = text.replace('POM.1N','POM. 1N')
        text = text.replace('pom.1N','pom. 1N')
        text = text.replace('LIT.ZH', 'LIT. ZH')
        text = text.replace('Nab.Oktyabrskaya', 'Nab. Oktyabrskaya')
        text = text.replace('TER.C', 'TER. C')
        text = text.replace('POM.1H', 'POM. 1H')
        text = text.replace('PL.POBEDI', 'PL. POBEDI')
        text = text.replace('UL.PRAVAYA', 'UL. PRAVAYA')
        text = text.replace('bld.Nº', 'bld. Nº')
        text = text.replace('UL.DZERZINSKOGO', 'UL. DZERZINSKOGO')
        text = text.replace('SAINT - PETERSBURG', 'SAINT PETERSBURG')
        text = text.replace('SAINT - PETERSBURG', 'SAINT PETERSBURG')
       
        
        # juntar números 9 . 9 -> 9.9
        text = re.sub(r'(\d+)\s*\.\s*(\d+)',r'\1.\2' , text)
        # juntar números 9 - 9 -> 9-9
        text = re.sub(r'(\d+)\s*\-\s*(\d+)',r'\1.\2' , text)
        # LTDA
        text = text.replace('Ltda . ', 'Ltda. ')
        text = text.replace('LTDA . ', 'LTDA. ')
        text = text.replace('SUL /LESTE', 'SUL/LESTE')

        # Fix amp;
        text = text.replace('FLAT Camp ; D', 'FLAT C & D')
        text = text.replace(' amp ; ', ' & ')
        text = text.replace(' amp; ', ' & ')

        # remove duplicate spaces
        text = re.sub(' +', ' ', text)
        return text  
    
class NerItTokenizer(object):

    def __init__(self):
        pass  

    def tokenize(self, text):
        punct = string.punctuation
        text = text.replace('\t', ' ')
        text = text.replace('\r', ' ')
        text = text.replace('\n', ' ')
        text = text.replace('#13;', '')
        text = text.replace('sif', 'SIF')
        text = text.replace('Sif', 'SIF')
        # separa a vírgula no final, precedida por qualquer caractere
        text = re.sub(r'(.*?),$', r'\1 ,', text)
        # separa a vírgula entre letras
        text = re.sub(r'(?<=[a-zA-Z]),', r' , ', text)
        # separa a vírgula precedida de ponto
        text = text.replace('.,', '. , ')
        # separa a vírgula sempre que iniciar a palavra
        text = re.sub(r',([a-zA-Z0-9])', r', \1', text)
        # vírgula seguida de espaço
        text = text.replace(', ', ' , ')
        # - 
        text = re.sub(r'(?<!\s)-|-(?!\s)', r' - ', text)
        # /
        text = re.sub(r'(?<=^)/|/(?=\s|$)', r' / ', text)
        text = re.sub(r'/(?=\s|$)', r' / ', text)
        
        # LIMITED.
        text = text.replace('LIMITED', ' LIMITED ')
        text = text.replace('LIMITED.', ' LIMITED .')
        text = text.replace('LIMITED', ' LIMITED ')
        text = text.replace('LTDA', ' LTDA ')
        text = text.replace('Ltda', ' Ltda ')
        text = text.replace('Limited', ' Limited ')
        text = text.replace('COMPANY', ' COMPANY ')
        text = text.replace('Company', ' Company ')
        text = text.replace('GROUP', ' GROUP ')
        text = text.replace('S.A.', ' S.A. ')
        
        # preserve terms
        terms = [
        'No.', 'NO.', 'nO.', 'no.','Nº.', 'NOS.', 'S/N°',
        ' HK', 'HK ', ' H.K.', 'H.K ', ' HK.', 'HK. ',
        'S.A.', 'E-MAIL:', 'e-mail', 'Email:', 'email', 'EMAIL', 'Tel:', 'TEL:', 'TEL.:', 'FAX:','fax', 'Fax:'
        'PLAZA', 'ADDRESS:', 'Add.:', 'ADD.:',
        'ATTN.:', 'ATTN:', 'Attn.:',
        'N.T.', 'NT.',
        'Bldg.', 'Blk.', 'BLDG.', 'bldg.',
        'Rd.', 'RD.', 'ROD.',
        'TRADING:', 'WEBSITE:'
        ]

        for term in terms:
            text = text.replace(term, ' ' + term + ' ')

        text = text.replace(' LTD . ', ' LTD. ')
        text = text.replace(' LTDA . ', ' LTDA. ')
        text = text.replace('/FAX', '/ FAX')
        text = text.replace('FAX', ' FAX')
        text = text.replace('.:', '.: ')
        text = text.replace(':', ': ')
        text = text.replace(';', ' ; ')
        

        text = re.sub (r"\(\s*(\d+)\s*\)", r"(\1)", text)
        text = re.sub (r"\(\s*([+-]?\d+)\s*\)", r"(\1)", text)
        text = text.replace('TEL :', 'TEL: ')
        text = text.replace('FAX :', 'FAX: ')
        text = text.replace('EMAIL :', 'EMAIL: ')
        text = text.replace('E - MAIL', 'E-MAIL')
        text = text.replace('e - mail', 'e-mail')
        text = text.replace('E - mail', 'E-mail')
        text = text.replace('MAIL :', 'MAIL: ')
        text = text.replace('PHONE :', 'PHONE: ')
        text = text.replace('ADDRESS :', 'ADDRESS: ')
        text = text.replace('ATTN :', 'ATTN: ')
        text = text.replace(' TERRITORIES.', ' TERRITORIES . ')

        text = text.replace('Tell:', ' Tel: ')
        text = text.replace('HongKong', ' Hong Kong ')
        text = text.replace('Kong.', ' Kong . ')
        text = text.replace('KONG.', ' KONG . ')
        text = text.replace('CENTRAL.', ' CENTRAL . ')
        text = text.replace('STREET-', ' STREET - ')
        text = text.replace('Street-', ' Street - ')
        text = text.replace('WEST-', ' WEST - WEST ')
        text = text.replace('Center.', ' Center . ')
        text = text.replace('CENTRE.', ' CENTRE . ')
        text = text.replace('IND.CENTRE', ' IND. CENTRE ')
        text = text.replace('LOG.CENTER.G/F', 'LOG. CENTER . G/F')
        
       
        # remove duplicate spaces
        text = re.sub(' +', ' ', text)
       
        # HONG KONG
        text = text.replace('HONG', ' HONG ')
        text = text.replace('KONG', ' KONG ')
        # KOWLOON
        text = text.replace('KOWLOON', ' KOWLOON ')
        # ()
        text = text.replace('(', ' (')
        text = text.replace(')', ') ')
        text = text.replace('( ', '(')
        text = text.replace(' )', ')')
        # []
        text = text.replace('[', ' [')
        text = text.replace(']', '] ')
        text = text.replace('[ ', '[')
        text = text.replace(' ]', ']')
        # /
        text = text.replace('/ ', ' / ')
        


        # juntar números 9 . 9 -> 9.9
        text = re.sub(r'(\d+)\s*\.\s*(\d+)',r'\1.\2' , text)
        # juntar números 9 - 9 -> 9-9
        text = re.sub(r'(\d+)\s*\-\s*(\d+)',r'\1.\2' , text)
        # LTDA
        text = text.replace('Ltda . ', 'Ltda. ')
        text = text.replace('LTDA . ', 'LTDA. ')
        text = text.replace('SUL /LESTE', 'SUL/LESTE')

      
       
        

        # retokenize
        text = text.replace('/', ' / ')
        text = text.replace('S / A', 'S/A')
        text = text.replace('S / N', 'S/N')
        text = text.replace('S / Nº', 'S/Nº')
        text = text.replace('S / nº', ' S/nº')
        text = text.replace('/SIF', '/ SIF')
        text = text.replace('AV.SEN.', ' AV. SEN. ')
        
        # Italy
        text = re.sub(r'([0-9]+) / ([A-Z])', r'\1/\2', text)
        text = text.replace('(', ' ( ')
        text = text.replace(')', ' ) ')
        text = text.replace('ITALY.', 'ITALY .')
        text = text.replace('Italy.', 'Italy .')
        text = text.replace('P.NO', 'P. NO')
        
        text = re.sub(r'([a-zA-Z0-9]{6,})(\.)', r'\1 \2', text)
       
        
        # Fix amp;
        text = text.replace('FLAT Camp ; D', 'FLAT C & D')
        text = text.replace(' amp ; ', ' & ')
        text = text.replace(' amp; ', ' & ')

        # remove duplicate spaces
        text = re.sub(' +', ' ', text)
        text = re.sub(' +', ' ', text)
        return text  

class NerEsTokenizer(object):

    def __init__(self):
        pass  

    def tokenize(self, text):
        punct = string.punctuation
        text = text.replace('\t', ' ')
        text = text.replace('\r', ' ')
        text = text.replace('\n', ' ')
        text = text.replace('#13;', '')
        text = text.replace('sif', 'SIF')
        text = text.replace('Sif', 'SIF')
        # separa a vírgula no final, precedida por qualquer caractere
        text = re.sub(r'(.*?),$', r'\1 ,', text)
        # separa a vírgula entre letras
        text = re.sub(r'(?<=[a-zA-Z]),', r' , ', text)
        # separa a vírgula precedida de ponto
        text = text.replace('.,', '. , ')
        # separa a vírgula sempre que iniciar a palavra
        text = re.sub(r',([a-zA-Z0-9])', r', \1', text)
        # vírgula seguida de espaço
        text = text.replace(', ', ' , ')
        # - 
        text = re.sub(r'(?<!\s)-|-(?!\s)', r' - ', text)
        # /
        text = re.sub(r'(?<=^)/|/(?=\s|$)', r' / ', text)
        text = re.sub(r'/(?=\s|$)', r' / ', text)
        
        # LIMITED.
        text = text.replace('LIMITED', ' LIMITED ')
        text = text.replace('LIMITED.', ' LIMITED .')
        text = text.replace('LIMITED', ' LIMITED ')
        text = text.replace('LTDA', ' LTDA ')
        text = text.replace('Ltda', ' Ltda ')
        text = text.replace('Limited', ' Limited ')
        text = text.replace('COMPANY', ' COMPANY ')
        text = text.replace('Company', ' Company ')
        text = text.replace('GROUP', ' GROUP ')
        text = text.replace('S.A.', ' S.A. ')
        
        # preserve terms
        terms = [
        'No.', 'NO.', 'nO.', 'no.','Nº.', 'NOS.', 'S/N°',
        ' HK', 'HK ', ' H.K.', 'H.K ', ' HK.', 'HK. ',
        'S.A.', 'E-MAIL:', 'e-mail', 'Email:', 'email', 'EMAIL', 'Tel:', 'TEL:', 'TEL.:', 'FAX:','fax', 'Fax:'
        'PLAZA', 'ADDRESS:', 'Add.:', 'ADD.:',
        'ATTN.:', 'ATTN:', 'Attn.:',
        'N.T.', 'NT.',
        'Bldg.', 'Blk.', 'BLDG.', 'bldg.',
        'Rd.', 'RD.', 'ROD.',
        'TRADING:', 'WEBSITE:'
        ]

        for term in terms:
            text = text.replace(term, ' ' + term + ' ')

        text = text.replace(' LTD . ', ' LTD. ')
        text = text.replace(' LTDA . ', ' LTDA. ')
        text = text.replace('/FAX', '/ FAX')
        text = text.replace('FAX', ' FAX')
        text = text.replace('.:', '.: ')
        text = text.replace(':', ': ')
        text = text.replace(';', ' ; ')
        text = text.replace('//', ' // ')

        text = re.sub (r"\(\s*(\d+)\s*\)", r"(\1)", text)
        text = re.sub (r"\(\s*([+-]?\d+)\s*\)", r"(\1)", text)
        text = text.replace('TEL :', 'TEL: ')
        text = text.replace('FAX :', 'FAX: ')
        text = text.replace('EMAIL :', 'EMAIL: ')
        text = text.replace('E - MAIL', 'E-MAIL')
        text = text.replace('e - mail', 'e-mail')
        text = text.replace('E - mail', 'E-mail')
        text = text.replace('MAIL :', 'MAIL: ')
        text = text.replace('PHONE :', 'PHONE: ')
        text = text.replace('ADDRESS :', 'ADDRESS: ')
        text = text.replace('ATTN :', 'ATTN: ')
        text = text.replace(' TERRITORIES.', ' TERRITORIES . ')

        text = text.replace('Tell:', ' Tel: ')
        text = text.replace('HongKong', ' Hong Kong ')
        text = text.replace('Kong.', ' Kong . ')
        text = text.replace('KONG.', ' KONG . ')
        text = text.replace('CENTRAL.', ' CENTRAL . ')
        text = text.replace('STREET-', ' STREET - ')
        text = text.replace('Street-', ' Street - ')
        text = text.replace('WEST-', ' WEST - WEST ')
        text = text.replace('Center.', ' Center . ')
        text = text.replace('CENTRE.', ' CENTRE . ')
        text = text.replace('IND.CENTRE', ' IND. CENTRE ')
        text = text.replace('LOG.CENTER.G/F', 'LOG. CENTER . G/F')
        
       
        # remove duplicate spaces
        text = re.sub(' +', ' ', text)
       
        # HONG KONG
        text = text.replace('HONG', ' HONG ')
        text = text.replace('KONG', ' KONG ')
        # KOWLOON
        text = text.replace('KOWLOON', ' KOWLOON ')
        # ()
        text = text.replace('(', ' (')
        text = text.replace(')', ') ')
        text = text.replace('( ', '(')
        text = text.replace(' )', ')')
        # []
        text = text.replace('[', ' [')
        text = text.replace(']', '] ')
        text = text.replace('[ ', '[')
        text = text.replace(' ]', ']')
        # /
        text = text.replace('/ ', ' / ')
        # BRAZIL
        text = text.replace('Brasil.', 'Brasil .')
        text = text.replace('BRASIL.', 'BRASIL .')
        # CHILE
        text = text.replace('Chile.', ' Chile . ')
        text = text.replace('N°', ' N° ')
        text = text.replace('CHILE.', ' CHILE . ')


        # juntar números 9 . 9 -> 9.9
        text = re.sub(r'(\d+)\s*\.\s*(\d+)',r'\1.\2' , text)
        # juntar números 9 - 9 -> 9-9
        text = re.sub(r'(\d+)\s*\-\s*(\d+)',r'\1.\2' , text)
        # LTDA
        text = text.replace('Ltda . ', 'Ltda. ')
        text = text.replace('LTDA . ', 'LTDA. ')
        text = text.replace('SUL /LESTE', 'SUL/LESTE')

      
       
        

        # retokenize
        text = text.replace('/', ' / ')
        text = text.replace('S / A', ' S/A ')
        text = text.replace('S / N', ' S/N ')
        text = text.replace('S / Nº', ' S/Nº ')
        text = text.replace('S / nº', ' S/nº ')
        text = text.replace('/SIF', '/ SIF ')
        text = text.replace('AV.SEN.', ' AV. SEN. ')
        
        
        # Spain
        text = re.sub(' +', ' ', text)
        text = re.sub(' +', ' ', text)
        text = text.replace('S. L.', 'S.L.')
        text = text.replace('C /', 'C/')
        text = text.replace('S.A. U.', 'S.A.U.')
        text = text.replace('ISLAS CANARIAS.', 'ISLAS CANARIAS .')
        text = text.replace('ESPANA.', 'ESPANA .')
        text = text.replace('SPAIN', ' SPAIN ')
        text = text.replace('ESPAÑA', ' ESPAÑA ')
        text = text.replace('ESPANHA', ' ESPANHA ')
        text = text.replace('ISORA.', 'ISORA .')
        text = text.replace('TENERIFE.', 'TENERIFE .')
        text = text.replace('TENERIFE', ' TENERIFE ')
        text = text.replace('ESPAÑA.', 'ESPAÑA .')
        text = text.replace('ADEJE.', 'ADEJE .')
        text = text.replace('ALBAL.', 'ALBAL .')
        text = text.replace('TELDE.', 'TELDE .')
        text = text.replace('ABONA.', 'ABONA .')
        text = text.replace('GORO.', 'GORO .')
        text = text.replace('VIEJO.', 'VIEJO .')
        text = text.replace('ARAFO.', 'ARAFO .')
        text = text.replace('FRISU.', 'FRISU .')
        text = text.replace('MANZANA', ' MANZANA ')
        text = text.replace('AGÜIMES.', 'AGÜIMES .')
        text = text.replace('POL .', 'POL.')
        text = text.replace('IND .', 'IND.')
        text = re.sub(r'([a-zA-Z0-9]{6,})(\.)', r'\1 \2', text)
       
        
        # Fix amp;
        text = text.replace('FLAT Camp ; D', 'FLAT C & D')
        text = text.replace(' amp ; ', ' & ')
        text = text.replace(' amp; ', ' & ')

        # remove duplicate spaces
        text = re.sub(' +', ' ', text)
        return text  
    
class NerDeTokenizer(object):

    def __init__(self):
        pass  

    def tokenize(self, text):
        punct = string.punctuation
        text = text.replace('\t', ' ')
        text = text.replace('\r', ' ')
        text = text.replace('\n', ' ')
        text = text.replace('#13;', '')
        text = text.replace('sif', 'SIF')
        text = text.replace('Sif', 'SIF')
        # separa a vírgula no final, precedida por qualquer caractere
        text = re.sub(r'(.*?),$', r'\1 ,', text)
        # separa a vírgula entre letras
        text = re.sub(r'(?<=[a-zA-Z]),', r' , ', text)
        # separa a vírgula precedida de ponto
        text = text.replace('.,', '. , ')
        # separa a vírgula sempre que iniciar a palavra
        text = re.sub(r',([a-zA-Z0-9])', r', \1', text)
        # vírgula seguida de espaço
        text = text.replace(', ', ' , ')
        # - 
        text = re.sub(r'(?<!\s)-|-(?!\s)', r' - ', text)
        # /
        text = re.sub(r'(?<=^)/|/(?=\s|$)', r' / ', text)
        text = re.sub(r'/(?=\s|$)', r' / ', text)
        
        # LIMITED.
        text = text.replace('LIMITED', ' LIMITED ')
        text = text.replace('LIMITED.', ' LIMITED .')
        text = text.replace('LIMITED', ' LIMITED ')
        text = text.replace('LTDA', ' LTDA ')
        text = text.replace('Ltda', ' Ltda ')
        text = text.replace('Limited', ' Limited ')
        text = text.replace('COMPANY', ' COMPANY ')
        text = text.replace('Company', ' Company ')
        text = text.replace('GROUP', ' GROUP ')
        text = text.replace('S.A.', ' S.A. ')
        
        # preserve terms
        terms = [
        'No.', 'NO.', 'nO.', 'no.','Nº.', 'NOS.', 'S/N°',
        ' HK', 'HK ', ' H.K.', 'H.K ', ' HK.', 'HK. ',
        'S.A.', 'E-MAIL:', 'e-mail', 'Email:', 'email', 'EMAIL', 'Tel:', 'TEL:', 'TEL.:', 'FAX:','fax', 'Fax:'
        'PLAZA', 'ADDRESS:', 'Add.:', 'ADD.:',
        'ATTN.:', 'ATTN:', 'Attn.:',
        'N.T.', 'NT.',
        'Bldg.', 'Blk.', 'BLDG.', 'bldg.',
        'Rd.', 'RD.', 'ROD.',
        'TRADING:', 'WEBSITE:'
        ]

        for term in terms:
            text = text.replace(term, ' ' + term + ' ')

        text = text.replace(' LTD . ', ' LTD. ')
        text = text.replace(' LTDA . ', ' LTDA. ')
        text = text.replace('/FAX', '/ FAX')
        text = text.replace('FAX', ' FAX')
        text = text.replace('.:', '.: ')
        text = text.replace(':', ': ')
        text = text.replace(';', ' ; ')
        

        text = re.sub (r"\(\s*(\d+)\s*\)", r"(\1)", text)
        text = re.sub (r"\(\s*([+-]?\d+)\s*\)", r"(\1)", text)
        text = text.replace('TEL :', 'TEL: ')
        text = text.replace('FAX :', 'FAX: ')
        text = text.replace('EMAIL :', 'EMAIL: ')
        text = text.replace('E - MAIL', 'E-MAIL')
        text = text.replace('e - mail', 'e-mail')
        text = text.replace('E - mail', 'E-mail')
        text = text.replace('MAIL :', 'MAIL: ')
        text = text.replace('PHONE :', 'PHONE: ')
        text = text.replace('ADDRESS :', 'ADDRESS: ')
        text = text.replace('ATTN :', 'ATTN: ')
        text = text.replace(' TERRITORIES.', ' TERRITORIES . ')

        text = text.replace('Tell:', ' Tel: ')
        text = text.replace('HongKong', ' Hong Kong ')
        text = text.replace('Kong.', ' Kong . ')
        text = text.replace('KONG.', ' KONG . ')
        text = text.replace('CENTRAL.', ' CENTRAL . ')
        text = text.replace('STREET-', ' STREET - ')
        text = text.replace('Street-', ' Street - ')
        text = text.replace('WEST-', ' WEST - WEST ')
        text = text.replace('Center.', ' Center . ')
        text = text.replace('CENTRE.', ' CENTRE . ')
        text = text.replace('IND.CENTRE', ' IND. CENTRE ')
        text = text.replace('LOG.CENTER.G/F', 'LOG. CENTER . G/F')
        
       
        # remove duplicate spaces
        text = re.sub(' +', ' ', text)
       
        # HONG KONG
        text = text.replace('HONG', ' HONG ')
        text = text.replace('KONG', ' KONG ')
        # KOWLOON
        text = text.replace('KOWLOON', ' KOWLOON ')
        # ()
        text = text.replace('(', ' (')
        text = text.replace(')', ') ')
        text = text.replace('( ', '(')
        text = text.replace(' )', ')')
        # []
        text = text.replace('[', ' [')
        text = text.replace(']', '] ')
        text = text.replace('[ ', '[')
        text = text.replace(' ]', ']')
        # /
        text = text.replace('/ ', ' / ')
        # BRAZIL
        text = text.replace('Brasil.', 'Brasil .')
        text = text.replace('BRASIL.', 'BRASIL .')
        # CHILE
        text = text.replace('Chile.', ' Chile . ')
        text = text.replace('N°', ' N° ')
        text = text.replace('CHILE.', ' CHILE . ')


        # juntar números 9 . 9 -> 9.9
        text = re.sub(r'(\d+)\s*\.\s*(\d+)',r'\1.\2' , text)
        # juntar números 9 - 9 -> 9-9
        text = re.sub(r'(\d+)\s*\-\s*(\d+)',r'\1.\2' , text)
        # LTDA
        text = text.replace('Ltda . ', 'Ltda. ')
        text = text.replace('LTDA . ', 'LTDA. ')
        text = text.replace('SUL /LESTE', 'SUL/LESTE')

        # retokenize
        text = text.replace('/', ' / ')
        text = text.replace('S / A', 'S/A')
        text = text.replace('S / N', 'S/N')
        text = text.replace('S / Nº', 'S/Nº')
        text = text.replace('S / nº', ' S/nº')
        text = text.replace('/SIF', '/ SIF')
        text = text.replace('AV.SEN.', ' AV. SEN. ')
        
        text = text.replace('str.', ' str. ')
        text = text.replace('Str.', ' Str. ')
        text = text.replace('STR.', ' STR. ')
        text = text.replace('GERMANY', ' GERMANY ')
        text = text.replace('Germany', ' Germany ')
        text = text.replace('/GERMANY', ' GERMANY ')
        text = text.replace('Deutschland', ' Deutschland ')
        text = text.replace('MÜNCHEN', ' MÜNCHEN ')
        text = text.replace('HERBOLZHEIM', ' HERBOLZHEIM ')
        text = re.sub(r'(\d)[.](\d{5}) ', r'\1 . \2 ', text)
        text = re.sub(r'([A-Z])[.](\d{5}) ', r'\1 . \2 ', text)
        text = re.sub(r'([A-Z]{1,2})[ ]{0,1}[\-.](\d{5})', r'\1  \2 ', text)
        text = re.sub(r' [\-](\d{5}) ', r' \1 ', text)
        text = re.sub(r' ([S][Tt][Rr].)(\d) ', r'\1 \2', text)
        
        # Fix amp;
        text = text.replace('FLAT Camp ; D', 'FLAT C & D')
        text = text.replace(' amp ; ', ' & ')
        text = text.replace(' amp; ', ' & ')

        # remove duplicate spaces
        text = re.sub(' +', ' ', text)
        return text  

class NerJoTokenizer(object):

    def __init__(self):
        pass  

    def tokenize(self, text):
        punct = string.punctuation
        text = text.replace('\t', ' ')
        text = text.replace('\r', ' ')
        text = text.replace('\n', ' ')
        text = text.replace('#13;', '')
        text = text.replace('sif', 'SIF')
        text = text.replace('Sif', 'SIF')
         # find UNICODE chars and transform them
        matches = list(set(re.findall('&#\d{2,4} *;', text)))
        for m in matches:
            text = text.replace(m, html.unescape(m))

        # separa a vírgula no final, precedida por qualquer caractere
        text = re.sub(r'(.*?),$', r'\1 ,', text)
        # separa a vírgula entre letras
        text = re.sub(r'(?<=[a-zA-Z]),', r' , ', text)
        # separa a vírgula precedida de ponto
        text = text.replace('.,', '. , ')
        # separa a vírgula sempre que iniciar a palavra
        text = re.sub(r',([a-zA-Z0-9])', r', \1', text)
        # vírgula seguida de espaço
        text = text.replace(', ', ' , ')
        # - 
        text = re.sub(r'(?<!\s)-|-(?!\s)', r' - ', text)
        # /
        text = re.sub(r'(?<=^)/|/(?=\s|$)', r' / ', text)
        text = re.sub(r'/(?=\s|$)', r' / ', text)
        
        # LIMITED.
        text = text.replace('LIMITED', ' LIMITED ')
        text = text.replace('LIMITED.', ' LIMITED .')
        text = text.replace('LIMITED', ' LIMITED ')
        text = text.replace('LTDA', ' LTDA ')
        text = text.replace('Ltda', ' Ltda ')
        text = text.replace('Limited', ' Limited ')
        text = text.replace('COMPANY', ' COMPANY ')
        text = text.replace('Company', ' Company ')
        text = text.replace('GROUP', ' GROUP ')
        text = text.replace('S.A.', ' S.A. ')
        
        # preserve terms
        terms = [
        'No.', 'NO.', 'nO.', 'no.','Nº.', 'NOS.', 'S/N°',
        ' HK', 'HK ', ' H.K.', 'H.K ', ' HK.', 'HK. ',
        'S.A.', 'E-MAIL:', 'e-mail', 'Email:', 'email', 'EMAIL', 'Tel:', 'TEL:', 'TEL.:', 'FAX:','fax', 'Fax:'
        'PLAZA', 'ADDRESS:', 'Add.:', 'ADD.:',
        'ATTN.:', 'ATTN:', 'Attn.:',
        'N.T.', 'NT.',
        'Bldg.', 'Blk.', 'BLDG.', 'bldg.',
        'Rd.', 'RD.', 'ROD.',
        'TRADING:', 'WEBSITE:'
        ]

        for term in terms:
            text = text.replace(term, ' ' + term + ' ')

        text = text.replace(' LTD . ', ' LTD. ')
        text = text.replace(' LTDA . ', ' LTDA. ')
        text = text.replace('/FAX', '/ FAX')
        text = text.replace('FAX', ' FAX')
        text = text.replace('.:', '.: ')
        text = text.replace(':', ': ')
        text = text.replace(';', ' ; ')
        

        text = re.sub (r"\(\s*(\d+)\s*\)", r"(\1)", text)
        text = re.sub (r"\(\s*([+-]?\d+)\s*\)", r"(\1)", text)
        text = text.replace('TEL :', 'TEL: ')
        text = text.replace('FAX :', 'FAX: ')
        text = text.replace('EMAIL :', 'EMAIL: ')
        text = text.replace('E - MAIL', 'E-MAIL')
        text = text.replace('e - mail', 'e-mail')
        text = text.replace('E - mail', 'E-mail')
        text = text.replace('MAIL :', 'MAIL: ')
        text = text.replace('PHONE :', 'PHONE: ')
        text = text.replace('ADDRESS :', 'ADDRESS: ')
        text = text.replace('ATTN :', 'ATTN: ')
        text = text.replace(' TERRITORIES.', ' TERRITORIES . ')

        text = text.replace('Tell:', ' Tel: ')
        text = text.replace('HongKong', ' Hong Kong ')
        text = text.replace('Kong.', ' Kong . ')
        text = text.replace('KONG.', ' KONG . ')
        text = text.replace('CENTRAL.', ' CENTRAL . ')
        text = text.replace('STREET-', ' STREET - ')
        text = text.replace('Street-', ' Street - ')
        text = text.replace('WEST-', ' WEST - WEST ')
        text = text.replace('Center.', ' Center . ')
        text = text.replace('CENTRE.', ' CENTRE . ')
        text = text.replace('IND.CENTRE', ' IND. CENTRE ')
        text = text.replace('LOG.CENTER.G/F', 'LOG. CENTER . G/F')
        
       
        # remove duplicate spaces
        text = re.sub(' +', ' ', text)
       
        # HONG KONG
        text = text.replace('HONG', ' HONG ')
        text = text.replace('KONG', ' KONG ')
        # KOWLOON
        text = text.replace('KOWLOON', ' KOWLOON ')
        # ()
        text = text.replace('(', ' (')
        text = text.replace(')', ') ')
        text = text.replace('( ', '(')
        text = text.replace(' )', ')')
        # []
        text = text.replace('[', ' [')
        text = text.replace(']', '] ')
        text = text.replace('[ ', '[')
        text = text.replace(' ]', ']')
        # /
        text = text.replace('/ ', ' / ')
        


        # juntar números 9 . 9 -> 9.9
        text = re.sub(r'(\d+)\s*\.\s*(\d+)',r'\1.\2' , text)
        # juntar números 9 - 9 -> 9-9
        text = re.sub(r'(\d+)\s*\-\s*(\d+)',r'\1.\2' , text)
        # LTDA
        text = text.replace('Ltda . ', 'Ltda. ')
        text = text.replace('LTDA . ', 'LTDA. ')
        text = text.replace('SUL /LESTE', 'SUL/LESTE')

      
       
        

        # retokenize
        text = text.replace('/', ' / ')
        text = text.replace('S / A', 'S/A')
        text = text.replace('S / N', 'S/N')
        text = text.replace('S / Nº', 'S/Nº')
        text = text.replace('S / nº', ' S/nº')
        text = text.replace('/SIF', '/ SIF')
        text = text.replace('AV.SEN.', ' AV. SEN. ')

        # JORDAN
        text = re.sub(r'([0-9]+) / ([A-Z])', r'\1/\2', text)
        text = text.replace('(', ' ( ')
        text = text.replace(')', ' ) ')
        text = text.replace('JORDAN.', 'JORDAN .')
        text = text.replace('AMMAN', ' AMMAN ')
        text = text.replace('Jordan.', 'Jordan .')
        text = text.replace('CO.FOR', 'CO. FOR')
        text = text.replace('Co.', ' Co. ')
        text = text.replace('1ST.FL', '1ST. FL')
        text = text.replace('P.O.BOX', 'P.O. BOX')
        text = text.replace('.3RD', '. 3RD')
        text = text.replace('AL - ', 'AL-')
        text = text.replace('Al - ', 'Al-')
        text = text.replace('al - ', 'al-')
        text = text.replace('EST - JORDAN', 'EST-JORDAN')
        

        # Fix amp;
        text = text.replace('FLAT Camp ; D', 'FLAT C & D')
        text = text.replace(' amp ; ', ' & ')
        text = text.replace(' amp; ', ' & ')

        # remove duplicate spaces
        text = re.sub(' +', ' ', text)
        text = re.sub(' +', ' ', text)
        return text  

class NerEgTokenizer(object):

    def __init__(self):
        pass  

    def tokenize(self, text):
        punct = string.punctuation
        text = text.replace('\t', ' ')
        text = text.replace('\r', ' ')
        text = text.replace('\n', ' ')
        text = text.replace('#13;', '')
        text = text.replace('sif', 'SIF')
        text = text.replace('Sif', 'SIF')
        
         # find UNICODE chars and transform them
        matches = list(set(re.findall('&#\d{2,4} *;', text)))
        for m in matches:
            text = text.replace(m, html.unescape(m))

        # separa a vírgula no final, precedida por qualquer caractere
        text = re.sub(r'(.*?),$', r'\1 ,', text)
        # separa a vírgula entre letras
        text = re.sub(r'(?<=[a-zA-Z]),', r' , ', text)
        # separa a vírgula precedida de ponto
        text = text.replace('.,', '. , ')
        # separa a vírgula sempre que iniciar a palavra
        text = re.sub(r',([a-zA-Z0-9])', r', \1', text)
        # vírgula seguida de espaço
        text = text.replace(', ', ' , ')
        # - 
        text = re.sub(r'(?<!\s)-|-(?!\s)', r' - ', text)
        # /
        text = re.sub(r'(?<=^)/|/(?=\s|$)', r' / ', text)
        text = re.sub(r'/(?=\s|$)', r' / ', text)
        
        # LIMITED.
        text = text.replace('LIMITED', ' LIMITED ')
        text = text.replace('LIMITED.', ' LIMITED .')
        text = text.replace('LIMITED', ' LIMITED ')
        text = text.replace('LTDA', ' LTDA ')
        text = text.replace('Ltda', ' Ltda ')
        text = text.replace('Limited', ' Limited ')
        text = text.replace('COMPANY', ' COMPANY ')
        text = text.replace('Company', ' Company ')
        text = text.replace('GROUP', ' GROUP ')
        text = text.replace('S.A.', ' S.A. ')
        
        # preserve terms
        terms = [
        'No.', 'NO.', 'nO.', 'no.','Nº.', 'NOS.', 'S/N°',
        ' HK', 'HK ', ' H.K.', 'H.K ', ' HK.', 'HK. ',
        'S.A.', 'E-MAIL:', 'e-mail', 'Email:', 'email', 'EMAIL', 'Tel:', 'TEL:', 'TEL.:', 'FAX:','fax', 'Fax:'
        'PLAZA', 'ADDRESS:', 'Add.:', 'ADD.:',
        'ATTN.:', 'ATTN:', 'Attn.:',
        'N.T.', 'NT.',
        'Bldg.', 'Blk.', 'BLDG.', 'bldg.',
        'Rd.', 'RD.', 'ROD.',
        'TRADING:', 'WEBSITE:'
        ]

        for term in terms:
            text = text.replace(term, ' ' + term + ' ')

        text = text.replace(' LTD . ', ' LTD. ')
        text = text.replace(' LTDA . ', ' LTDA. ')
        text = text.replace('/FAX', '/ FAX')
        text = text.replace('FAX', ' FAX')
        text = text.replace('.:', '.: ')
        text = text.replace(':', ': ')
        text = text.replace(';', ' ; ')
        

        text = re.sub (r"\(\s*(\d+)\s*\)", r"(\1)", text)
        text = re.sub (r"\(\s*([+-]?\d+)\s*\)", r"(\1)", text)
        text = text.replace('TEL :', 'TEL: ')
        text = text.replace('FAX :', 'FAX: ')
        text = text.replace('EMAIL :', 'EMAIL: ')
        text = text.replace('E - MAIL', 'E-MAIL')
        text = text.replace('e - mail', 'e-mail')
        text = text.replace('E - mail', 'E-mail')
        text = text.replace('MAIL :', 'MAIL: ')
        text = text.replace('PHONE :', 'PHONE: ')
        text = text.replace('ADDRESS :', 'ADDRESS: ')
        text = text.replace('ATTN :', 'ATTN: ')
        text = text.replace(' TERRITORIES.', ' TERRITORIES . ')

        text = text.replace('Tell:', ' Tel: ')
        text = text.replace('HongKong', ' Hong Kong ')
        text = text.replace('Kong.', ' Kong . ')
        text = text.replace('KONG.', ' KONG . ')
        text = text.replace('CENTRAL.', ' CENTRAL . ')
        text = text.replace('STREET-', ' STREET - ')
        text = text.replace('Street-', ' Street - ')
        text = text.replace('WEST-', ' WEST - WEST ')
        text = text.replace('Center.', ' Center . ')
        text = text.replace('CENTRE.', ' CENTRE . ')
        text = text.replace('IND.CENTRE', ' IND. CENTRE ')
        text = text.replace('LOG.CENTER.G/F', 'LOG. CENTER . G/F')
        
       
        # remove duplicate spaces
        text = re.sub(' +', ' ', text)
       
        # HONG KONG
        text = text.replace('HONG', ' HONG ')
        text = text.replace('KONG', ' KONG ')
        # KOWLOON
        text = text.replace('KOWLOON', ' KOWLOON ')
        # ()
        text = text.replace('(', ' (')
        text = text.replace(')', ') ')
        text = text.replace('( ', '(')
        text = text.replace(' )', ')')
        # []
        text = text.replace('[', ' [')
        text = text.replace(']', '] ')
        text = text.replace('[ ', '[')
        text = text.replace(' ]', ']')
        # /
        text = text.replace('/ ', ' / ')
        


        # juntar números 9 . 9 -> 9.9
        text = re.sub(r'(\d+)\s*\.\s*(\d+)',r'\1.\2' , text)
        # juntar números 9 - 9 -> 9-9
        text = re.sub(r'(\d+)\s*\-\s*(\d+)',r'\1.\2' , text)
        # LTDA
        text = text.replace('Ltda . ', 'Ltda. ')
        text = text.replace('LTDA . ', 'LTDA. ')
        text = text.replace('SUL /LESTE', 'SUL/LESTE')


        # retokenize
        text = text.replace('/', ' / ')
        text = text.replace('S / A', 'S/A')
        text = text.replace('S / N', 'S/N')
        text = text.replace('S / Nº', 'S/Nº')
        text = text.replace('S / nº', ' S/nº')
        text = text.replace('/SIF', '/ SIF')
        text = text.replace('AV.SEN.', ' AV. SEN. ')
        
        # EGYPT
        text = re.sub(r'([0-9]+) / ([A-Z])', r'\1/\2', text)
        text = text.replace('(', ' ( ')
        text = text.replace(')', ' ) ')
        text = text.replace('APT.', 'APT. ')
        text = text.replace('EGYP.', 'EGYPT .')
        text = text.replace('Egypt.', 'Egypt .')
        text = text.replace('EGYPT.', 'EGYPT .')
        text = text.replace('INDUSTRIES.', 'INDUSTRIES .')
        text = text.replace(' GROUP .NET', 'GROUP.NET')
        text = text.replace('EL - ', 'EL-')
        text = text.replace('El - ', 'El-')
        

        # Fix amp;
        text = text.replace('FLAT Camp ; D', 'FLAT C & D')
        text = text.replace(' amp ; ', ' & ')
        text = text.replace(' amp; ', ' & ')

        # remove duplicate spaces
        text = re.sub(' +', ' ', text)
        text = re.sub(' +', ' ', text)
        return text  
        
class NerClTokenizer(object):
    
    def __init__(self):
        pass  

    def tokenize(self, text):
        punct = string.punctuation
        text = text.replace('\t', ' ')
        text = text.replace('\r', ' ')
        text = text.replace('\n', ' ')
        text = text.replace('#13;', ' ')
        # separa a vírgula no final, precedida por qualquer caractere
        text = re.sub(r'(.*?),$', r'\1 ,', text)
        # separa a vírgula entre letras
        text = re.sub(r'(?<=[a-zA-Z]),', r' , ', text)
        # separa a vírgula precedida de ponto
        text = text.replace('.,', '. , ')
        # separa a vírgula sempre que iniciar a palavra
        text = re.sub(r',([a-zA-Z0-9])', r', \1', text)
        # vírgula seguida de espaço
        text = text.replace(', ', ' , ')
        # - 
        #text = re.sub(r'(?<!\s)-|-(?!\s)', r' - ', text)
        # /
        text = re.sub(r'(?<=^)/|/(?=\s|$)', r' / ', text)
        text = re.sub(r'/(?=\s|$)', r' / ', text)
        
        # LIMITED.
        text = text.replace('LIMITED', ' LIMITED ')
        text = text.replace('LIMITED.', ' LIMITED .')
        text = text.replace('LIMITED', ' LIMITED ')
        text = text.replace('LTDA', ' LTDA ')
        text = text.replace('Ltda', ' Ltda ')
        text = text.replace('Limited', ' Limited ')
        text = text.replace('COMPANY', ' COMPANY ')
        text = text.replace('Company', ' Company ')
        text = text.replace('GROUP', ' GROUP ')
        text = text.replace('S.A.', ' S.A. ')
        
        # preserve terms
        terms = [
        'No.', 'NO.', 'nO.', 'no.','Nº.', 'NOS.', 'S/N°',
        ' HK', 'HK ', ' H.K.', 'H.K ', ' HK.', 'HK. ',
        'S.A.', 'E-MAIL:', 'e-mail', 'Email:', 'email', 'EMAIL', 'Tel:', 'TEL:', 'TEL.:', 'FAX:','fax', 'Fax:'
        'PLAZA', 'ADDRESS:', 'Add.:', 'ADD.:',
        'ATTN.:', 'ATTN:', 'Attn.:',
        'N.T.', 'NT.',
        'Bldg.', 'Blk.', 'BLDG.', 'bldg.',
        'Rd.', 'RD.', 'ROD.',
        'TRADING:', 'WEBSITE:'
        ]

        for term in terms:
            text = text.replace(term, ' ' + term + ' ')

        text = text.replace(' LTD . ', ' LTD. ')
        text = text.replace(' LTDA . ', ' LTDA. ')
        text = text.replace('/FAX', '/ FAX')
        text = text.replace('FAX', ' FAX')
        text = text.replace('.:', '.: ')
        text = text.replace(':', ': ')
        text = text.replace(';', ' ; ')
        

        text = re.sub (r"\(\s*(\d+)\s*\)", r"(\1)", text)
        text = re.sub (r"\(\s*([+-]?\d+)\s*\)", r"(\1)", text)
        text = text.replace('TEL :', 'TEL: ')
        text = text.replace('FAX :', 'FAX: ')
        text = text.replace('EMAIL :', 'EMAIL: ')
        text = text.replace('E - MAIL', 'E-MAIL')
        text = text.replace('e - mail', 'e-mail')
        text = text.replace('E - mail', 'E-mail')
        text = text.replace('MAIL :', 'MAIL: ')
        text = text.replace('PHONE :', 'PHONE: ')
        text = text.replace('ADDRESS :', 'ADDRESS: ')
        text = text.replace('ATTN :', 'ATTN: ')
        text = text.replace(' TERRITORIES.', ' TERRITORIES . ')

        text = text.replace('Tell:', ' Tel: ')
        text = text.replace('HongKong', ' Hong Kong ')
        text = text.replace('Kong.', ' Kong . ')
        text = text.replace('KONG.', ' KONG . ')
        text = text.replace('CENTRAL.', ' CENTRAL . ')
        text = text.replace('STREET-', ' STREET - ')
        text = text.replace('Street-', ' Street - ')
        text = text.replace('WEST-', ' WEST - WEST ')
        text = text.replace('Center.', ' Center . ')
        text = text.replace('CENTRE.', ' CENTRE . ')
        text = text.replace('IND.CENTRE', ' IND. CENTRE ')
        text = text.replace('LOG.CENTER.G/F', 'LOG. CENTER . G/F')
        
       
        # remove duplicate spaces
        text = re.sub(' +', ' ', text)
       
        # HONG KONG
        text = text.replace('HONG', ' HONG ')
        text = text.replace('KONG', ' KONG ')
        # KOWLOON
        text = text.replace('KOWLOON', ' KOWLOON ')
        # ()
        text = text.replace('(', ' (')
        text = text.replace(')', ') ')
        text = text.replace('( ', '(')
        text = text.replace(' )', ')')
        # []
        text = text.replace('[', ' [')
        text = text.replace(']', '] ')
        text = text.replace('[ ', '[')
        text = text.replace(' ]', ']')
        # /
        text = text.replace('/ ', ' / ')
        # BRAZIL
        text = text.replace('Brasil.', 'Brasil .')
        text = text.replace('BRASIL.', 'BRASIL .')
        # CHILE
        text = text.replace('Chile.', ' Chile . ')
        text = text.replace('N°', ' N° ')
        text = text.replace('CHILE.', ' CHILE . ')


        # juntar números 9 . 9 -> 9.9
        text = re.sub(r'(\d+)\s*\.\s*(\d+)',r'\1.\2' , text)
        # juntar números 9 - 9 -> 9-9
        text = re.sub(r'(\d+)\s*\-\s*(\d+)',r'\1.\2' , text)
        # LTDA
        text = text.replace('Ltda . ', 'Ltda. ')
        text = text.replace('LTDA . ', 'LTDA. ')
        text = text.replace('SUL /LESTE', 'SUL/LESTE')

        # retokenize
        text = text.replace('/', ' / ')
        text = text.replace('S / A', 'S/A')
        text = text.replace('S / N', 'S/N')
        text = text.replace('S / Nº', 'S/Nº')
        text = text.replace('S / nº', ' S/nº')
        text = text.replace('/SIF', '/ SIF')
        text = text.replace('AV.SEN.', ' AV. SEN. ')
        


        # remove duplicate spaces
        text = re.sub(' +', ' ', text)
        return text  
       
class NerKrTokenizer(object):

    def __init__(self):
        pass  

    def tokenize(self, text):
        punct = string.punctuation
        text = text.replace('\t', ' ')
        text = text.replace('\r', ' ')
        text = text.replace('\n', ' ')
        text = text.replace('#13;', ' ')
        # separa a vírgula no final, precedida por qualquer caractere
        text = re.sub(r'(.*?),$', r'\1 ,', text)
        # separa a vírgula entre letras
        text = re.sub(r'(?<=[a-zA-Z]),', r' , ', text)
        # separa a vírgula precedida de ponto
        text = text.replace('.,', '. , ')
        # separa a vírgula sempre que iniciar a palavra
        text = re.sub(r',([a-zA-Z0-9])', r', \1', text)
        # vírgula seguida de espaço
        text = text.replace(', ', ' , ')
        # - 
        text = re.sub(r'(?<!\s)-|-(?!\s)', r' - ', text)
        # /
        text = re.sub(r'(?<=^)/|/(?=\s|$)', r' / ', text)
        text = re.sub(r'/(?=\s|$)', r' / ', text)
        
        # LIMITED.
        text = text.replace('LIMITED', ' LIMITED ')
        text = text.replace('LIMITED.', ' LIMITED .')
        text = text.replace('LIMITED', ' LIMITED ')
        text = text.replace('LTDA', ' LTDA ')
        text = text.replace('Ltda', ' Ltda ')
        text = text.replace('Limited', ' Limited ')
        text = text.replace('COMPANY', ' COMPANY ')
        text = text.replace('Company', ' Company ')
        text = text.replace('GROUP', ' GROUP ')
        text = text.replace('S.A.', ' S.A. ')
        
        # preserve terms
        terms = [
        'No.', 'NO.', 'nO.', 'no.','Nº.', 'NOS.', 'S/N°',
        ' HK', 'HK ', ' H.K.', 'H.K ', ' HK.', 'HK. ',
        'S.A.', 'E-MAIL:', 'e-mail', 'Email:', 'email', 'EMAIL', 'Tel:', 'TEL:', 'TEL.:', 'FAX:','fax', 'Fax:'
        'PLAZA', 'ADDRESS:', 'Add.:', 'ADD.:',
        'ATTN.:', 'ATTN:', 'Attn.:',
        'N.T.', 'NT.',
        'Bldg.', 'Blk.', 'BLDG.', 'bldg.',
        'Rd.', 'RD.', 'ROD.',
        'TRADING:', 'WEBSITE:'
        ]

        for term in terms:
            text = text.replace(term, ' ' + term + ' ')

        text = text.replace(' LTD . ', ' LTD. ')
        text = text.replace(' LTDA . ', ' LTDA. ')
        text = text.replace('/FAX', '/ FAX')
        text = text.replace('FAX', ' FAX')
        text = text.replace('.:', '.: ')
        text = text.replace(':', ': ')
        text = text.replace(';', ' ; ')
        

        text = re.sub (r"\(\s*(\d+)\s*\)", r"(\1)", text)
        text = re.sub (r"\(\s*([+-]?\d+)\s*\)", r"(\1)", text)
        text = text.replace('TEL :', 'TEL: ')
        text = text.replace('FAX :', 'FAX: ')
        text = text.replace('EMAIL :', 'EMAIL: ')
        text = text.replace('E - MAIL', 'E-MAIL')
        text = text.replace('e - mail', 'e-mail')
        text = text.replace('E - mail', 'E-mail')
        text = text.replace('E - mark', 'E-mark')
        text = text.replace('E - MARK', 'E-MARK')
        text = text.replace('S - FOOD', 'S-FOOD')
        text = text.replace('MAIL :', 'MAIL: ')
        text = text.replace('PHONE :', 'PHONE: ')
        text = text.replace('ADDRESS :', 'ADDRESS: ')
        text = text.replace('ATTN :', 'ATTN: ')
        text = text.replace(' TERRITORIES.', ' TERRITORIES . ')

        text = text.replace('Tell:', ' Tel: ')
        text = text.replace('HongKong', ' Hong Kong ')
        text = text.replace('Kong.', ' Kong . ')
        text = text.replace('KONG.', ' KONG . ')
        text = text.replace('CENTRAL.', ' CENTRAL . ')
        text = text.replace('STREET-', ' STREET - ')
        text = text.replace('Street-', ' Street - ')
        text = text.replace('WEST-', ' WEST - WEST ')
        text = text.replace('Center.', ' Center . ')
        text = text.replace('CENTRE.', ' CENTRE . ')
        text = text.replace('IND.CENTRE', ' IND. CENTRE ')
        text = text.replace('LOG.CENTER.G/F', 'LOG. CENTER . G/F')
        
       
        # remove duplicate spaces
        text = re.sub(' +', ' ', text)
       
        # HONG KONG
        text = text.replace('HONG', ' HONG ')
        text = text.replace('KONG', ' KONG ')
        # KOWLOON
        text = text.replace('KOWLOON', ' KOWLOON ')
        # ()
        text = text.replace('(', ' (')
        text = text.replace(')', ') ')
        text = text.replace('( ', '(')
        text = text.replace(' )', ')')
        # []
        text = text.replace('[', ' [')
        text = text.replace(']', '] ')
        text = text.replace('[ ', '[')
        text = text.replace(' ]', ']')
        # /
        text = text.replace('/ ', ' / ')
        # BRAZIL
        text = text.replace('Brasil.', 'Brasil .')
        text = text.replace('BRASIL.', 'BRASIL .')
        # CHILE
        text = text.replace('Chile.', ' Chile . ')
        text = text.replace('N°', ' N° ')
        text = text.replace('CHILE.', ' CHILE . ')


        # juntar números 9 . 9 -> 9.9
        text = re.sub(r'(\d+)\s*\.\s*(\d+)',r'\1.\2' , text)
        # juntar números 9 - 9 -> 9-9
        text = re.sub(r'(\d+)\s*\-\s*(\d+)',r'\1.\2' , text)
        # LTDA
        text = text.replace('Ltda . ', 'Ltda. ')
        text = text.replace('LTDA . ', 'LTDA. ')
        text = text.replace('SUL /LESTE', 'SUL/LESTE')

        # retokenize
        text = text.replace('/', ' / ')
        text = text.replace(' - ','-')
        text = text.replace('S / A', 'S/A')
        text = text.replace('S / N', 'S/N')
        text = text.replace('S / Nº', 'S/Nº')
        text = text.replace('S / nº', ' S/nº')
        text = text.replace('/SIF', '/ SIF')
        text = text.replace('AV.SEN.', ' AV. SEN. ')
        


        # remove duplicate spaces
        text = re.sub(' +', ' ', text)
        return text  
    