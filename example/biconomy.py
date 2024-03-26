from base_exchange import BaseExchange, TickerInfo, Symbol


class Biconomy(BaseExchange):
    """
        docs: https://github.com/BiconomyOfficial/apidocs?tab=readme-ov-file#Getting-Started
    """

    def __init__(self):
        self.id = 'biconomy'
        self.base_url = "https://www.biconomy.com/"
        self.markets = {}  # not really needed, just a stub

    async def fetch_tickers(self) -> dict[str, TickerInfo]:
        data = await self.fetch_data(self.base_url + 'api/v1/tickers')
        # return data
        return self.normalize_data(data)

    def _convert_symbol_to_ccxt(self, symbols: str) -> Symbol:
        if isinstance(symbols, str):
            symbols = symbols.replace("_", "/")
            return symbols
        raise TypeError(f"{symbols} invalid type")

    def normalize_data(self, data: dict) -> dict[Symbol, TickerInfo]:
        normalized_data = {}
        tickers = data.get('ticker', [])
        for ticker in tickers:
            symbol = self._convert_symbol_to_ccxt(ticker.get("symbol", ''))
            normalized_data[symbol] = TickerInfo(last=float(ticker.get("last", 0)),
                                                 baseVolume=float(ticker.get("vol", 0)),
                                                 quoteVolume=0)
        return normalized_data
