from celery import shared_task
from helpers import CoinMarketCap as cmc
from .models import ScrapedData


@shared_task
def scrape_coin_data(coin_abbr, job_id):
    coin_url = cmc.get_coin_url(coin_abbr)
    html = cmc.scrape(coin_url)
    coin_data = cmc.get_coin_data(html)

    scraped_data = ScrapedData.objects.create(
        job_id=job_id,
        coin_name=coin_abbr,
        price=coin_data['price'],
        price_change=coin_data.get('price_change', 0.0),
        market_cap=coin_data['market_cap'],
        market_cap_rank=coin_data['market_cap_rank'],
        volume=coin_data['volume'],
        volume_rank=coin_data['volume_rank'],
        volume_change=coin_data['volume_change'],
        circulating_supply=coin_data['circulating_supply'],
        total_supply=coin_data['total_supply'],
        diluted_market_cap=coin_data['diluted_market_cap'],
        contracts=coin_data['contracts'],
        official_links=coin_data['official_links'],
        socials=coin_data['socials']
    )
    cmc.save_to_excel(coin_data)
    print("created")

    return coin_data

