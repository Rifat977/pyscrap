import requests
import json
import pandas as pd

url = "https://api.afl.com.au/statspro/playersStats/seasons/CD_S2022014?includeBenchmarks=false"

payload={}
headers = {
  'x-media-mis-token': 'da04eb80e0cc37b495d88bf116f18e98',
  'Referer': 'https://www.afl.com.au/',
  'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36',
  'Cookie': 'JSESSIONID=03FB146CEB23EE4C0ABBB20C9A0C2111'
}

response = requests.get(url, headers=headers, data=payload)

playerdata = response.json()

p_info = pd.json_normalize(playerdata['players'])

p_info.to_csv('player_data.csv', index=False)