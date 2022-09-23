# We’ll extract the job title, company hiring, location,
# and the link to the job listing using Requests and Beautiful Soup
# and export the data to a CSV file

# This info is public, so we don't violate rules

import csv
import random
import time
import requests
from bs4 import BeautifulSoup
import webbrowser

# link with preferred parameters
# https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Data%20Scientist&location=Israel&locationId=&geoId=101620260&f_TPR=r86400&f_E=1,2&position=1&pageNum=0&start=0

headers = {
    'accept': '*/*',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
}


def get_links_to_jobs(headers):
    for i in range(0, 125, 25):
        url = f'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Data%20Scientist' \
              f'&location=Israel&locationId=&geoId=101620260&f_TPR=r86400&f_E=1,2&position=1&pageNum=0&start={i}'
        resp = requests.get(url, headers=headers)
        soup = BeautifulSoup(resp.content, 'lxml')

        if len(soup.text):
            all_a = soup.find_all('a', class_='base-card__full-link absolute top-0 right-0 bottom-0 left-0 p-0 z-[2]')
            with open('links_to_jobs.txt', 'a') as file:
                [print(link.get('href'), file=file) for link in all_a]

        else:
            print('All links saved to "links_to_jobs.txt" file')
            break


# get_links_to_jobs(headers)
#
with open('new_jobs.csv', 'a', newline='') as output_file:
    writer = csv.writer(output_file)
    writer.writerow(['Job Title',
                     'Company',
                     'Location',
                     'Seniority Level',
                     'Employment Type',
                     'Apply Link'])


with open('new_jobs.csv', 'a', newline='') as output_file, open('links_to_jobs.txt', 'r') as input_file:
    writer = csv.writer(output_file)

    for line in input_file:
        time.sleep(random.randint(2,5))
        line = line.replace('il', 'www').strip()
        print(f'parsing {line}')
        resp = requests.get(line, headers=headers)
        soup = BeautifulSoup(resp.content, 'lxml')
        job_title = soup.find('h1').text.strip()
        company = soup.find('span', class_='topcard__flavor').find('a').text.strip()
        location = soup.find('span', class_='topcard__flavor topcard__flavor--bullet').text.strip()
        location = location.encode('cp850', 'replace').decode()
        location = ''.join([i for i in location if i != '?'])
        try:
            apply = soup.find('a', class_='apply-button apply-button--link top-card-layout__cta mt-2 ml-1.5 h-auto babybear:flex-auto top-card-layout__cta--primary btn-md btn-primary').get('href')
        except:
            apply = 'Easy Apply on LinkedIn'
        job_criterias = soup.find_all('span', class_='description__job-criteria-text description__job-criteria-text--criteria')
        criterias = [criteria.text.strip() for criteria in job_criterias]
        try:
            seniority_level = criterias[0]
        except:
            seniority_level = "Unknown"

        try:
            employment_type = criterias[1]
        except:
            employment_type = "Unknown"

        writer.writerow([job_title, company, location, seniority_level, employment_type, apply])





# import webbrowser
# chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'
# webbrowser.get(chrome_path).open(apply, new=2)

# or

# webbrowser.open_new_tab("http://www.google.com")



