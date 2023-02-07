import yaml
from bs4 import BeautifulSoup
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class WebScraper:
    def __init__(self, config):
        self.config = config

    def fetch_html(self, url):
        driver = webdriver.Firefox()
        driver.get(url)
        wait = WebDriverWait(driver, 10)
        for tag in self.config['tags']:
            wait.until(EC.presence_of_element_located((By.XPATH, tag)))
        html = driver.page_source
        driver.close()
        return html

    def extract_data(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        data = []
        dom = etree.HTML(str(soup))
        for tag in self.config['tags']:
            elements = dom.xpath(tag)
            for element in elements:
                data.append(element.text.strip())

        # TODO: Get detail content from the url
        # links = dom.xpath(tag + '/parent::a')
        # if len(links) > 0:
        #     for link in links:
        #         if link.attrib['href'].startswith('/'):
        #             link.attrib['href'] = url + link.attrib['href']
        #         # Open the link and get the detail content
        #         open_link_html = self.fetch_html(link.attrib['href'])
        #         detail_content = self.extract_data(open_link_html)
        return data

if __name__ == '__main__':
    with open('config/website_lists.yaml') as f:
        config = yaml.safe_load(f)

    websites = config['websites']
    for website in websites:
        name = website['name']
        url = website['url']
        tags = website['tags']
        print(f"Fetching data from {name}...")
        scraper = WebScraper({'tags': tags})
        html = scraper.fetch_html(url)
        data = scraper.extract_data(html)
        print(f"Data from {name}: {data}")
