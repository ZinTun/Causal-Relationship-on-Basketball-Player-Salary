from bs4 import BeautifulSoup
import requests

import pandas as pd
import numpy as np

#needed to convert unicode to numeric
import unicodedata
import time
import sys
import csv
    
def createDataFrame(cols, rows):
    l = range(len(rows))

    table = pd.DataFrame(columns=cols, index = l)    # create dataframe with schema


    for i in l:
        if len(rows[i]) == len(cols):
            table.loc[i]=rows[i]

    return table

def getPlayerSalary(playerURL, teamURL):
    try:
        time.sleep(0.5)
        salary = 'NA'
        req = requests.get(playerURL)
        text = BeautifulSoup(req.text, "html.parser")
        if len(text.findAll('div', {'id':'all_all_salaries'})) == 0 or teamURL == 'NA':
            print playerURL
            print teamURL
            return salary
        stats = str(text.findAll('div', {'id':'all_all_salaries'})[0]).replace('<!--','').replace('-->','')

        text = BeautifulSoup(stats, "html.parser")

        stats = text.find('table', {'id': 'all_salaries'})
        

        for i in stats.tbody.find_all('tr'):
            result = []
            hasData = True
            salary = 'NA'
        

            if len(i.find_all('td')) == 0:
                hasData = False
            
            for j in i.find_all('td'):
                text = j.get_text()


                if 'team_name' in str(j):
                    if len(j.find_all('a')) == 0:
                        team = 'NA'
                    else:
                        teamYear =  j.find_all('a')[0]['href']
                        
                        team = teamYear.split('/')[2]
                        year = teamYear.split('/')[3][:-5]
                        
                if 'salary' in str(j):
                    salary = text.replace('$', '').replace(',','')       

            if hasData:

                teamToMatch = teamURL.split('/')[4]
                yearToMarch = teamURL.split('/')[5][:-5]
                


                                
                if year == yearToMarch and team == teamToMatch:
                    return salary

        return salary
    except Exception as e:
        print e
        print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ GOT ERROR ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
        salary = 'ERROR'
        return salary


with open('error.csv', 'rb') as f:
    reader = csv.reader(f)
    your_list = list(reader)

cols = []
rows = []

cols.append('Player_URL')
cols.append('Team_URL')
cols.append('Year')
cols.append('Salary')
for i in your_list:
    print i

    i[3] = getPlayerSalary(i[0], i[1])
    rows.append(i)

for i in range(len(rows)):
    rows[i] = [x.encode('UTF8') for x in rows[i]]                          

cols = [x.encode('UTF8') for x in cols]
a = createDataFrame(cols,rows)
a.to_csv('reprocessed.csv', index = False)
