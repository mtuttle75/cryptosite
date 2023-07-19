import requests
from portfolios.models import Asset

def _get_crypto_assets_json():
    url = 'https://api.coincap.io/v2/assets'
    r = requests.get(url)

    try:
        r.raise_for_status()
        return r.json()
    except:
        return None
    
def update_crypto_assets():
    json = _get_crypto_assets_json()
    if json is not None:
        asset_query_set = []

        for crypto_asset in json['data']:
            new_asset = Asset()
            new_asset.name = crypto_asset['name']
            new_asset.symbol = crypto_asset['symbol']
            new_asset.price = crypto_asset['priceUsd']
            new_asset.market_cap = crypto_asset['marketCapUsd']
            new_asset.volume = crypto_asset['volumeUsd24Hr']
            new_asset.change_daily = crypto_asset['changePercent24Hr']
            asset_query_set.append(new_asset)

            Asset.objects.bulk_create(asset_query_set, update_conflicts=True, unique_fields=['name', 'symbol'], update_fields=['price', 'market_cap', 'volume', 'change_daily'],)

        
        