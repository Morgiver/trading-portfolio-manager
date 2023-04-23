import unittest

# Custom Python
from src.trading_portfolio_manager import *

class TestPositionManager(unittest.TestCase):
    def test_manager_initialization(self):
        manager = PositionManager(100.0, 1)
        self.assertEqual(manager.start_balance, 100.0)
        self.assertEqual(manager.max_positions, 1)

    def test_manager_open(self):
        manager = PositionManager(100.0, 1)
        position = manager.open(1.0, 1.0, '01/01/2000, 00:00:00', BUY_SIDE, 1.1, 0.9)
        self.assertEqual(type(position), Position)
        self.assertEqual(type(position.identifier), uuid.UUID)
        self.assertEqual(len(manager.positions), 1)

    def test_manager_open_max(self):
        manager = PositionManager(100.0, 0)
        position = manager.open(1.0, 1.0, '01/01/2000, 00:00:00', BUY_SIDE, 1.1, 0.9)
        self.assertEqual(type(position), NoneType)
        self.assertEqual(len(manager.positions), 0)

    def test_manager_get_position(self):
        manager = PositionManager(100.0, 1)
        position = manager.open(1.0, 1.0, '01/01/2000, 00:00:00', BUY_SIDE, 1.1, 0.9)
        self.assertEqual(type(manager.get_position(position.identifier)), Position)
        with self.assertRaises(Exception):
            manager.get_position(uuid.uuid4())

    def test_manager_close(self):
        manager = PositionManager(100.0, 2)
        position = manager.open(1.0, 1.0, '01/01/2000, 00:00:00', BUY_SIDE, 1.1, 0.9)
        manager.close(1.01, 1.02, _uuid=position.identifier)
        self.assertEqual(type(position.close_date), str)
        position_two = manager.open(1.0, 1.0, '01/01/2000, 00:00:00', BUY_SIDE, 1.1, 0.9)
        manager.close(1.01, 1.02)
        self.assertEqual(type(position_two.close_date), str)

    def test_manager_close_raising(self):
        manager = PositionManager(100.0, 1)
        position = manager.open(1.0, 1.0, '01/01/2000, 00:00:00', BUY_SIDE, 1.1, 0.9)
        with self.assertRaises(Exception):
            manager.close(1.01, 1.02, _uuid=uuid.uuid4())

    def test_manager_balance(self):
        manager = PositionManager(100.0, 2)
        position = manager.open(1.0, 1.0, '01/01/2000, 00:00:00', BUY_SIDE, 1.1, 0.9)
        manager.close(1.1, 1.11, _uuid=position.identifier)
        position_two = manager.open(1.0, 1.0, '01/01/2000, 00:00:00', BUY_SIDE, 1.1, 0.9)
        position_two.update_by_tick({'Date': '01/01/2000, 00:00:01', 'Bid': 1.09, 'Ask': 1.098})
        self.assertEqual(manager.balance(), manager.start_balance + 10000.0)

    def test_manager_equity(self):
        manager = PositionManager(100.0, 2)
        position = manager.open(1.0, 1.0, '01/01/2000, 00:00:00', BUY_SIDE, 1.1, 0.9)
        manager.close(1.1, 1.11, _uuid=position.identifier)
        position_two = manager.open(1.0, 1.0, '01/01/2000, 00:00:00', BUY_SIDE, 1.1, 0.9)
        position_two.update_by_tick({'Date': '01/01/2000, 00:00:01', 'Bid': 1.09, 'Ask': 1.098})
        self.assertEqual(manager.equity(), manager.start_balance + 19000.0)
