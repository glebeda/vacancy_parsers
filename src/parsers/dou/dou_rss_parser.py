from datetime import datetime

import feedparser

from src.model import VacancyModel
from src.parsers.abstract_parser import AbstractParser
from src.utils import get_clean_summary, get_level, get_type


class DouRssParser(AbstractParser):

    def parse(self) -> [VacancyModel]:
        results = []
        feed = feedparser.parse('https://jobs.dou.ua/vacancies/feeds/?category=QA')
        for entry in feed['entries']:
            link = entry['id']
            title = entry['title']
            summary = entry['summary']
            published = entry['published']
            published_date = datetime.strptime(published, '%a, %d %b %Y %H:%M:%S %z').replace(tzinfo=None).isoformat()

            data = {
                "title": title,
                "link": link,
                "raw_text": summary,
                "clean_text": get_clean_summary(summary),
                "level": get_level(title),
                "type": get_type(title),
                "published": published_date,
            }

            results.append(VacancyModel(**data))

        return results
