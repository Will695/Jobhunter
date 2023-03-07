# Jobhunter
Web scraping job sites (jobserve.co.uk)


You will need to install the dependencies
You can do that by installing from requirements.txt.

Open up a command prompt and change directory to the files.

Now run 

```
pip install -r requirements.txt
```

You need to change is the Skillset and Keyword variables to match your search criteria
```python
skillset = ['windows','server','gpo','active','directory','sccm','vmware','itil','ad','gp','dns','dhcp','dfs','rds','infrastructure', 'powershell']
keywords = ['wintel','infrastructure engineer','wintel engineer','windows server']
```

You can also change the matchcount. This is from were it goes off to the description and matches words from the skillset variables the higher the number the more granular it gets

```python
matchcount = 4
```

you can also change the filterdate to look at jobs after a certain date make sure you follow the date format. YYYY-MM-DD

```python 
filterdate = '2023-03-05'
```