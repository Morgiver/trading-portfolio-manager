import unittest

# Custom Python
from src.portfolio_manager import *

class TestPosition(unittest.TestCase):
    def test_long_position_initialization(self):
        with self.assertRaises(Exception):
            Position('123abc','01/01/2000, 00:00:00', 1.0, 0.9, 1.1, 1.0, 100000.0, 0.01, BUY_SIDE, "forex", "Oanda", "EURUSD", ASSET_FUTURE)

    def test_short_position_initialization(self):
        with self.assertRaises(Exception):
            Position('123abc','01/01/2000, 00:00:00', 1.0, 1.1, 0.9, 1.0, 100000.0, 0.01, SELL_SIDE, "forex", "Oanda", "EURUSD", ASSET_FUTURE)

    def test_position_pip_size(self):
        p = Position('123abc','01/01/2000, 00:00:00', 1.0, 1.1, 0.9, 1.0, 100000.0, 0.01, BUY_SIDE, "forex", "Oanda", "EURUSD", ASSET_FUTURE)
        self.assertEqual(p.pip_size(), 0.0001)

    def test_position_pip_value(self):
        p = Position('123abc','01/01/2000, 00:00:00', 1.0, 1.1, 0.9, 1.0, 100000.0, 0.01, BUY_SIDE, "forex", "Oanda", "EURUSD", ASSET_FUTURE)
        self.assertEqual(p.pip_value(), 10.0)

    def test_get_pnl(self):
        long = Position('123abc','01/01/2000, 00:00:00', 1.0, 1.1, 0.9, 1.0, 100000.0, 0.01, BUY_SIDE, "forex", "Oanda", "EURUSD", ASSET_FUTURE)
        short = Position('123abc','01/01/2000, 00:00:00', 1.0, 0.9, 1.1, 1.0, 100000.0, 0.01, SELL_SIDE, "forex", "Oanda", "EURUSD", ASSET_FUTURE)
        self.assertEqual(long.get_pnl(1.0001, 1.0001), 10.0)
        self.assertEqual(short.get_pnl(1.0001, 1.0001), -10.0)

    def test_risk_reward_ratio(self):
        long = Position('123abc','01/01/2000, 00:00:00', 1.0, 1.1, 0.9, 1.0, 100000.0, 0.01, BUY_SIDE, "forex", "Oanda", "EURUSD", ASSET_FUTURE)
        short = Position('123abc','01/01/2000, 00:00:00', 1.0, 0.9, 1.1, 1.0, 100000.0, 0.01, SELL_SIDE, "forex", "Oanda", "EURUSD", ASSET_FUTURE)

        self.assertEqual(long.risk_reward_ratio(), 1.0)
        self.assertEqual(short.risk_reward_ratio(), 1.0)

    def test_position_update_by_candle(self):
        p = Position('123abc','01/01/2000, 00:00:00', 1.0, 1.1, 0.9, 1.0, 100000.0, 0.01, BUY_SIDE, "forex", "Oanda", "EURUSD", ASSET_FUTURE)
        self.assertEqual(p.get_pnl(1.0, 1.0), 0.0)
        p.update_by_candle({'Date': '01/01/2000, 00:00:01', 'High': 1.02, 'Low': 1.009, 'Close': 1.01})
        self.assertEqual(p.pnl, 1000.0)
        self.assertEqual(p.close_date, None)

    def test_update_by_candle_raising(self):
        p = Position('123abc','01/01/2000, 00:00:00', 1.0, 1.1, 0.9, 1.0, 100000.0, 0.01, "toto", "forex", "Oanda", "EURUSD", ASSET_FUTURE)
        with self.assertRaises(Exception):
            p.update_by_candle({'Date': '01/01/2000, 00:00:01', 'High': 1.02, 'Low': 1.009, 'Close': 1.01})

    def test_update_by_candle_long_win(self):
        long = Position('123abc','01/01/2000, 00:00:00', 1.0, 1.1, 0.9, 1.0, 100000.0, 0.01, BUY_SIDE, "forex", "Oanda", "EURUSD", ASSET_FUTURE)
        long.update_by_candle({'Date': '01/01/2000, 00:00:01', 'High': 1.15, 'Low': 1.09, 'Close': 1.101})
        self.assertEqual(long.pnl, 10000.0)
        self.assertEqual(long.close_date, '01/01/2000, 00:00:01')

    def test_update_by_candle_long_loss(self):
        long = Position('123abc','01/01/2000, 00:00:00', 1.0, 1.1, 0.9, 1.0, 100000.0, 0.01, BUY_SIDE, "forex", "Oanda", "EURUSD", ASSET_FUTURE)
        long.update_by_candle({'Date': '01/01/2000, 00:00:01', 'High': 1.01, 'Low': 0.89, 'Close': 0.9})
        self.assertEqual(long.pnl, -10000.0)
        self.assertEqual(long.close_date, '01/01/2000, 00:00:01')

    def test_update_by_candle_short_win(self):
        short = Position('123abc','01/01/2000, 00:00:00', 1.0, 0.9, 1.1, 1.0, 100000.0, 0.01, SELL_SIDE, "forex", "Oanda", "EURUSD", ASSET_FUTURE)
        short.update_by_candle({'Date': '01/01/2000, 00:00:01', 'High': 1.01, 'Low': 0.89, 'Close': 0.9})
        self.assertEqual(short.pnl, 10000.0)
        self.assertEqual(short.close_date, '01/01/2000, 00:00:01')

    def test_update_by_candle_short_loss(self):
        short = Position('123abc','01/01/2000, 00:00:00', 1.0, 0.9, 1.1, 1.0, 100000.0, 0.01, SELL_SIDE, "forex", "Oanda", "EURUSD", ASSET_FUTURE)
        short.update_by_candle({'Date': '01/01/2000, 00:00:01', 'High': 1.15, 'Low': 1.09, 'Close': 1.101})
        self.assertEqual(short.pnl, -10000.0)
        self.assertEqual(short.close_date, '01/01/2000, 00:00:01')
