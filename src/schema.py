"""
  {
    "id": "bitcoin",
    "symbol": "btc",
    "name": "Bitcoin",
    "image": "https://assets.coingecko.com/coins/images/1/large/bitcoin.png?1696501400",
    "current_price": 70770,
    "market_cap": 1392444275089,
    "market_cap_rank": 1,
    "fully_diluted_valuation": 1486989851393,
    "total_volume": 47121993496,
    "high_24h": 71419,
    "low_24h": 66811,
    "price_change_24h": 3884.22,
    "price_change_percentage_24h": 5.80722,
    "market_cap_change_24h": 76831203281,
    "market_cap_change_percentage_24h": 5.83995,
    "circulating_supply": 19664781.0,
    "total_supply": 21000000.0,
    "max_supply": 21000000.0,
    "ath": 73738,
    "ath_change_percentage": -3.82897,
    "ath_date": "2024-03-14T07:10:36.635Z",
    "atl": 67.81,
    "atl_change_percentage": 104479.82623,
    "atl_date": "2013-07-06T00:00:00.000Z",
    "roi": null,
    "last_updated": "2024-03-26T11:15:43.525Z"
  }
"""
from pydantic import BaseModel


class MarketCoinGecko(BaseModel):
    """
    для аннотации и лучшей читабельности
    Содержании полей в ответе на эндпоинт
    https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd
    """
    symbol: str
    current_price: float | int
    market_cap: float | int
    market_cap_change_24h: float | int


class DictMarketData(BaseModel):
    """
    для аннотации и лучшей читабельности
    Содержании полей в ответе на эндпоинт
    https://api.coingecko.com/api/v3/coins/bitcoins
    """
    symbol: str
    current_price: dict
    market_cap: dict
    market_cap_change_24h_in_currency: dict


class CoinToCoin(BaseModel):
    """
    для аннотации и лучшей читабельности
    Содержании полей в ответе на эндпоинт
    https://api.coingecko.com/api/v3/coins/bitcoins
    """
    market_data: dict


