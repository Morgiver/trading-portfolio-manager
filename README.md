# Portfolio Manager

This package will provide an API to manage multiple assets on multiple exchange platform on different type of market (Forex, Crypto, Bound, etc.)

## Actual State : Iteration 1 [Working on definition] (see [historic for past iterations](https://github.com/Morgiver/trading-portfolio-manager/blob/main/iterations.md))

The objectives of the Iteration 1 is to enhance the project.

0. Define all new point for the Iteration 1.
1. The Manager should be able to update all position if necessary.
2. The Manager should be considered to be part of a bigger position manager. In other word when we create a position manager it will stack all positions. And if we create a second manager to manage specific position for an exchange or a specific pair, we should be capable to ask to the primary manager to give us a second manager.
3. The Manager should be able to calculate a position in respect of given risk management rules.
