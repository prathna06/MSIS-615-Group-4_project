import pandas as pd
import random
import time
from bs4 import BeautifulSoup
import requests
import lxml

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
}


def scrape():
    base_url = "https://www.usnews.com/education/best-global-universities/rankings?page=%i"
    results = []
    for p in range(1, 10):
        page = requests.get(base_url % p, headers = headers)
        soup = BeautifulSoup(page.text, 'lxml')
        res_tab = soup.find('div', {'id' : 'rankings'}) 
        page_universities = res_tab.find_all('ol')
        for univ in page_universities[0].select('li[class*="item-list__ListItemStyled-sc"]'):
            university_data = []
            if univ.get_text() != '':
                name = univ.find('h2').getText()
                print("Name:" + name)
                ranking = univ.find('li').getText().split(" ")[0][1:-2]
                print("Ranking:" + ranking)
                enrollment = univ.select('dd[class*="QuickStatHug__"]')[1].getText()
                print("Enrollment:" + enrollment)
                university_data.append(name)
                university_data.append(ranking)
                university_data.append(enrollment)
                results.append(university_data)
        time.sleep(random.randint(2,4))

    return pd.DataFrame(results)

if __name__ == '__main__':
    
    final = scrape()

    final.to_csv("enrolmentRanking.csv", encoding='utf-8-sig', index=False)



