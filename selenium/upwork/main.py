import csv
import json
import requests
from bs4 import BeautifulSoup

headers = {
    'Accept': '*/*',
    'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8,bn;q=0.7,fr;q=0.6,mt;q=0.5',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    # Requests sorts cookies= alphabetically
    # 'Cookie': 'arp_scroll_position=333.3333435058594; ci_session=be7hkeq5tdongip3svvt2df33e5grmsq; csrf_cookie_name=b5456f23e6b1843bf4dc06c2f4ae9229',
    'Origin': 'https://ngodarpan.gov.in',
    # 'Referer': 'https://ngodarpan.gov.in/index.php/home/statewise_ngo/175/35/1',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

base_url = "https://ngodarpan.gov.in/index.php/home/statewise"

def get_record(item):
    parse_id = item['onclick']
    id = ''
    for d in parse_id:
        if d.isdigit():
            id = id + d
    token_res = requests.get('https://ngodarpan.gov.in/index.php/ajaxcontroller/get_csrf', headers=headers)
    text = token_res.json()
    token = text['csrf_token']
    cookies = {
        'arp_scroll_position': '333.3333435058594',
        'ci_session': 'be7hkeq5tdongip3svvt2df33e5grmsq',
        'csrf_cookie_name': token,
    }
    data = {
        'id': id,
        'csrf_test_name': token,
    }   
    info_res = requests.post('https://ngodarpan.gov.in/index.php/ajaxcontroller/show_ngo_info', cookies=cookies, headers=headers, data=data)
    data = info_res.text
    parse_json = json.loads(data)
    ngo_name = parse_json['infor']['0']['ngo_name']
    reg_no_city_add = parse_json['registeration_info'][0]['nr_regNo'] + ', ' + parse_json['registeration_info'][0]['nr_city'] + ', ' + parse_json['registeration_info'][0]['StateName']
    reg_address = parse_json['registeration_info'][0]['nr_add']
    sector = parse_json['infor']['issues_working_db']
    unique_id = parse_json['infor']['0']['UniqueID']
    registered_with = parse_json['registeration_info'][0]['reg_name']
    type_of_ngo = parse_json['registeration_info'][0]['TypeDescription']
    reg_no = parse_json['registeration_info'][0]['nr_regNo']
    if parse_json['infor']['0']['reg_updDocId']:
        reg_cert = 'Available'
    else:
        reg_cert = 'N/A'
    if parse_json['infor']['0']['pan_updDocId']:
        pan_card ='Available'
    else:
        pan_card = 'N/A'
    act_name = parse_json['registeration_info'][0]['nr_actName']
    reg_city = parse_json['registeration_info'][0]['nr_city']
    reg_state = parse_json['registeration_info'][0]['StateName']
    reg_date = parse_json['registeration_info'][0]['ngo_reg_date']
    mem_name = []
    mem_num = []
    mem_email = []
    mem_desig = []
    for member in parse_json['member_info']:
        mem_name.append(member['FName'])
        mem_num.append(member['MobileNo'])
        mem_email.append(member['EmailId'])
        mem_desig.append(member['DesigName'])
    if parse_json['registeration_info'][0]['nr_isFcra']=='N':
        nr_isFcra = 'Not available'
    else:
        nr_isFcra = 'Available'
    if parse_json['registeration_info'][0]['fcrano'] == '':
        fcrano = 'Not available'
    else:
        fcrano = parse_json['registeration_info'][0]['fcrano']
    address = parse_json['registeration_info'][0]['nr_add']
    city = parse_json['registeration_info'][0]['nr_city']
    state = parse_json['registeration_info'][0]['StateName']
    mobile_no = parse_json['infor']['0']['Mobile']
    telephone = parse_json['infor']['0']['Off_phone1']
    website = parse_json['infor']['0']['ngo_url']
    email = parse_json['infor']['0']['Email']
    result = (ngo_name, reg_no_city_add, reg_address, sector, unique_id, registered_with, type_of_ngo, reg_no,
    reg_cert, pan_card, act_name,reg_city, reg_state, reg_date, mem_name, mem_num, mem_email, mem_desig,
    nr_isFcra, fcrano, address, city, state, telephone, mobile_no, website, email)
    return result

def parse_list(link):
    records = []
    res_ngo_list = requests.get(link, headers=headers)
    soup_ngo_list = BeautifulSoup(res_ngo_list.text, 'html.parser')
    ngo_list_td = soup_ngo_list.find_all('a', {'href':'javascript:void(0)', 'onclick':True, 'class':False})
    for item in ngo_list_td:
        try:
            record = get_record(item)
            records.append(record)
            with open('results.csv', 'a+', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerows(records)
            records.clear()
        except:
            continue
         
def parse_pagination(link): 
    print('Collecting: ', link)
    parse_list(link)
    for i in range(2, 50000):
        try:
            response = requests.get(link, headers=headers) 
            soup = BeautifulSoup(response.text, 'html.parser')
            next_page = soup.find('a', {'data-ci-pagination-page':True, 'rel':'next'})
            link = next_page['href']
            print('Collecting: ', link)
            parse_list(str(link))
        except:
            break

def main():
    with open('results.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Name of VO/NGO', 'Registration No.,City & State', 'Address', 'Sectors working in', 'Unique ID of VO/ NGO',
            'Registered With', 'Type of NGO', 'Registration No', 'Copy of Registration Certificate', 'Copy of Pan Card',
            'Act name', 'City of registration', 'State of registration', 'Date of registration',
            'Name', 'Mobile Number', 'Email ID', 'Designation',
            'FCRA available', 'FCRA registraion no.',
            'Address', 'City', 'State', 'Telephone', 'Mobile No','Website URL', 'E-mail'])
    print('CSV file created!')
    response = requests.get(base_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    statewise = soup.find_all('a', class_="bluelink11px")
    x = 1
    for item in statewise:
        print('Statewise: ', x)
        parse_pagination(item['href'])   
        x += 1     


main()

