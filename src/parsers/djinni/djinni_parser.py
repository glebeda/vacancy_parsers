import datetime

import requests
from bs4 import BeautifulSoup

from src.model import VacancyModel
from src.parsers.abstract_parser import AbstractParser
from src.utils import get_level, get_type, get_clean_summary


class DjinniParser(AbstractParser):
    BASE_URL = "https://djinni.co"

    def parse(self) -> [VacancyModel]:
        url = f"{self.BASE_URL}/jobs/?all-keywords=&any-of-keywords=&exclude-keywords=" \
              "&primary_keyword=QA&primary_keyword=QA+Automation"
        response = requests.get(url)
        print()
        page = BeautifulSoup(response.text, "html.parser")

        all_links = page.find_all('a', class_='profile', href=True)

        results = []
        for link in all_links:
            vacancy_link = f"{self.BASE_URL}{link['href']}"
            response = requests.get(vacancy_link)
            vacancy = BeautifulSoup(response.text, "html.parser")
            title = vacancy.select_one('div.detail--title-wrapper h1').getText().strip()
            summary = vacancy.select_one('div.row-mobile-order-2')

            print()
            data = {
                "title": title,
                "link": vacancy_link,
                "raw_text": str(summary),
                "clean_text": summary.get_text(),
                "level": get_level(title),
                "type": get_type(title),
                "published": datetime.datetime.now().isoformat(),
            }

            results.append(VacancyModel(**data))
        return results
