from bs4 import BeautifulSoup, Comment
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import re

proxy = [
    'http://104.207.44.69:3128',
    'http://104.207.56.240:3128',
    'http://104.207.35.225:3128',
    'http://104.207.46.127:3128',
    'http://104.207.32.158:3128'
    ]

#* Scraper Class
class Scraper:
    def __init__(self, headless=False, disable_images=True):
        self.options = webdriver.EdgeOptions()

        prox = random.choice(proxy)

        self.options.add_argument(f'--proxy-server={prox}')

        print(f'\nUsing proxy: {prox}\n')

        if headless:
            self.options.add_argument('--headless')

        if disable_images:
            prefs = {"profile.managed_default_content_settings.images": 2, 'profile.managed_default_content_settings.javascript': 2}
            self.options.add_experimental_option("prefs", prefs)

        self.driver = webdriver.Edge(options=self.options)
        self.wait = WebDriverWait(self.driver, 10)

    def get_source(self, url):
        self.driver.get(url)
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body')))

        return self.driver.page_source
    
    def get_lyrics(self, source):
        soup = BeautifulSoup(source, 'html.parser')
        comment = soup.find(string=lambda text: isinstance(text, Comment) and text == ' Usage of azlyrics.com content by any third-party lyrics provider is prohibited by our licensing agreement. Sorry about that. ')
        
        if comment:
            lyrics = comment.find_parent().text.strip()
            return lyrics
        
        return None
    
    def get_genius_lyrics(self, source):
        soup = BeautifulSoup(source, 'html.parser')
        lyrics = soup.find_all('div', class_='Lyrics__Container-sc-1ynbvzw-1')

        if lyrics:
            lyrics = " ".join([lyric.text for lyric in lyrics])
            return lyrics
        
        return None

    def get_youtube_link(self, source):
        soup = BeautifulSoup(source, 'html.parser')
        youtube_link_tag = soup.find('a', class_='play-this-track-playlink--youtube')

        if youtube_link_tag:
            youtube_link = youtube_link_tag['href']
            return youtube_link
        
        return None
    
    def get_movie_name(self, source):
        soup = BeautifulSoup(source, 'html.parser')
        movie_name = soup.find('span', class_='feat')
        in_movie = False
        movie = None

        if movie_name is not None:
            movie_name = movie_name.text

            reg = re.findall('from "(.*?)" soundtrack', movie_name)

            if reg:
                movie = reg[0]
                in_movie = True

        return in_movie, movie

    def close(self):
        self.driver.close()