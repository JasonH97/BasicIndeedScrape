import re

def normalize(s):
    salary = re.sub("\$|,|from |up to ","",s.strip().lower())
    if 'hour' in salary:
        salary = round(float(re.search('^[1-9]\d*(\.\d{2})?',salary).group())*2080)
    elif 'day' in salary:
        salary = int(re.search('^[1-9]\d*',salary).group())*260
    elif 'week' in salary:
        salary = int(re.search('^[1-9]\d*',salary).group())*52
    elif 'month' in salary:
        salary = int(re.search('^[1-9]\d*',salary).group())*12
    elif 'year' in salary:
        salary = int(re.search('^[1-9]\d+',salary).group())
    else:
        pass
    return salary


"""
KNOWN PATTERNS

$A a day
$A - $B a day
$A - $B a week
$A - $B a year
$A - $B an hour
$A a month
$A a year
From $A a year
up to $A a month
"""
