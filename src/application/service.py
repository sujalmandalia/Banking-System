from __future__ import annotations

from typing import TYPE_CHECKING
from eventsourcing.domain import OriginatorVersionError
from eventsourcing.application import Application, AggregateNotFoundError
from domain.model import BankAccount
from config.dbconfig import cursor

if TYPE_CHECKING:
    from decimal import Decimal
    from uuid import UUID


class BankAccountApplication(Application):
    def open_account(self, full_name: str, email_address: str) -> UUID:
        account = BankAccount(
            full_name=full_name,
            email=email_address,
        )
        self.save(account)
        return account.id

    def get_account(self, account_id: UUID) -> BankAccount:
        try:
            # print(self.repository.get(account_id))
            return self.repository.get(account_id)
        except AggregateNotFoundError:
            raise AccountNotFoundError(
                f"Account with ID {account_id} not found."
            ) from None
        except OriginatorVersionError as ve:
            print(f"Version error for account {account_id}: {ve}")
            raise RuntimeError(
                f"A version conflict occurred while {account_id}."
            ) from ve
        except Exception as e:
            print(f"Unexpected error while fetching account {account_id}: {e}")
            raise RuntimeError(
                f"An unexpected error occurred account {account_id}."
            ) from e

    def get_current_state_account(self, account_id):
        query = """SELECT
    originator_id,
    SUM(
        CASE
            WHEN topic = 'domain.model:BankAccount.Credited' THEN (
                (convert_from(state, 'UTF8')::jsonb)->'amount'->>'_data_'
            )::NUMERIC
            WHEN topic = 'domain.model:BankAccount.Debited' THEN -(
                (convert_from(state, 'UTF8')::jsonb)->'amount'->>'_data_'
            )::NUMERIC
            WHEN topic = 'domain.model:BankAccount.Opened' THEN 0
        END
    ) as balance
    FROM bankaccountapplication_events
    WHERE originator_id = %s
    group by originator_id;"""
        cursor.execute(query, (str(account_id),))
        account = cursor.fetchone()
        if account:
            return account
        else:
            raise Exception("Account not found")

    def get_balance(self, account_id: UUID) -> Decimal:
        # For SQL Query
        account = self.get_current_state_account(account_id=account_id)
        balance = account[-1]
        return balance
        # For repository
        # account = self.get_account(account_id)
        # return account.balance

    def deposit_funds(self, credit_account_id: UUID, amount: Decimal) -> None:
        account = self.get_account(credit_account_id)
        account.credit(amount)
        self.save(account)

    def withdraw_funds(self, debit_acount_id, amount: Decimal) -> None:
        account = self.get_account(debit_acount_id)
        account.debit(amount)
        self.save(account)

    def transfer_funds(
        self, debit_account_id: UUID, credit_account_id: UUID, amount: Decimal
    ) -> None:
        debit_account = self.get_account(debit_account_id)
        credit_account = self.get_account(credit_account_id)
        debit_account.debit(amount)
        credit_account.credit(amount)
        self.save(debit_account, credit_account)

    def close_account(self, account_id: UUID) -> None:
        account = self.get_account(account_id)
        account.close()
        self.save(account)

    # def get_all_accounts(self):
    #     query = """
    #         SELECT
    #         originator_id,
    #         SUM(
    #         CASE
    #             WHEN topic = 'domain.model:BankAccount.Credited' THEN (
    #                 (convert_from(state, 'UTF8')::jsonb)->'amount'->>'_data_'
    #             )::NUMERIC
    #             WHEN topic = 'domain.model:BankAccount.Debited' THEN -(
    #                 (convert_from(state, 'UTF8')::jsonb)->'amount'->>'_data_'
    #             )::NUMERIC
    #             WHEN topic = 'domain.model:BankAccount.Opened' THEN 0
    #         END
    #     ) as balance,
    #         CASE
    #         WHEN COUNT(
    #             CASE WHEN topic = 'domain.model:BankAccount.Closed' THEN 1
    #             END
    #         ) > 0 THEN 'closed'
    #         ELSE 'opened'
    #     END AS status
    #     FROM bankaccountapplication_events
    #     group by originator_id
    #     """
    #     cursor.execute(query)
    #     result = cursor.fetchall()
    #     for item in result:
    #         print(f"Account Number:{item[0]}")
    #         print(f"Account Balance:{item[1]}")
    #         print(f"Account Status:{item[2]}")
    #         print("---------------------------")

    def get_all_accounts(self):
        query = """
        select distinct originator_id
        from bankaccountapplication_events;
        """
        cursor.execute(query)
        aggregateIds = cursor.fetchall()
        for aggregates in aggregateIds:
            account_id = aggregates[0]
            account_info = self.repository.get(account_id)
            account_balance = account_info.balance
            # account_status = account_info.is_closed
            print(f"The account {account_id} and balance is {account_balance}")
            print("----------------------------------------------------------")


class AccountNotFoundError(Exception):
    pass
