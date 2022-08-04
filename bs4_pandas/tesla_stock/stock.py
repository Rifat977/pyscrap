import pandas as pd
import requests

headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36'}

res = requests.get('https://finviz.com/quote.ashx?t=TSLA', headers=headers)

pd_table = pd.read_html(res.text, attrs={'class':'snapshot-table2'})

pd_table[0].to_csv('tesla.csv', index=False, header=False)