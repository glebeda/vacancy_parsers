from src.model import VacancyModel


class AbstractParser(object):

    def parse(self) -> [VacancyModel]:
        raise NotImplementedError
