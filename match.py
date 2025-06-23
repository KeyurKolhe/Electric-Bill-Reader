from pattern import patterns
from datetime import datetime

def extract_data(text):
    extracted_data = {}


    for key, pattern in patterns.items():
        match = pattern.findall(text)
        extracted_data[key] = match[0] if match else None
        
    if extracted_data['Due_Date']:
        extracted_data['Due_Date'] = datetime.strptime(extracted_data['Due_Date'], '%d-%b-%y')

    if extracted_data['Bill']:
        extracted_data['Bill'] = float(extracted_data['Bill'].replace(',', ''))

    if extracted_data['Year'] and extracted_data['ConsumerId'] and extracted_data['BillNo']:
        extracted_data['BillNo'] = int(extracted_data['BillNo'])
        extracted_data['Year'] = int(extracted_data['Year'])
        extracted_data['ConsumerId'] = int(extracted_data['ConsumerId'])
        

    return extracted_data
