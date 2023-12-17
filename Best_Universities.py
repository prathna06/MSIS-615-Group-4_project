import pandas as pd
import random
import time
from bs4 import BeautifulSoup
import requests
import sqlite3

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
}
def scrape():
    base_url = "https://www.usnews.com/best-colleges/search?_sort=rank&_sortDirection=asc&_page=%i"
    nationalUniversityURL = []
    for p in range(1, 1001):
        page = requests.get(base_url % p, headers=headers)
        print(base_url)
        soup = BeautifulSoup(page.text, 'lxml')
        for i in soup.find_all("a", {"class": "card-more"}):
            nationalUniversityURL.append(i['href'])
          

    websiteURL = 'https://www.usnews.com'
    university_data_list = []

    for url in nationalUniversityURL:
        page = requests.get(websiteURL + url, headers=headers)
        print(websiteURL+url)
        soup = BeautifulSoup(page.text, 'html.parser')

        university_data = {}
        #gtkLHO
        for i in soup.find_all("h1", {"class": "gtkLHO"}):
            university_name = i.find('span', class_='HeadingWithIcon__NoWrap-sc-1kfmde2-1').text.strip()
            print(i.contents[0]+university_name)
            university_data['University Name'] = i.contents[0]+university_name

        for i in soup.find_all("p", {"class": "ckzlaT"}):
            if i.contents == ['Acceptance Rate']:
                parent = i.parent
                university_data['Acceptance Rate'] = parent.find_all("p")[-1].contents[0]
            elif i.contents == ['SAT Range*']:
                parent = i.parent
                university_data['SAT Range'] = parent.find_all("p")[-1].contents[0]
            elif i.contents == ['ACT Range*']:
                parent = i.parent
                university_data['ACT Range'] = parent.find_all("p")[-1].contents[0]
            elif i.contents == ['Undergraduate Enrollment']:
                parent = i.parent
                university_data['Undergraduate Enrollment'] = parent.find_all("p")[-1].contents[0]
            elif i.contents == ['Tuition & Fees']:
                parent = i.parent
                university_data['Tuition & Fees'] = parent.find_all("p")[-1].contents[0]

        for i in soup.find_all("div", {"class": "kMhOFk"}):
            if i.contents == ['4-Year Graduation Rate']:
                parent = i.parent
                university_data['Graduation Rate'] = parent.find_all("p")[0].contents[0]
            elif i.contents == ['Student/Faculty Ratio']:
                parent = i.parent
                university_data['Student/Faculty Ratio'] = parent.find_all("p")[0].contents[0]

        university_data_list.append(university_data)
 
    return university_data_list

def save_to_csv(data_list, filename='university_data1.csv'):
    df = pd.DataFrame(data_list)

    # Add ranking column
    df['Ranking'] = range(1,1001)
    df.to_csv(filename, index=False)

def save_to_db(df):
   # df = pd.DataFrame(data_list)
    print(df)
    # Clean data
    data = clean_data(df)
    
    conn = sqlite3.connect(':memory:')
    data.to_sql(name='university_data', con=conn)

    university_data = pd.read_sql('select * from university_data', conn)
    print(university_data)

 
def clean_data(data):
    data['Ranking'] = range(1,1001)
    data['Tuition & Fees'] = pd.to_numeric(data['Tuition & Fees'].str.split('$').str.get(1).str.replace(',',''))
    data['Undergraduate Enrollment'] = pd.to_numeric(data['Undergraduate Enrollment'].str.replace(',',''))
    data['Acceptance Rate'] = pd.to_numeric(data['Acceptance Rate'].str.split('%').str.get(0))
    data['Minimum SAT score'] = pd.to_numeric(data['SAT Range'].str.split('-').str.get(0))
    data['Minimum ACT score'] = pd.to_numeric(data['ACT Range'].str.split('-').str.get(0))
    data['Graduation Rate'] = pd.to_numeric(data['Graduation Rate'].str.split('%').str.get(0))
    data['Student Per Faculty'] = pd.to_numeric(data['Student/Faculty Ratio'].str.split(':').str.get(0))

    data = data.dropna()

    data['Tuition & Fees'] = data['Tuition & Fees'].astype(int)
    data['Undergraduate Enrollment'] = data['Undergraduate Enrollment'].astype(int)
    data['Acceptance Rate'] = data['Acceptance Rate'].astype(int)
    data['Minimum SAT score'] = data['Minimum SAT score'].astype(int)
    data['Minimum ACT score'] = data['Minimum ACT score'].astype(int)
    data['Graduation Rate'] = data['Graduation Rate'].astype(int)
    data['Student Per Faculty'] = data['Student Per Faculty'].astype(int)

    del data['SAT Range']
    del data['ACT Range']
    del data['Student/Faculty Ratio']
    return data

if __name__ == '__main__':
   # university_data = scrape()  
  #save_to_csv(university_data)
    save_to_db(pd.read_csv('university_data1.csv'))