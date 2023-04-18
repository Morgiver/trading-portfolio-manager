# Custom Python
from src.portfolio_manager.functions import *

BUY_SIDE = "buy_side"
SELL_SIDE = "sell_side"

ASSET_SPOT   = "asset_spot"
ASSET_FUTURE = "asset_future"

class Position:
    def __init__(self,
            open_date: str,
            entry: float,
            target: float = -1.0,
            stoploss: float = -1.0,
            lot_size: float = 1.0,
            contract_size: float = 100000.0,
            pip_size_factor: float = 0.01,
            side: str = BUY_SIDE,
            market: str = "Forex",
            exchange: str = "Oanda",
            pair: str = "EURUSD",
            _type: str = ASSET_FUTURE) -> None:
        self.market          = market
        self.exchange        = exchange
        self.pair            = pair
        self.entry           = entry
        self.stoploss        = stoploss
        self.target          = target
        self.lot_size        = lot_size
        self.contract_size   = contract_size
        self.pip_size_factor = pip_size_factor
        self.side            = side
        self.pnl             = 0
        self.type            = _type
        self.open_date       = open_date
        self.close_date      = None

        if self.side == BUY_SIDE and self.stoploss > 0.0 and self.target > 0.0 and self.stoploss > self.target:
            raise Exception("Stoploss cannot be bigger than target in Long Side")
        elif self.side == SELL_SIDE and self.stoploss > 0.0 and self.target > 0.0 and self.stoploss < self.target:
            raise Exception("Stoploss cannot be lower than target in Short Side")

    def pip_size(self) -> float:
        """
        See pip_size() method in functions.py
        """
        return pip_size(self.pip_size_factor)

    def pip_value(self) -> float:
        """
        See pip_value() method in functions.py
        """
        return pip_value(self.entry, self.pip_size(), self.lot_size, self.contract_size)

    def get_pnl(self, bid_price: float, ask_price: float) -> float:
        """
        Calculate and returning the actual profit and loss
        """
        pip_value = self.pip_value()

        if self.side == BUY_SIDE:
            return round(((bid_price - self.entry) / self.pip_size()) * pip_value, 5)

        if self.side == SELL_SIDE:
            return round(((self.entry - ask_price) / self.pip_size()) * pip_value, 5)

    def risk_reward_ratio(self) -> float:
        """
        Calculate the risk reward ratio.

        This calculates how many times one wins the risk.
        A ratio greater than 1.0 means that a loss will be recovered with a single trade.
        A ratio smaller than 1.0 will require several winning trades to recoup our losses.
        """
        return round(abs((self.entry - self.target) / (self.entry - self.stoploss)), 2)

    def update_by_candle(self, candle) -> None:
        """
        Updating the position with a given Candle

        Will update the Candle pnl and check if stoploss and target have been hit.
        In that case, the position will be closed.
        """
        self.pnl = self.get_pnl(candle['Close'], candle['Close'])

        if self.side == BUY_SIDE:
            if self.stoploss > 0.0 and candle['Low'] <= self.stoploss:
                self.close_date = candle['Date']
                self.pnl = self.get_pnl(self.stoploss, self.stoploss)
            elif self.target > 0.0 and candle['High'] >= self.target:
                self.close_date = candle['Date']
                self.pnl = self.get_pnl(self.target, self.target)
        elif self.side == SELL_SIDE:
            if self.stoploss > 0.0 and candle['High'] >= self.stoploss:
                self.close_date = candle['Date']
                self.pnl = self.get_pnl(self.stoploss, self.stoploss)
            elif self.target > 0.0 and candle['Low'] <= self.target:
                self.close_date = candle['Date']
                self.pnl = self.get_pnl(self.target, self.target)
        else:
            raise Exception(f"Side has to be : 'buy' or 'sell' value")

    def update_by_tick(self, tick):
        # TODO:
        pass

    def update_by_trade(self, trade):
        # TODO:
        pass
