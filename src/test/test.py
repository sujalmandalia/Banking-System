from __future__ import annotations

import unittest
from decimal import Decimal
from uuid import uuid4

from ..domain.model import AccountClosedError,InsufficientFundsError
from ..application.service import BankAccountApplication,AccountNotFoundError

class Test(unittest.TestCase):
  def test_application(self):
    app = BankAccountApplication()

    with self.assertRaises(AccountNotFoundError):
      app.get_balance(uuid4())