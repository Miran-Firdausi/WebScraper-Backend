import time
from selenium import webdriver
from selenium.webdriver import ChromeOptions, ActionChains
from filelock import FileLock
from .coin_mapping import COIN_MAP
from bs4 import BeautifulSoup
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

options = ChromeOptions()
options.add_argument('--headless=new')

EXCEL_FILE = 'output.xlsx'
LOCK_FILE = 'output.xlsx.lock'


def convert_to_number(string):
    """
    Converts a string including symbols and commas to a numerical value.
    """
    number = string.split()[0]
    number = number.replace('$', '').replace(',', '').replace('%', '')
    return float(number)


class CoinMarketCap:
    @staticmethod
    def get_coin_url(coin_abbr):
        base_url = "https://coinmarketcap.com/currencies/"
        coin_name = COIN_MAP.get(coin_abbr, coin_abbr.lower())
        return f"{base_url}{coin_name}"

    @staticmethod
    def scrape(url):
        print("Connecting to scraping browser")
        html = ""
        with webdriver.Chrome(options=options) as driver:
            print(f"Connected! Navigated to {url}")
            driver.get(url)
            time.sleep(10)
            html = driver.page_source
        print("Done Scraping!")
        return html

    @staticmethod
    def get_coin_data(html):
        soup = BeautifulSoup(html, "html.parser")

        coin_stats_div = soup.find('div', {'data-module-name': 'Coin-stats'})
        coin_data = {}

        if coin_stats_div:
            # Extract price
            price = coin_stats_div.find('span', {'class': 'sc-d1ede7e3-0 fsQm base-text'}).text.strip()
            price = convert_to_number(price)
            coin_data['price'] = price

            # Extract price change
            price_change_element = coin_stats_div.find('p', {'class': 'sc-71024e3e-0 sc-58c82cf9-1 ihXFUo iPawMI'})
            if price_change_element:
                price_change_color = price_change_element.get('color')
                price_change_value = price_change_element.text.strip().split('%')[0]
                if price_change_color == 'red':
                    price_change_value = '-' + price_change_value

                coin_data['price_change'] = float(price_change_value)

            # Extract market cap
            market_cap_element = coin_stats_div.find('div', string='Market cap').parent.parent.find('dd')
            market_cap_value = market_cap_element.contents[1].strip()
            market_cap_value = convert_to_number(market_cap_value)
            coin_data['market_cap'] = market_cap_value

            # Extract volume (24h)
            volume_24h_element = coin_stats_div.find('div', string='Volume (24h)').parent.parent.find('dd')
            volume_24h_value = volume_24h_element.contents[1].strip()
            volume_24h_value = convert_to_number(volume_24h_value)
            coin_data['volume'] = volume_24h_value

            # Extract Market cap and volume rank
            rank_elements = coin_stats_div.find_all('span', {'class': 'text slider-value rank-value'})
            market_cap_rank_value = int(rank_elements[0].text[1:])
            volume_rank_value = int(rank_elements[1].text[1:])
            coin_data['market_cap_rank'] = market_cap_rank_value
            coin_data['volume_rank'] = volume_rank_value

            # Extract Volume Change
            volume_change_element = coin_stats_div.select_one(
                'div.sc-d1ede7e3-0.sc-cd4f73ae-0.bwRagp.iWXelA.flexBetween:has(dt:-soup-contains("Volume/Market cap (24h)")) dd')
            volume_change_value = convert_to_number(volume_change_element.text.strip())
            coin_data['volume_change'] = volume_change_value

            # Extract circulating supply
            circulating_supply_element = coin_stats_div.find('div', string='Circulating supply').parent.parent.find(
                'dd')
            circulating_supply_value = convert_to_number(circulating_supply_element.text.strip())
            coin_data['circulating_supply'] = circulating_supply_value

            # Extract total supply
            total_supply_element = coin_stats_div.select_one(
                'div.sc-d1ede7e3-0.sc-cd4f73ae-0.bwRagp.iWXelA.flexBetween:has(dt:-soup-contains("Total supply")) dd')
            total_supply_value = convert_to_number(total_supply_element.text.strip())
            coin_data['total_supply'] = total_supply_value

            # Extract Fully diluted market cap
            diluted_market_cap_element = coin_stats_div.select_one(
                'div.sc-d1ede7e3-0.sc-cd4f73ae-0.bwRagp.iWXelA.flexBetween:has(dt:-soup-contains("Fully diluted market cap")) dd')
            diluted_market_cap_value = convert_to_number(diluted_market_cap_element.text.strip())
            coin_data['diluted_market_cap'] = diluted_market_cap_value

            contract = {}
            coin_data['contracts'] = []

            # Extract contracts information
            contracts_elements = coin_stats_div.find_all('div', {
                'class': 'sc-d1ede7e3-0 sc-7f0f401-0 sc-96368265-0 bwRagp gQoblf eBvtSa flexStart'})
            for element in contracts_elements:
                contract_name = element.find('span', {'class': 'sc-71024e3e-0 dEZnuB'}).text.strip()
                address_element = element.find('a')
                contract = {}
                if address_element:
                    address_value = address_element.get('href').split('/')[-1]
                    contract['name'] = contract_name
                    contract['address'] = address_value
                    coin_data['contracts'].append(contract)
            # Extract official links
            official_links_element = coin_stats_div.select(
                '.sc-d1ede7e3-0.jTYLCR:has(span:-soup-contains("Official links")) .sc-d1ede7e3-0.sc-7f0f401-0.gRSwoF.gQoblf')

            official_links = []

            for div in official_links_element:
                link_element = div.find('a')
                if link_element:
                    link_dict = {}
                    link = link_element.get('href')
                    link_text = link_element.text.strip()
                    if link and link_text:
                        link_dict['name'] = link_text
                        link_dict['link'] = link
                        official_links.append(link_dict)

            coin_data['official_links'] = official_links

            # Extract social links
            social_links_element = coin_stats_div.select(
                '.sc-d1ede7e3-0.jTYLCR:has(span:-soup-contains("Socials")) .sc-d1ede7e3-0.sc-7f0f401-0.gRSwoF.gQoblf')

            social_links = []
            for div in social_links_element:
                link_element = div.find('a')
                if link_element:
                    link_dict = {}
                    link = link_element.get('href')
                    link_text = link_element.text.strip()
                    if link and link_text:
                        link_dict['name'] = link_text
                        link_dict['link'] = link
                        social_links.append(link_dict)
            coin_data['socials'] = social_links
        else:
            coin_data['error'] = 'Coin statistics div not found in HTML.'
        return coin_data

    @staticmethod
    def save_to_excel(coin_data, file_name='output.xlsx'):
        with FileLock(LOCK_FILE):
            try:
                try:
                    df_existing = pd.read_excel(EXCEL_FILE)
                except FileNotFoundError:
                    df_existing = pd.DataFrame()

                # Create DataFrame for new data
                df_new = pd.DataFrame([coin_data])

                # Append new data to existing data
                df_combined = pd.concat([df_existing, df_new], ignore_index=True)

                # Write combined data to Excel
                df_combined.to_excel(EXCEL_FILE, index=False)
            except Exception as e:
                print(f"Error writing to Excel: {e}")

