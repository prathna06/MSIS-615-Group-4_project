import pandas as pd
import random
import time
from bs4 import BeautifulSoup
import requests


headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
}

def scrape():
    base_url = "https://www.usnews.com/best-colleges/rankings/national-universities?_page=%i"
    nationalUniversityURL = []

    for p in range(1, 11):
        page = requests.get(base_url % p, headers=headers)
        soup = BeautifulSoup(page.text, 'lxml')

        for i in soup.find_all("a", {"class": "card-more"}):
            nationalUniversityURL.append(i['href'])

    websiteURL = 'https://www.usnews.com'
    university_data_list = []

    for url in nationalUniversityURL:
        page = requests.get(websiteURL + url, headers=headers)
        soup = BeautifulSoup(page.text, 'html.parser')

        university_data = {}

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

        for i in soup.find_all("div", {"class": "kMhOFk"}):
            if i.contents == ['4-Year Graduation Rate']:
                parent = i.parent
                university_data['Graduation Rate'] = parent.find_all("p")[0].contents[0]
            elif i.contents == ['Student/Faculty Ratio']:
                parent = i.parent
                university_data['Student/Faculty Ratio'] = parent.find_all("p")[0].contents[0]

        university_data_list.append(university_data)

    return university_data_list

def save_to_csv(data_list, filename='university_data.csv'):
    df = pd.DataFrame(data_list)
    df.to_csv(filename, index=False)

if __name__ == '__main__':
    university_data = scrape()
    save_to_csv(university_data)
