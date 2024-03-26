import asyncio
from base_exchange import BaseExchange, Symbol, TickerInfo
from src.mixin import MyExchangeMixin
from src.schema import MarketCoinGecko, CoinToCoin, DictMarketData


class MyExchange(MyExchangeMixin, BaseExchange):
    """
    Класс для отрисовки в нужном формата полученные данные от эндпоинта API CoinGecko

    ...

    Атрибуты
    ---------
    coin_is_rel_coin: bool | None = False
        {
        "BTC/USDT": TickerInfo(last=57000, baseVolume=11328, quoteVolume=3456789),
        }

    ...

    coin_is_rel_coi: bool | None = True
        {
        "ETH/BTC": TickerInfo(last=4026, baseVolume=4567, quoteVolume=0)
        }
    """

    def __init__(self, cur: str | None = None, coin: str | None = None, coins: tuple | None = None,
                 coin_is_rel_coin: bool | None = False):
        super().__init__(cur, coin, coin_is_rel_coin)
        self.id = "coingecko"  # exchange name as in coingecko
        self.base_url = "https://api.coingecko.com/api/v3/"  # base url for API requests
        self.markets = {}  # todo all trading pairs (sometimes it's not needed)

    def normalize_data(self, data: dict | list) -> dict[Symbol, TickerInfo]:
        """
        Метод для изъятия из сырых данных нужных для дальнейшего их использование
        :param data: список или словарь. Зависит от эндпоинта
        :return: словарь из указанных значений

        ...

        Пример возвращения данных
        {
        'BTC/USD': TickerInfo(last=70119, baseVolume=4826312161, quoteVolume=1372816952082)
          }

        """
        # данные полученные от эндпоинта coins/
        if isinstance(data, dict):
            normal_dict = {}
            # оборачиваем в схему полученные данные
            dict_value_coins = DictMarketData(symbol=data['symbol'], **data['market_data'])
            # получаемые нужные словари
            current_price: dict[str, int | float] = (
                dict_value_coins.current_price)
            market_cap: dict[str, int | float] = (
                dict_value_coins.market_cap)
            market_cap_change_24h_in_currency: dict[str, int | float] = (
                dict_value_coins.market_cap_change_24h_in_currency)
            # получаем список всех валют ввиду аббревиатур
            list_coins = list(current_price.keys())
            # делаем итерацию и используем имена валюта для получения значения
            for symbol in list_coins:
                symbol_double = self._convert_symbol_to_ccxt(base_symbol=symbol, quoted_symbol=dict_value_coins.symbol)
                normal_dict[symbol_double] = TickerInfo(
                    last=current_price.get(symbol),
                    baseVolume=market_cap.get(symbol),
                    quoteVolume=market_cap_change_24h_in_currency.get(symbol)
                )
        # данные полученные от эндпоинта coins/markets
        elif isinstance(data, list):
            normal_dict = {}
            # делаем итерацию по полученным данным
            for value_coin in data:
                symbol = self._convert_symbol_to_ccxt(base_symbol=value_coin['symbol'], quoted_symbol=self.cur)
                given_value = MarketCoinGecko(**value_coin)
                normal_dict[symbol] = TickerInfo(
                    last=given_value.current_price,
                    baseVolume=given_value.market_cap_change_24h,
                    quoteVolume=given_value.market_cap
                )
        else:
            normal_dict = {}
        return normal_dict

    async def fetch_tickers(self) -> dict[Symbol, TickerInfo]:
        url_api = self._check_get_url()
        data = await self.fetch_data(self.base_url + url_api)
        return self.normalize_data(data)

    async def load_markets(self):
        ...  # todo if needed!
