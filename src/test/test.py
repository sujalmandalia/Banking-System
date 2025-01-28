from unittest import TestCase
from application.service import BankAccountApplication, AccountNotFoundError
from domain.model import InsufficientFundsError, AccountClosedError
from decimal import Decimal
from uuid import uuid4


class TestBankAccounts(TestCase):
    def test(self) -> None:
        app = BankAccountApplication()
        with self.assertRaises(AccountNotFoundError):
            app.get_balance(uuid4())

        account1 = app.open_account(
            full_name="John Doe", email_address="john@gmail.com"
        )

        self.assertEqual(app.get_balance(account1), Decimal(0.00))
        app.deposit_funds(
            credit_account_id=account1,
            amount=Decimal("200.00"),
        )

        self.assertEqual(app.get_balance(account1), Decimal("200.00"))

        app.withdraw_funds(
            debit_acount_id=account1,
            amount=Decimal("100.00")
        )

        self.assertEqual(app.get_balance(account1), Decimal("100.00"))

        with self.assertRaises(InsufficientFundsError):
            app.withdraw_funds(
                debit_acount_id=account1,
                amount=Decimal("150.00"),
            )
        self.assertEqual(app.get_balance(account1), Decimal("100.00"))

        app.close_account(account_id=account1)

        with self.assertRaises(AccountClosedError):
            app.deposit_funds(credit_account_id=account1, amount=500)

        with self.assertRaises(AccountClosedError):
            app.withdraw_funds(debit_acount_id=account1, amount=3000)
