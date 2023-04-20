class PositionManager:
    def __init__(self,
            start_balance: float = 100.0,
            max_positions: int = 1) -> None:
        self.max_positions    = max_positions
        self.start_balance    = start_balance
        self.position_indexer = {}
        self.positions        = []

    def open(self, entry: float, lot_size: float, date: str, side: str = BUY_SIDE, target: Union[float, NoneType] = None, stoploss: Union[float, NoneType], identifier: Union[str, NoneType] = None) -> None:
        if len(self.position) < self.max_positions:
            if not identifier:
                identifier = uuid.uuid4()

            while identifier in self.position_indexer:
                identifier = uuid.uuid4()

            self.position.append(Position(identifier, date, entry, target, stoploss, lot_size, side=side))
            self.position_indexer[identifier] = len(self.positions) - 1

    def close(self, bid_price: float, ask_price: float, identifier: Union[str, NoneType] = None) -> None:
        if identifier is not None:
            # Close one identified position
            _id = self.position_indexer[identifier]
            self.positions[_id].close(datetime.fromtimestamp(datetime.now()).strftime(DATE_STR_FORMAT), bid_price, ask_price)
        else:
            # Close all opened positions
            for position in self.positions:
                position.close(datetime.fromtimestamp(datetime.now()).strftime(DATE_STR_FORMAT), bid_price, ask_price)

    def balance(self, incl: bool = False) -> float:
        balance = self.start_balance

        for position in self.positions:
            if (not incl and position.close_date is not None) or incl:
                balance += position.pnl

        return balance
