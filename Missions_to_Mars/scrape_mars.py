from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
from webdriver_manager.chrome import ChromeDriverManager


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path':ChromeDriverManager().install()}
    return Browser("chrome", **executable_path, headless=False)


def scrape_info():
    browser = init_browser()
    mars_data = {}

    # Mars News URL
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    # Scrape page into Soup
    html = browser.html
    news_soup = bs(html, "html.parser")

    #scrapping latest news about mars from nasa
    news_title = news_soup.find_all("div",class_="content_title").text
    news_par = news_soup.find("div", class_="article_teaser_body").text

    # JPL Mars Space Images to be scraped
    jpl_nasa_url = 'https://www.jpl.nasa.gov'
    images_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(images_url)
    html = browser.html
    images_soup = bs(html, 'html.parser')
    # Retrieve featured image link
    relative_image_path = images_soup.find_all('img')[3]["src"]
    featured_image_url = jpl_nasa_url + relative_image_path
    
    # Mars facts to be scraped
    facts_url = 'https://space-facts.com/mars/'
    tables = pd.read_html(facts_url)
    mars_facts_df = tables[2]
    mars_facts_df.columns = ["Description", "Value"]
    mars_html_table = mars_facts_df.to_html()
    mars_html_table.replace('\n', '')

    # Mars 
    mars_dict = {
        "news_title": news_title,
        "news_par": news_par,
        "featured_image_url": featured_image_url,
        "fact_table": str(mars_html_table),
        "hemisphere_images": hemisphere_image_urls
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data
