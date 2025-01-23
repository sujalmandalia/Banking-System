from __future__ import annotations
from eventsourcing.domain import Aggregate,event
from decimal import Decimal

class BankAccount(Aggregate):
  @event("Opened")
  def __init__(self,full_name: str,email:str):
    self.full_name = full_name
    self.email = email
    self.balance =  Decimal("0.00")
    self.is_closed = False

  @event('Credited')
  def credit(self,amount:Decimal):
    self.check_account_is_not_closed()
    self.balance += amount

  @event("Debited")
  def debit(self, amount: Decimal):
    self.check_account_is_not_closed()
    self.check_has_sufficient_funds(amount)
    self.balance -= amount

  @event("Closed")
  def close(self) -> None:
    self.is_closed = True

  def check_account_is_not_closed(self):
    if self.is_closed:
      raise AccountClosedError(
                f"Account {self.id} is closed and cannot perform this operation."
            )

    
  def check_has_sufficient_funds(self, amount: Decimal):
    if self.balance < amount:
      raise InsufficientFundsError(
        f"Insufficient funds in account {self.id}. "
        f"Attempted to debit {amount}, but the balance is {self.balance}."
      )
    
class TransactionError(Exception):
    pass

class AccountClosedError(TransactionError):
    pass

class InsufficientFundsError(TransactionError):
    pass