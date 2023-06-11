from datetime import datetime

import requests
from bs4 import BeautifulSoup

from src.model import VacancyModel
from src.parsers.abstract_parser import AbstractParser
from src.utils import get_clean_summary, get_level, get_type


class LinkedinParser(AbstractParser):
    BASE_URL = "https://www.linkedin.com/jobs/search?keywords=Qa" \
               "&location=%D0%A3%D0%BA%D1%80%D0%B0%D0%B8%D0%BD%D0%B0" \
               "&locationId=&geoId=102264497&f_TPR=r86400&position=1&pageNum=0"

    def parse(self) -> [VacancyModel]:
        response = requests.get(self.BASE_URL)
        page = BeautifulSoup(response.text, "html.parser")
        all_links = page.find_all('a', class_='base-card__full-link', href=True)
        results = []
        for link in all_links:
            vacancy_link = link['href']
            response = requests.get(vacancy_link)
            vacancy = BeautifulSoup(response.text, "html.parser")
            title = vacancy.select_one('h1.top-card-layout__title').getText().strip()
            if "qa" not in title.lower():
                print(f"Skip position {title}")
                continue

            html_summary = vacancy.select_one('div.show-more-less-html__markup')
            summary = str(html_summary).replace("</br>", " ")

            data = {
                "title": title,
                "link": vacancy_link,
                "raw_text": summary,
                "clean_text": get_clean_summary(summary),
                "level": get_level(title),
                "type": get_type(title),
                "published": datetime.now().isoformat(),
            }

            results.append(data)
        return results
