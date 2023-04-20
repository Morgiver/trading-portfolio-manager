import uuid
from types import NoneType
from typing import Union
from datetime import datetime

# Custom Python
from src.portfolio_manager.functions import *

BUY_SIDE = "buy_side"
SELL_SIDE = "sell_side"

ASSET_SPOT   = "asset_spot"
ASSET_FUTURE = "asset_future"

DATE_STR_FORMAT = '%m/%d/%Y, %H:%M:%S'

class Position:
    def __init__(self,
            identifier: str,
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
        self.identifier      = identifier
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

        Parameters:
        bid_price (float): Best price of the Bid side in the orderbook
        ask_price (float): Best price of the Ask side in the orderbook

        Returns:
        float: The Profit and Loss value
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

        Parameters:
        None

        Returns:
        float: The Risk Reward Ratio value
        """
        return round(abs((self.entry - self.target) / (self.entry - self.stoploss)), 2)

    def close(self, close_date: str, bid_price: float, ask_price: float) -> None:
        """
        Closing the position

        Parameters:
        close_date (str): The date when the position is closed, in
                          '%m/%d/%Y, %H:%M:%S' str format
        bid_price (float): Best price of the Bid side in the orderbook
        ask_price (float): Best price of the Ask side in the orderbook

        Returns:
        None
        """
        self.close_date = close_date
        self.pnl = self.get_pnl(bid_price, ask_price)

    def update_by_candle(self, candle: dict) -> None:
        """
        Updating the position with a given Candle

        Will update the Candle pnl and check if stoploss and target have been hit.
        In that case, the position will be closed.

        Parameters:
        candle (dict): A candle containing the Open Date, High Price, Low Price,
                       Close Price and Volume.

        Returns:
        None
        """
        self.pnl = self.get_pnl(candle['Close'], candle['Close'])

        if self.side == BUY_SIDE:
            if self.stoploss > 0.0 and candle['Low'] <= self.stoploss:
                self.close(candle['Date'], self.stoploss, self.stoploss)
            elif self.target > 0.0 and candle['High'] >= self.target:
                self.close(candle['Date'], self.target, self.target)
        elif self.side == SELL_SIDE:
            if self.stoploss > 0.0 and candle['High'] >= self.stoploss:
                self.close(candle['Date'], self.stoploss, self.stoploss)
            elif self.target > 0.0 and candle['Low'] <= self.target:
                self.close(candle['Date'], self.target, self.target)
        else:
            raise Exception(f"Side of Position has to be : '{BUY_SIDE}' or '{SELL_SIDE}' value")

    def update_by_tick(self, tick: dict) -> None:
        """
        Updating the position with a given Tick

        A Tick is a move of two possible price : Bid and Ask prices.
        Bid and Ask are the best prices in the orderbook, they move when the
        orderbook is impacted.

        Using the tick to update a position is much more precise.

        Parameters:
        tick (dict): A Tick containing Date, Bid Price and Ask Price
        """
        self.pnl = self.get_pnl(tick['Bid'], tick['Ask'])

        if self.side == BUY_SIDE:
            if (self.stoploss > 0.0 and tick['Bid'] <= self.stoploss) or (self.target > 0.0 and tick['Bid'] >= self.target):
                self.close(tick['Date'], tick['Bid'], tick['Ask'])
        elif self.side == SELL_SIDE:
            if (self.stoploss > 0.0 and tick['Ask'] >= self.stoploss) or (self.target > 0.0 and tick['Ask'] <= self.target):
                self.close(tick['Date'], tick['Bid'], tick['Ask'])
        else:
            raise Exception(f"Side of Position has to be : '{BUY_SIDE}' or '{SELL_SIDE}' value")

    def update_by_trade(self, trade: dict) -> None:
        """
        Updating the position with a given executed Trade

        A Trade is an executed transaction at a price level. It can be used to
        update the position when we are in lack of information (e.g. can't access,
        to the ticker or candles.).

        Parameters:
        trade (dict): An executed Trade containing Date and Price level at minimum.

        Returns:
        None
        """
        self.pnl = self.get_pnl(trade['Price'], trade['Price'])

        if self.side == BUY_SIDE:
            if self.stoploss > 0.0 and trade['Price'] <= self.stoploss:
                self.close(trade['Date'], self.stoploss, self.stoploss)
            elif self.target > 0.0 and trade['Price'] >= self.target:
                self.close(trade['Date'], self.target, self.target)
        elif self.side == SELL_SIDE:
            if self.stoploss > 0.0 and trade['Price'] >= self.stoploss:
                self.close(trade['Date'], self.stoploss, self.stoploss)
            elif self.target > 0.0 and trade['Price'] <= self.target:
                self.close(trade['Date'], self.target, self.target)
        else:
            raise Exception(f"Side of Position has to be : '{BUY_SIDE}' or '{SELL_SIDE}' value")
