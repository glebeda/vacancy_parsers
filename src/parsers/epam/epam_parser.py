import time
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager

from src.model import VacancyModel
from src.parsers.abstract_parser import AbstractParser
from src.utils import get_level, get_type, get_clean_summary


class EpamParser(AbstractParser):
    BASE_URL = "https://careers.epam.ua/vacancies/job-listings?country=Ukraine"

    def parse(self) -> [VacancyModel]:
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get(self.BASE_URL)

        show_more_selector = 'a.search-result__view-more'

        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, show_more_selector)))
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, show_more_selector)))

        while True:
            try:
                last_element = driver.find_element(By.XPATH, "(//*[contains(@class, 'search-result__item')])[last()]")
                driver.execute_script("arguments[0].scrollIntoView(true);", last_element)
                show_more = driver.find_element(By.CSS_SELECTOR, show_more_selector)
                if not show_more.is_displayed():
                    break
                show_more.click()
                time.sleep(3)
            except NoSuchElementException:
                break

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()

        jobs = soup.find_all(class_='search-result__item')
        results = []
        for job in jobs:
            title = job.find(class_='search-result__item-name').get_text(strip=True)
            link = job.find('a')['href']
            description = job.find(class_='search-result__item-description').get_text(strip=True)

            data = {
                "title": title,
                "link": link,
                "raw_text": description,
                "clean_text": get_clean_summary(description),
                "level": get_level(title),
                "type": get_type(title),
                "published": "",
            }
            results.append(VacancyModel(**data))

        return results
