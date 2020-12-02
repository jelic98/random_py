import re
import requests
import pandas as pd
from bs4 import BeautifulSoup

TSV = 'dpf.tsv'
URL = 'https://www.penzijskifond.rs/generali_basic/vrednost_investicione_jedinice.1157.html'
SEL = '#my-page > div.contentWrap > section > div > div > div.sideBar.col-lg-3.col-md-4 > div:nth-child(2) > div > div.chartValue > div > p'
PAY, UNI = 'Neto uplata', 'Broj IJ'

def atof(x):
    return float(re.sub(',', '.', re.sub('\.', '', x)))

df = pd.read_csv(TSV, sep='\t')
df[PAY] = df[PAY].apply(lambda x: atof(x))
df[UNI] = df[UNI].apply(lambda x: atof(x))
pay = df[PAY].sum()
uni = df[UNI].sum()

bs = BeautifulSoup(requests.get(URL).content, 'html.parser')
curr = atof(bs.select(SEL)[0].text.split(' ')[0].strip())

acc = curr * uni
irv = acc - pay
irp = irv / pay

print("{:<20s}{:>15.2f}".format("Vrednost IJ", curr))
print("{:<20s}{:>15.2f}".format("Ukupno IJ", uni))
print("{:<20s}{:>15.2f}".format("Akumulirano RSD", acc))
print("{:<20s}{:>15.2f}".format("Uplaceno RSD", pay))
print("{:<20s}{:>15.2f}".format("Prinos RSD", irv))
print("{:<20s}{:>15.2f}".format("Stopa prinosa", irp))
