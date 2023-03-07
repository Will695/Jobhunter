import requests
from lxml import html
from bs4 import BeautifulSoup as bs
import pandas as pd
import warnings
import string
import webbrowser
from datetime import datetime
warnings.filterwarnings('ignore')


df = pd.DataFrame()

# url = 'https://jobserve.com/gb/en/JobListing.aspx?shid=9E3A653CA4FC49D2D13B&page=1'

'''
Varibles that you can change 
'''
skillset = ['windows','server','gpo','active','directory','sccm','vmware','itil','ad','gp','dns','dhcp','dfs','rds','infrastructure', 'powershell']
keywords = ['wintel','infrastructure engineer','wintel engineer','windows server']
matchcount = 4
filterdate = '2023-03-05'

######### don't change anything below ########
baseurl = 'https://jobserve.com'

for keyword in keywords:
    print(keyword)
    keyword = keyword.replace(' ','+')
    url = f'https://jobserve.com/gb/en/JobListing.aspx?shid=9E3A653CA4FC49D2D13B&sq=%22{keyword}%22'
    r = requests.get(url)

    soup = bs(r.content, "html.parser")

    jobs = soup.find("div", attrs={"class": "jobSearchContainer"})

    jobdivs = ['jobListingItemEven','jobListingItem']

    # for jobdiv in jobdivs:
    #     jobdiv = str(jobdiv)

    evenjobs = jobs.find_all("div", attrs={"class": 'jobListingItemEven'})
    print('getting evens')
    for i in range(len(evenjobs)):
        title = evenjobs[i].find('a', attrs={"class":"jobListPosition"}).text
        href = evenjobs[i].find('a', attrs={"class":"jobListPosition"})
        href = href['href']
        salary = evenjobs[i].find('span', attrs={"class":"jobListRate"}).text
        location = evenjobs[i].find('span', attrs={"class":"jobListLocation"}).text
        jobtype = evenjobs[i].find('span', attrs={"class":"jobListJobType"}).text
        joburl = f'{baseurl}{href}'
        print('evens')
        df = df.append({
            'title':title.lower(),
            'url':joburl.lower(),
            'salary':salary.lower(),
            'location':location.lower(),
            'jobtype':jobtype.lower(),
            },ignore_index=True)

    oddsjobs = jobs.find_all("div", attrs={"class": 'jobListingItem'})
    print('getting odds')
    for i in range(len(oddsjobs)):
        title = oddsjobs[i].find('a', attrs={"class":"jobListPosition"}).text
        href = oddsjobs[i].find('a', attrs={"class":"jobListPosition"})
        href = href['href']
        salary = oddsjobs[i].find('span', attrs={"class":"jobListRate"}).text
        location = oddsjobs[i].find('span', attrs={"class":"jobListLocation"}).text
        jobtype = oddsjobs[i].find('span', attrs={"class":"jobListJobType"}).text
        joburl = f'{baseurl}{href}'
        print('added odds')
        df = df.append({
            'title':title.lower(),
            'url':joburl.lower(),
            'salary':salary.lower(),
            'location':location.lower(),
            'jobtype':jobtype.lower(),
            },ignore_index=True)


desurl = df[:1]['url'].values[0]

temp = df

# descr = requests.get(desurl)

# soup = bs(descr.content, "html.parser")

# description = soup.find("div", attrs={"class": "md_skills"}).text.lower()

# filter for keywords
temp.index = range(len(temp['url']))

def matchskills(url,skillset):
    descr = requests.get(url)

    
    soup = bs(descr.content, "html.parser")
    
    description = soup.find("div", attrs={"class": "md_skills"}).text.lower()
    dateposted = soup.find("span", attrs={"class": "td_posted_date"}).text.lower()
    dateposted = dateposted.strip('posted: ')
    dateposted = dateposted.split(', ')[1]
    temp.at[temp[temp['url'] == url].index.values[0],'dateposted'] = dateposted
    descriptionstr = description

    description = description.replace('\n',' ')
    description = description.translate(str.maketrans('', '', string.punctuation))
    description = description.split(' ')
    
    # skillset = ['windows','server','gpo','active','directory','sccm','vmware','itil','ad','gp','dns','dhcp','dfs','rds','infrastructure', 'powershell']
    # for i in range(len(temp['link'])):
    count = 0
    if 'inside ir35' in descriptionstr:
        temp.at[temp[temp['url'] == url].index.values[0],'ir35'] = 'inside ir35'  
    if 'outside ir35' in descriptionstr:
        print('found outside')
        temp.at[temp[temp['url'] == url].index.values[0],'ir35'] = 'outside ir35'  
    # desc = temp[temp['link'] == temp['link'][i]]['main-description'].values[0].split(' ')
    for skill in skillset:
        if skill in description:
            print(skill)
            count += 1

    temp.at[temp[temp['url'] == url].index.values[0],'count'] = count
    temp.at[temp[temp['url'] == url].index.values[0],'realurl'] = descr.url


jobcount = len(temp['url'])
for i in range(len(temp['url'])):
    print(f'{i} out of {jobcount}')
    matchskills(temp['url'][i],skillset)


temp['ir35'] = temp['ir35'].fillna('none')

temp['date'] = temp['dateposted']

temp['date'] = pd.to_datetime(df['date'], dayfirst=True)

res = df.sort_values('date', ascending=False)

res = res.fillna('none')

res = res[res['date'] != 'none']

res = res[res['count'] > matchcount] 

res.index = range(len(res['date']))

res = res[res['date'].astype(str) > filterdate]

#### This bit opens the webpages, you can comment this bit out and send it to a csv if needed
for i in range(len(res['realurl'])):
    webbrowser.open(res['realurl'][i])