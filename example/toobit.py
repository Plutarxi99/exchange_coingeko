from base_exchange import Symbol, TickerInfo, BaseExchange


class Toobit(BaseExchange):
    """
        docs: https://toobit-docs.github.io/apidocs/spot/v1/en/#24hr-ticker-price-change-statistics
    """

    def __init__(self):
        self.id = 'toobit'
        self.base_url = "https://api.toobit.com/"
        self.markets = {}

    async def fetch_tickers(self) -> dict[Symbol, TickerInfo]:
        if not self.markets:
            await self.load_markets()

        result = {}
        for symbol in self.markets.values():
            print(f"Fetching: {symbol}")
            data = await self.fetch_data(self.base_url + 'quote/v1/ticker/24hr?symbol=' + symbol)
            result.update(self.normalize_data(data))
        return result

    async def load_markets(self):
        data = await self.fetch_data(self.base_url + "api/v1/exchangeInfo")
        symbols = data.get("symbols", [])
        for symbol in symbols:
            base = symbol["baseAsset"]
            quote = symbol["quoteAsset"]
            if base and quote:
                self.markets[base + "/" + quote] = base + quote

    def normalize_data(self, data: list) -> dict[Symbol, TickerInfo]:
        normalized_data = {}
        result = data[0]
        symbol = self._convert_symbol_to_ccxt(result.get("s"))
        normalized_data[symbol] = TickerInfo(last=float(result.get("c", 0)),
                                             baseVolume=float(result.get("v", 0)),
                                             quoteVolume=float(result.get("qv", 0)))
        return normalized_data

    def _convert_symbol_to_ccxt(self, symbols: str) -> Symbol:
        if isinstance(symbols, str):
            if symbols.endswith("USDT"):
                symbols = symbols.replace("USDT", "/USDT")
            return symbols
        raise TypeError(f"{symbols} invalid type")
