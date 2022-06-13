import contextlib
import json
import time
import traceback

from django.core.management.base import BaseCommand, CommandError
from biblishelf_web.apps.main.models import RepoModel, ResourceModel
from biblishelf_web.apps.book.models import BookModel
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
import re


class Command(BaseCommand):
    help = ''

    def add_arguments(self, parser):
        parser.add_argument('db', type=str)
        parser.add_argument('--headless', action='store_true')

    def handle(self, db, headless, *args, **options):

        with self.open(headless) as browser:
            for book in BookModel.objects.using(db).filter(
                douban_id__isnull=True
            ).exclude(isbn__isnull=True):
                try:
                    res = self.search_isbn(browser, book.isbn)
                except KeyboardInterrupt:
                    print("user interrupt")
                    break
                except:
                    traceback.print_exc()
                    continue
                assert isinstance(book, BookModel)
                if res:
                    print(res)
                    book.douban_id = res.get("douban_id")
                    book.name = res.get("title", book.name)
                    book.info = json.dumps(res)
                    book.save(update_fields=('douban_id', 'name', 'info'), using=db)

    @contextlib.contextmanager
    def open(self, headless):
        options = Options()
        options.headless = headless
        self.browser = webdriver.Firefox(
            options=options,
            executable_path=".\dev\geckodriver.exe"
        )
        try:
            yield self.browser
        except:
            traceback.print_exc()
        self.browser.close()

    def search_isbn(self, browser: webdriver.Firefox, isbn):
        browser.get("https://book.douban.com/")
        assert "豆瓣读书" in browser.title
        elem = browser.find_element(By.NAME, "search_text")
        elem.clear()
        elem.send_keys(isbn)
        elem.send_keys(Keys.RETURN)
        wait = WebDriverWait(browser, 10)
        wait.until(EC.title_contains(isbn))
        wait.until(EC.presence_of_element_located(
            (By.XPATH, "/html/body/div[@id='wrapper']/div[@id='root']/div/div/div/div/div/div[@class='item-root']/a[@class='cover-link']")
        ))
        elems = browser.find_elements(
            by=By.XPATH,
            value="/html/body/div[@id='wrapper']/div[@id='root']/div/div/div/div/div/div[@class='item-root']/a[@class='cover-link']"
        )
        for elem in elems:
            elem.click()
            break
        wait.until(EC.url_contains('https://book.douban.com/subject/'))
        res = {}
        if match := re.match(r'https://book.douban.com/subject/(\d+)/', browser.current_url):
            douban_id = match.groups()[0]
            res['douban_id'] = douban_id
            image = browser.find_element(
                by=By.XPATH,
                value="/html/body/div[@id='wrapper']/div[@id='content']/div/div[1]/div[1]/div[1]/div[1]/div[1]/a"
            )
            res['image_url'] = image.get_attribute("href")
            title_dom = browser.find_element(
                by=By.XPATH,
                value="/html/body/div[@id='wrapper']/h1/span"
            )
            res['title'] = title_dom.text
            info = browser.find_element(
                by=By.XPATH,
                value="/html/body/div[@id='wrapper']/div[@id='content']/div/div[1]/div[1]/div[1]/div[1]/div[@id='info']"
            )
            m = {}
            for item in info.text.split("\n"):
                try:
                    k, v = item.split(":", maxsplit=1)
                except:
                    print(f"error {item}")
                    continue
                k, v = k.strip(), v.strip()
                m[k] = v
            res['author'] = m.get("作者")
            res['publisher'] = m.get("出版社")
            res['publisher_data'] = m.get("出版年")
            try:
                res["page"] = int(m.get("页数"))
            except:
                print(f"error {m}")
            res['info'] = m

            return res
