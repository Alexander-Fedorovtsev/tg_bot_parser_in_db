import requests
import config
import pandas as pd
from bs4 import BeautifulSoup as BS
from sqlighter import SQLcity


class Parsercity():
    def __init__(self, parse_url):
        """Парсим переданную страницу и создаем объект dataframe"""
        r = requests.get(parse_url)
        self.soup = BS(r.content, "html.parser")
        self.df = pd.DataFrame(columns=['city', 'url', 'population'])
        table = self.soup.find("table", class_="standard sortable")
        for row in table.tbody.find_all('tr'):    
            columns = row.find_all('td')
            if(columns != []):
                city = columns[1].text.strip()
                url = columns[1].a.get("href")
                population = columns[4].get("data-sort-value")
                self.df = self.df.append({'city': city,  'url': url, 'population': population,}, ignore_index=True)
    
    def add_in_db(self, db):
        """Добавляем данные в таблицу с городами если городов там нет"""
        for i, row in self.df.iterrows():
            if not db.get_city_names(row[0]):
                db.add_city(row[0],row[1],row[2])



if __name__ == "__main__":
    # код для отладки
    db = SQLcity("db.db")
    Parsercity(config.PARSE_URL).add_in_db(db)
    CITY = "верея"
    print(db.find_city(CITY))
    if db.find_city(CITY):
        print(db.find_city(CITY)[1])
        print(db.find_city(CITY)[2])
        print(db.find_city(CITY)[3])        

        

    

