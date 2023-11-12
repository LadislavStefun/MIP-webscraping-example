import requests
import bs4 as bs
import http.client
from bs4 import BeautifulSoup
import pandas as pd
http.client._MAXHEADERS = 1000


def scrape_stu_faculties(url):
    #základná dátová štruktúra, obasahujúc názvy a stŕanky fakúlt
    data_dict = {'Názov fakulty': [], 'Stránka fakulty': []}
    #program spraví get request na nami zvolený link a vráteny HTML dokument sprasuje nástroj BS4
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    #Vyhladaj všetky prvky, ktoré spĺňajú typ ul a sú triedy nav navbar-nav main-header-list
    #v tomto neusporiadanom liste sa nachádzajú informácie o fakultách aj so sprievodnými linkami na ich webové stránky
    ul_of_faculties = soup.find(
        "ul", {"class": "nav navbar-nav main-header-list"}).find_all("a")
    #prechádzame jednotlivými prvkami neusporiadaného listu a podľa stanovených kritérii hľadáme názvy fakúlt
    for item in ul_of_faculties:
        #Zisti či následovný prvok spĺňa základné kritéria, aby bol vložený do našej dátovej štruktúry
        if item.get('title') is not None and len(item.get('title')) > 1:
            data_dict['Názov fakulty'].append(item.get('title'))
            data_dict['Stránka fakulty'].append(item.get('href'))

    #1. Vytvor, 2. Zoraď a 3. Exportni dataframe pozbieraných dát
    df = pd.DataFrame(data_dict)
    df.sort_values("Názov fakulty", kind='quicksort', inplace=True)
    df.to_csv('fakulty.csv', index=False, encoding="utf-8")


def main():
    #hlavný chod programu
    url = "https://www.stuba.sk/"
    scrape_stu_faculties(url)


if __name__ == '__main__':
    main()
