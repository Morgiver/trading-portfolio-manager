# Portfolio Manager

This package will provide an API to manage multiple assets on multiple exchange platform on different type of market (Forex, Crypto, Bound, etc.)

### Actual State : Iteration 0

The objectives of the Iteration 0 is to build good foundation to have a easy maintainable project.

1. Have multiple unit test in the beginning
2. Structure different type of market
3. Structure different type of trading (Spot, Futures, etc.)
4. Build a base class for Position, it will contain Open Date, Entry, Target, Stoploss, Lot Size, Position Side (long or short), Market type, Exchange Platform, Pair, Pip Size and Trading type
5. The position have to be build correctly, if there's a target and a stoploss they will be correctly set or raise an exception.
6. The position will calculate the pip value.
7. The position will calculate it's pnl and store it.
8. The position will calculate it's risk reward ratio if there's a stop and a target.
9. The position should be updated by different way : receiving an entire candle, receiving the last tick, or receiving the last trade executed.
10. All position should be managed by a PositionManager
11. The manager will be build with a max of positions, a starting balance and a list to stack all positions.
12. The manager should be capable to open and close a position
13. The Manager should be capable to return the actual balance by calculating all the pnl
14. The Manager should be capable to update all position if necessary.
15. The Manager should be considered to be part of a bigger position manager. In other word when we create a position manager it will stack all positions. And if we create a second manager to manage specific position for an exchange or a specific pair, we should be capable to ask to the primary manager to give us a second manager.
16. The Manager should be capable to calculate a position in respect of given risk management rules.
