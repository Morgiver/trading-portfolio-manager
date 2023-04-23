def pip_size(factor: float = 0.01) -> float:
    """
    Calculate the size of a pip

    A pip is the smallest whole unit price move.
    For example the EURUSD pair has a pip size at 0.0001, so every time
    the price moves by one pip, the price has moved by a value of 0.0001.
    There's another value called pipette, it's a half of a pip (0.00005).

    In most forex pairs one pip is a movement in the fourth decimal place (0.0001).
    This represent 1% / 100. 100 is the factor (some pairs have another factor).

    Parameters:
    factor (float): Dividing factor

    Returns:
    float: The size of the pip
    """
    return round((1.0 / 100.0) * factor, 5)

def pip_value(price: float, pip_size: float, lot_size: float, contract_size: float) -> float:
    """
    Calculate the pip value.

    The value of a pip changes depending on your position size, here the "lot_size",
    and the entry level price of your position.
    The pip value is used to easely calculate the profit and loss of your position.

    Parameters:
    price (float): The actual price of market.
    pip_size (float): The size of a pip for the market.
    lot_size (float): Size of the lot (or volume) for the position.
    contract_size (float): Size of the contract for 1.0 lot in dollars.

    Returns:
    float: The value of a pip.
    """
    return (pip_size / price) * (lot_size * contract_size)
