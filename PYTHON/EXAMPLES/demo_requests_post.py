import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

url = 'https://www.w3schools.com/python/demopage.php'
myobj = {'1': 'chad'}

x = requests.post(url, data = myobj, verify=False)

#print the response text (the content of the requested file):
print(x.status_code)
print(x.text)
