"""
    Description: For an exchange, get all trading pairs, their latest prices and trading volume for 24 hours
    Task:
        Create a class inherited from the BaseExchange class.
        Write the implementation of the methods and fill in the required fields (marked as "todo")
    Note:
        Feel free to add another internal methods.
        It is important that the example from the main function runs without errors
    The flow looks like this:
        1. Request data from the exchange
        2. We bring the ticker to the general format
        3. We extract from the ticker properties the last price,
            the 24-hour trading volume of the base currency
            and the 24-hour trading volume of the quoted currency.
            (at least one of the volumes is required)
        4. Return the structure in the format:
            {
                "BTC/USDT": TickerInfo(last=57000, baseVolume=11328, quoteVolume=3456789),
                "ETH/BTC": TickerInfo(last=4026, baseVolume=4567, quoteVolume=0)
            }
Описание: Для обмена получите информацию обо всех торговых парах, их последних ценах и объеме торгов за 24 часа
 Задача:
 Создайте класс, унаследованный от класса BaseExchange.
 Напишите реализацию методов и заполните необходимые поля (помеченные как "todo")
 Примечание:
 Смело добавляйте еще внутренние методы.
 Важно, чтобы пример из основной функции выполнялся без ошибок
 Поток выглядит следующим образом:
 1. Запрашиваем данные с биржи
 2. Приводим тикер к общему формату
 3. Извлекаем из свойств тикера последнюю цену,
24-часовой торговый объем базовой валюты
и 24-часовой торговый объем котируемой валюты.
 (требуется хотя бы один из объемов)
 4. Возвращаем структуру в формате:
"""

import asyncio

from base_exchange import TickerInfo, Symbol
from example.biconomy import Biconomy
from example.toobit import Toobit
from src.my_exchange import MyExchange


async def main():
    """
        Test yourself here. Verify prices and volumes here: https://www.coingecko.com/
    """
    exchange = MyExchange()
    # exchange = Biconomy()
    # exchange = Toobit()
    await exchange.load_markets()
    tickers = await exchange.fetch_tickers()
    for symbol, prop in tickers.items():
        print(symbol, prop)

    assert isinstance(tickers, dict)
    for symbol, prop in tickers.items():
        assert isinstance(prop, TickerInfo)
        assert isinstance(symbol, Symbol)


if __name__ == "__main__":
    asyncio.run(main())
