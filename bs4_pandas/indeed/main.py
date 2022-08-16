import csv
from datetime import datetime
import requests
from bs4 import BeautifulSoup

def get_url(postion, location):
    template = "http://www.indeed.com/jobs?q={}&l={}"
    url = template.format(postion, location)
    return url

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36'
}
base_url = "http://www.indeed.com"
url = get_url('Software Engineer', 'Silicon Valley, CA')

response = requests.get(url, headers=headers)

soup = BeautifulSoup(response.text, 'html.parser')
cards = soup.find_all('div', class_="job_seen_beacon")

def get_record(card):
    job_title = card.h2.a.span
    job_title = job_title['title']

    job_url = card.h2.a
    job_url = base_url+job_url['href']

    try:
        company_name = card.find('a', {"data-tn-element": 'companyName'}).text.strip()
    except AttributeError:
        company_name = 'N/A'
    company_location = card.find('div', class_="companyLocation").text.strip()

    job_summury = card.find('div', class_="job-snippet").text

    post_date = card.find('span', class_="date").text

    try:
        salary = card.find('svg', {'aria-label':'Salary'}).text
    except:
        salary = 'N/A'
    record = (job_title, job_url, company_name, company_location, job_summury, post_date, salary)
    return record


records = []

for card in cards:
    record = get_record(card)
    records.append(record)
    print(record)


