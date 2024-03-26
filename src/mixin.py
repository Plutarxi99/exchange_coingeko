from base_exchange import Symbol


class MyExchangeMixin:
    def __init__(self,
                 cur: str | None = None,
                 coin: str | None = None,
                 coin_is_rel_coin: bool | None = False
                 ):
        """
        :param cur: валюта, можно указать, если не указана используется usd
        :param coin: coin, можно указать, если не указана используется bitcoin
        :param coin_is_rel_coin: флаг, если указать True, то используется отношение coin-to-coin, иначе currency-to-coin
        """
        self.cur = cur  # currency in relation to all coin
        self.coin = coin  # coin in relation to all coin
        self.coin_is_rel_coin = coin_is_rel_coin  # the choice between methods of currency-to-coin or coin-to-coin relations

    def _convert_symbol_to_ccxt(self, base_symbol: str, quoted_symbol: str) -> Symbol:
        """
        Преобразование в полученные строки в пару базовой и конвертируемой валюты
        :param base_symbol: название валюты за которую будут покупать вторую
        :param quoted_symbol: название валюты, которую будут покупать
        :return: USD/BTC
        """
        symbol_str = f"{base_symbol}/{quoted_symbol}".upper()
        symbol = Symbol(symbol_str)
        return symbol

    def _check_get_url(self):
        # if stay flag coin_is_rel_coin False
        if not self.coin_is_rel_coin:
            # coin-one to cur-one
            if self.cur and self.coin:
                url_api = "coins/markets?vs_currency={0}&ids={1}".format(
                    self.cur, self.coin
                )
            # coin-many to cur-one
            elif self.cur and not self.coin:
                url_api = "coins/markets?vs_currency={0}".format(
                    self.cur
                )
            # coin-many to default cur='usd'
            else:
                self.cur = 'usd'
                url_api = "coins/markets?vs_currency={0}".format(
                    self.cur
                )
        # if stay flag coin_is_rel_coin True
        else:
            # coin-choise to coin-many
            if self.coin:
                url_api = "coins/{0}".format(
                    self.coin
                )
            # default coin='bitcoin' to coin-many
            else:
                self.coin = 'bitcoin'
                url_api = "coins/{0}".format(
                    self.coin
                )
        return url_api
