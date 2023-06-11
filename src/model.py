from datetime import datetime

from pydantic import BaseModel


class VacancyModel(BaseModel):
    title: str
    link: str
    level: str
    type: str
    clean_text: str
    raw_text: str
    published: str
