import requests
from bs4 import BeautifulSoup
from pdb import set_trace as bp
 
url = 'http://www.eventkeeper.com/mars/xpages/N/NEWTON/ek.cfm?curOrg=NEWTON'
headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
 
r = requests.get(url, headers=headers)
 
# make sure that the page exist
 
if r.status_code == 200:
    html = r.text
    soup = BeautifulSoup(html, features="lxml")
    event_dates = soup.find_all("div", {"class": "event_date"})
    events = []
    if event_dates is not None:
        for event_date in event_dates:
            for tag in event_date.parent.next_siblings:
                if tag.name and tag.get("class") == ['one_event']:
                    event = {}
                    event["date"] = event_date.text.strip()
                    event_name = tag.find("div", {"class": "event_name"})
                    if event_name:
                        event["name"] = event_name.text.strip()
                    event_time = tag.find("div", {"class": "event_time"})
                    if event_time:
                        event["time"] = event_time.text.strip()
                    event_description = tag.find("div", {"class": "event_description"})
                    if event_description:
                        event["description"] = event_description.text.strip()
                    events.append(event)
                elif tag.name and tag.get("class") == ['event_date_row']:
                    break
        print(events)
