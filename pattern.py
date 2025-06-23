import re

name_pattern = re.compile(r'\bSHRI\b\s{1}([a-zA-Z]+\s{1}+[a-zA-Z]+\s{1}+[a-zA-Z]+)')
address_pattern = re.compile(r'\bSHRI\b\s{1}+[a-zA-Z]*+\s{1}+[a-zA-Z]*+\s{1}+[a-zA-Z]*+\n(.+)')
phone_pattern = re.compile(r'(?:इमेल|Email):\n{2}(\d{2}\*{6}\d{2})')
billno_pattern = re.compile(r'\bBILL NO.\(GGN\)\:\s\b(.+)\n')
month_pat = re.compile(r'(?:माहे|Supply\sFor):\s([A-Z]{3})')
yr_pat = re.compile(r'[A-Z]{3}\-([0-9]{4})')
cons_pat = re.compile(r'(\d{12})\n\bSHRI\b')
due_pat = re.compile(r'(?:Rs|\x00)\:\n{2}(\d{2}\-[A-Z]{3}\-\d{2})\n')
#bill_pat = re.compile(r'(?:Rs|\x00)\:\n{2}\d{2}\-[A-Z]{3}\-\d{2}\n(.+)')
bill_pat = re.compile(r'\n*([\d,]+\.\d{2})\n*DPC')

patterns = {
    'Name': name_pattern,
    'Address': address_pattern,
    'Phone': phone_pattern,
    'BillNo': billno_pattern,
    'Month': month_pat,
    'Year': yr_pat,
    'ConsumerId': cons_pat,
    'Due_Date': due_pat,
    'Bill': bill_pat
}   