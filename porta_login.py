import cookielib
import urllib
import urllib2
from bs4 import BeautifulSoup


USERNAME = str(raw_input("Benutzer: "))
PASSWORD = str(raw_input("Passwort: "))

URL = "https://porta-system.uni-trier.de/qisserver/pages/sul/examAssessment/personExamsReadonly.xhtml?_flowId=examsOverviewForPerson-flow&_flowExecutionKey=e1s1"

# Store the cookies and create an opener that will hold them
cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

# Add our headers
opener.addheaders = [('User-agent', 'Porta Login')]

# Install our opener (note that this changes the global opener to the one
# we just made, but you can also just call opener.open() if you want)
urllib2.install_opener(opener)

# The action/ target from the form
authentication_url = 'https://porta-system.uni-trier.de:443/qisserver/rds?state=user&type=1&category=auth.login'

# Input parameters we are going to send
payload = {
  #'op': 'login-main',
  'asdf': USERNAME,
  'fdsa': PASSWORD
  }

# Use urllib to encode the payload
data = urllib.urlencode(payload)

# Build our Request object (supplying 'data' makes it a POST)
req = urllib2.Request(authentication_url, data)

# Make the request and read the response
resp = urllib2.urlopen(req)
contents = resp.read()

# Scrape Content with BS
page = urllib2.urlopen(URL).read()
soup = BeautifulSoup(page, "lxml")
div = soup.find('div', id='examsReadonly:overviewAsTreeReadonly')
for tr in soup.find_all('tr')[3:]:
    tds = tr.find_all('td')
    print "Grade: %s, Points: %s" % (tds[9].text, tds[10].text)
