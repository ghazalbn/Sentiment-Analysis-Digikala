from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from scrapy.http import HtmlResponse
import scrapy
import time
import urllib.parse


class MySpider(scrapy.Spider):
    name = 'digikala_spider'
    start_urls = ['https://bitly.cx/iyC3k']

    def __init__(self, *args, **kwargs):
        super(MySpider, self).__init__(*args, **kwargs)
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.wait = WebDriverWait(self.driver, 10)

    def parse(self, response):
        parsed_url = urllib.parse.urlparse(response.url)
        query_params = urllib.parse.parse_qs(parsed_url.query)
        query_params['pageSize'] = '100'
        new_query_string = urllib.parse.urlencode(query_params, doseq=True)
        new_url = urllib.parse.urlunparse(parsed_url._replace(query=new_query_string))

        self.driver.get(new_url)
        time.sleep(10)

        self.scroll_to_comments_section()
        time.sleep(5)

        self.handle_show_more_buttons(new_url)

        # Extract and follow pagination
        while True:
            self.logger.info("Extracting comments from current page...")
            yield from self.extract_comments(new_url)
            try:
                next_page_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='font-body flex justify-center items-center text-primary-700 cursor-pointer mr-2 pl-3 flex-row-reverse']")))
                self.driver.execute_script("arguments[0].click();", next_page_button)
                time.sleep(6)  # Wait for the next page to load
            except Exception as e:
                self.logger.info(f'No more next page button or error occurred: {e}')
                break

    def handle_show_more_buttons(self, url):
        while True:
            try:
                show_more_button = self.driver.find_element(By.CSS_SELECTOR, 'button[data-cro-id="pdp-comments-more"]')
                self.scroll_to_show_more_button()
                self.driver.execute_script("arguments[0].click();", show_more_button)
                time.sleep(3)  
                self.scroll_to_comments_section() 
            except Exception as e:
                self.logger.info(f'No more "Show More" buttons or error occurred: {e}')
                break

    def extract_comments(self, url):
        body = self.driver.page_source
        scrapy_response = HtmlResponse(url=url, body=body, encoding='utf-8')

        comments = scrapy_response.css('article.py-3.lg\\:mt-0.br-list-vertical-no-padding-200')
        if not comments:
            self.logger.info('No comments found.')

        for comment in comments:
            user_name = comment.css('p.text-caption.text-neutral-400::text').get()
            comment_text = comment.css('p.text-body-1.text-neutral-900.mb-1.pt-3.break-words::text').get()
            star_rating = self.extract_star_rating(comment)
            sentiment = self.map_star_rating_to_sentiment(star_rating)
            yield {
                'user_name': user_name,
                'comment_text': comment_text,
                'star_rating': star_rating,
                'sentiment': sentiment,
            }

    def extract_star_rating(self, comment):
        star_rating_element = comment.css('div.absolute.right-0.top-0.overflow-hidden.h-5')
        if star_rating_element:
            style = star_rating_element.attrib.get('style', '')
            width_percent = self.extract_percentage(style)
            return round((width_percent / 100) * 5)
        return 0

    def extract_percentage(self, style):
        try:
            width_str = style.split('width: ')[1].split('%')[0]
            return float(width_str)
        except (IndexError, ValueError):
            return 0.0

    def map_star_rating_to_sentiment(self, star_rating):
        if star_rating in [0, 1, 2]:
            return 'negative'
        elif star_rating == 3:
            return 'neutral'
        elif star_rating in [4, 5]:
            return 'positive'

    def scroll_to_comments_section(self):
        comments_section = self.driver.find_element(By.ID, 'commentSection')
        self.driver.execute_script("arguments[0].scrollIntoView();", comments_section)
        time.sleep(2)

    def scroll_to_show_more_button(self):
        show_more_button = self.driver.find_element(By.CSS_SELECTOR, 'button[data-cro-id="pdp-comments-more"]')
        self.driver.execute_script("arguments[0].scrollIntoView();", show_more_button)
        time.sleep(2) 

    def closed(self, reason):
        self.driver.quit()
