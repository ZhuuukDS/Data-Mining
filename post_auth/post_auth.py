from requests import Session
from bs4 import BeautifulSoup

'''
This script shows how to create path authorization requests.
It is needed when we need to parse the website with 'login/password'

This is based on the training website 'http://quotes.toscrape.com/'
'''

#  create headers to mask request headings
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'}

# create a session
session = Session()

# enter the website
session.get('http://quotes.toscrape.com/', headers=headers)

# go to login page and parse one-time token
response = session.get('http://quotes.toscrape.com/login', headers=headers)
soup = BeautifulSoup(response.text, 'lxml')
token = soup.find('form').find('input').get('value')

# to log in we need a dict with token, login and password
# (we can see it in 'Network' in path authorization)
input_data = {'csrf_token': token, 'username': '123', 'password': '123'}

# create a post request and get page after login
auth_page = session.post('http://quotes.toscrape.com/login', headers=headers, data=input_data, allow_redirects=True)

'''
Now we can create simple 'get' request to 'auth_page'
and then parse the information we need
'''
