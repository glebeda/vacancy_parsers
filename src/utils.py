import re

import requests

from src.constants import API_URL
from src.model import VacancyModel


def get_clean_summary(html):
    text = strip_tags(html)
    return text


def strip_tags(string):
    return re.sub(r'<.*?>', ' ', string)


def get_level(title):
    if "Junior" in title:
        return "junior"
    elif "Lead" in title:
        return "lead"
    elif "Senior" in title:
        return "senior"
    else:
        return "middle"


def get_type(title):
    if "automation" in title.lower() or "aqa" in title.lower():
        return "automation"
    else:
        return "manual"


def upload_results(results: [VacancyModel]):
    for result in results:
        requests.post(f"{API_URL}/vacancies", json=result.dict())
