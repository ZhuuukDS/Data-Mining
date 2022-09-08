'''
I’d like to scrape Malls.com (USA only) to extract a list of shopping centers and some basic information:
 - location name
 - address
 - contact information
 - stores within the shopping center
 - management and developer names
 - last updated date/time
 - website
 - description
 - open date

Deliverable: list in CSV form. Each row should be a location, and each column should be one of the attributes listed above.
'''

# importing necessary libraries
import requests  # library for requesting specific information from web-sites (send https requests and get html page)
from bs4 import BeautifulSoup  # main library for scraping (search elements in html code)
import re
import csv

# create a csv file with column names in the first line
# according to the task, columns are the attributes that we need to parse
with open('result.csv', 'w', newline='') as output:
    writer = csv.writer(output)
    writer.writerow(['location name',
                     'address',
                     'square footage',
                     'contact information',
                     'website',
                     'open date',
                     'management',
                     'developer',
                     'List of stores'])


# masking request headings
headers = {
    'accept': '*/*',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
}


def get_data():
    # save all links from all pages into local file links.txt
    for i in range(1, 45):
        url = f'https://www.malls.com/malls/?PAGEN_1={i}&regions=&countries=40&cities=&_=1662488824344&AJAX_PAGE=Y'
        page = requests.get(url, headers=headers)

        with open('liks.txt', 'a') as links_file:
            soup = BeautifulSoup(page.text, 'lxml')
            malls = soup.find_all('div', class_=re.compile('row loading-item size'))
            for mall in malls:
                link = mall.find('div', class_='big').find('a').get('href')
                links_file.writelines(f'https://www.malls.com{link}\n')

    # open file and iterate the links
    count = 0
    with open('liks.txt', 'r') as links_file:
        for link in links_file:
            mall_page = requests.get(link, headers=headers)
            soup = BeautifulSoup(mall_page.text, 'lxml')

            # create a dict with all required attributes.
            # define attributes to unknown (except 'location name')
            info_dict = {'location name': soup.find('h1', class_='title big').text.strip(), 'address': 'No info',
                         'trade area': 'No info', 'opening date': 'No info', 'phone': 'No info', 'website': 'No info',
                         'management': 'No info', 'developer': 'No info', 'list of stores': 'No info'}

            # if information can be retrieved, the dict updated by the key
            # if not, we pass and keep attribute unknown for this particular mall

            # get address
            try:
                address = soup.find('div', class_='row contacts v1') \
                    .find('div', class_='columns small-12 medium-6 half r') \
                    .find('div', class_='r').text.strip()
                info_dict['address'] = address
            except:
                pass

            # get opening data, trade area
            try:
                information = soup.find('div', class_='small grey').find_next().find_all('div', class_='r')
                for info in information:
                    info_dict[info.find_previous().text.strip()[:-1].lower()] = info.text.strip().lower()
            except:
                pass

            # get phone, website
            try:
                business_contacts = soup.find('div', class_='info').find_all('div', class_='small')
                for info in business_contacts:
                    info_dict[info.text.strip()[:-1].lower()] = info.find_next().text.strip().lower()
            except:
                pass

            # get management, developer
            try:
                pro_information = soup.find('div', class_='row contacts v2') \
                    .find('div', class_='columns small-12 medium-6 half r') \
                    .find('ul', class_='info-list').find_all('li')
                for pro_info in pro_information:
                    pro_list = pro_info.text.strip().lower().split('\n\n')
                    info_dict[pro_list[0][:-1]] = pro_list[1]
            except:
                pass

            # get list of stores
            try:
                stores = soup.find('div', class_='row shops').find_all('a')
                list_of_stores = [store.text for store in stores]
                info_dict['list of stores'] = ', '.join(list_of_stores)

            except:
                pass

            with open('result.csv', 'a', newline='') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow((info_dict['location name'],
                                 info_dict['address'],
                                 info_dict['trade area'],
                                 info_dict['phone'],
                                 info_dict['website'],
                                 info_dict['opening date'],
                                 info_dict['management'],
                                 info_dict['developer'],
                                 info_dict['list of stores']))
            count += 1
            print(f'Line {count} saved in result.csv file')

        print(f'->>>> all {count} lines have been successfully saved')


def main():
    get_data()


if __name__ == '__main__':
    main()
