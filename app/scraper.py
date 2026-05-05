import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from app.code_agent import CodeAgent
from app.config import Settings
from app.models import ScrapedRecord
from app.utils import ensure_dir, dump_json, dump_csv


def build_driver(s: Settings):
    options = Options()
    options.page_load_strategy = 'eager'
    options.add_argument('--window-size=1440,1200')
    options.add_argument('--no-sandbox')
    if s.headless:
        options.add_argument('--headless=new')
    if s.proxy_url:
        options.add_argument(f'--proxy-server={s.proxy_url}')
    return webdriver.Chrome(options=options)


def login(driver, s: Settings):
    driver.get(f'{s.base_url}/login')
    wait = WebDriverWait(driver, s.timeout_seconds)
    wait.until(EC.visibility_of_element_located((By.ID, 'username'))).clear()
    driver.find_element(By.ID, 'username').send_keys(s.username)
    driver.find_element(By.ID, 'password').clear()
    driver.find_element(By.ID, 'password').send_keys(s.password)
    driver.find_element(By.ID, 'login-button').click()
    wait.until(EC.url_contains('/feed'))


def extract(driver, s: Settings, agent: CodeAgent):
    records = []
    for card in agent.find_many(driver, 'card'):
        title = agent.find_first(card, 'title')
        category = agent.find_first(card, 'category')
        price = agent.find_first(card, 'price')
        rating = agent.find_first(card, 'rating')
        if not all([title, category, price, rating]):
            continue
        href = title.get_attribute('href') or '/'
        records.append(ScrapedRecord(external_id=card.get_attribute('data-id') or title.text[:20], title=title.text,
                                     category=category.text, price=agent.money(price.text),
                                     rating=agent.rating(rating.text),
                                     url=href if href.startswith('http') else s.base_url.rstrip('/') + href))
    return records


def run_scrape(s: Settings):
    out = ensure_dir(s.output_dir)
    agent = CodeAgent()
    driver = build_driver(s)
    try:
        login(driver, s)
        WebDriverWait(driver, s.timeout_seconds).until(EC.presence_of_element_located((By.ID, 'feed')))
        last = 0
        stagnant = 0
        for _ in range(s.page_limit):
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            time.sleep(.8)
            count = len(driver.find_elements(By.CSS_SELECTOR, '.product-card,[data-role="product-card"],article'))
            if count >= s.item_target:
                break
            stagnant = stagnant + 1 if count == last else 0
            if stagnant >= 2:
                break
            last = count
        rows = extract(driver, s, agent)
        dump_json(out / 'dynamic_records.json', rows)
        dump_csv(out / 'dynamic_records.csv', rows)
        dump_json(out / 'selector_report.json', [agent.report])
        return out / 'dynamic_records.json', out / 'dynamic_records.csv', len(rows)
    finally:
        driver.quit()
