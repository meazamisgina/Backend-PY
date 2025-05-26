class Account:
    def __init__(self,name,balance=0):
        self.name=name
        self.balance=balance
        self.deposits=[]
        self.withdrawals=[]
        self.loan_balance=0
        self.loan_history=[]
        self.transactions=[]
        self.is_frozen=False
        self.minimum_balance=0
        self.closed=False


    def deposit(self,amount):
        if self.closed:
            return "Account is closed."
        if self.is_frozen:
            return "Your account is frozen. You cannot deposit."
        if amount > 0:
            self.balance += amount
            self.deposits.append(amount)
            self.transactions.append(f"Deposited: {amount}")
            return f"Hello {self.name}, {amount} has been deposited in your account, your current balance is {self.balance}"
        else:
            return "Deposit amount must be positive."   



    def withdraw(self,amount):
        if self.closed:
            return f"{self.name} your account is closed."
        if self.is_frozen:
            return f"Hello {self.name} your account is frozen. You cannot withdraw."
        if amount > 0:
            if self.balance - amount < self.minimum_balance or amount > self.balance:
                return f"You can't withdraw because of insufficient funds."
            else: 
                self.balance -= amount
                self.withdrawals.append(amount)
                self.transactions.append(f"Withdrew: {amount}")
                return f"Hello {self.name}, {amount} has been withdrawn from your account, your remaining balance is {self.balance}"
        else:
            return "Withdrawal amount must be positive."



    def transfer_funds(self,amount,recipient):
        if self.closed or recipient.closed:
            return "{One of the accounts is closed.}"
        if self.is_frozen or recipient.is_frozen:
            return "One of the accounts is frozen."
        if amount > 0:
            if self.balance - amount < self.minimum_balance or amount > self.balance:
                return "Insufficient funds for transfer. Balance can't go below minimum balance."
            else:
                self.balance -= amount
                recipient.balance += amount
                self.withdrawals.append(amount)
                recipient.deposits.append(amount)
                self.transactions.append(f"Dear {self.name}, you transferred {amount} to {recipient.name}")
                recipient.transactions.append(f"Dear {recipient.name} you received {amount} from {self.name}")
                return f"Hello {self.name} you transferred {amount} to {recipient.name}. Your current balance is {self.balance}"
        else: 
            return f"Hello {self.name}, transfer amount must be positive."
    


    def get_balance_from_deposits_withdrawals(self):
        total_deposits = sum(self.deposits)
        total_withdrawals = sum(self.withdrawals)
        calculated_balance = total_deposits - total_withdrawals
        return calculated_balance



    def request_loan(self, amount):
        if self.closed:
            return f"{self.name}, your account is closed."
        if self.is_frozen:
            return f"{self.name} your account is frozen. you cannot request loan."
        if amount > 0:
            self.loan_balance += amount
            self.balance += amount
            self.loan_history.append(f"{self.name} you granted the loan of {amount}")
            self.transactions.append(f"{self.name} you takes loan of {amount}")
            return f"{self.name} you granted loan of {amount}. Your current balance is {self.balance}"
        else: 
            return f"Dear {self.name}, loan amount must be positive."



    def repay_loan(self,amount):
        if self.closed:
            return f"{self.name} your account is closed."
        if self.is_frozen:
            return f"{self.name} your account is frozen. You cannot repay loan."
        if amount >0:
            if amount > self.balance:
                return "Insufficient funds to repay loan."
            if amount > self.loan_balance:
                amount = self.loan_balance
            self.loan_balance -= amount
            self.balance -= amount
            self.loan_history.append(f"Hello {self.name}, you repaid {amount} of your loan.")
            self.transactions.append(f"Hello {self.name}, you repaid {amount} of your loan.")
            return f"Dear {self.name}, You have returned {amount} and your remaining loan is {self.loan_balance}. Your current balance is {self.balance}"
        else:
            return "Repayment amount must be positive."  



    def get_loan_statement(self):
        print("Loan History")
        for loan in self.loan_history:
            print(loan)
        return self.loan_history



    def get_statement(self):
        print("Deposits:", self.deposits)
        print("Withdrawals:", self.withdrawals)
        return {"Deposits": self.deposits, "Withdrawals": self.withdrawals}



    def get_full_transaction_history(self):
        print("Full Transaction History:")
        for transaction in self.transactions:
            print(transaction)
        return self.transactions



    def view_account_details(self):
        details = (
            f"Owner: {self.name}\n"
            f"Balance: {self.balance}\n"
            f"Loan: {self.loan_balance}\n"
            f"Minimum Balance: {self.minimum_balance}\n"
            f"Account Frozen: {self.is_frozen}\n"
            f"Account Closed: {self.closed}\n"
        )
        return details



    def change_account_owner_name(self, new_name):
        if self.closed:
            return "Account is closed."
        old_owner=self.name
        self.name = new_name
        self.transactions.append(f"Owner name changed from {self.name} to {new_name}")
        return f"Owner name changed from {old_owner} to {new_name}"



    def interest_calculation(self):
        if self.closed:
            return "Account is closed."
        if self.is_frozen:
            return "Account is frozen. Cannot apply interest."
        interest = self.balance * 0.05
        self.balance += interest
        self.deposits.append(interest)
        self.transactions.append(f"Applied interest is {interest}")
        return f"Hello {self.name}, interest of {interest} is applied to your balance. Your current balance is {self.balance}"



    def freeze_account(self):
        self.is_frozen = True
        self.transactions.append("Account frozen.")
        return "Account has been frozen."
    


    def unfreeze_account(self):
        self.is_frozen = False
        self.transactions.append("Account unfrozen.")
        return "Account has been unfrozen."



    def set_minimum_balance(self, amount):
        if amount >= 0:
            self.minimum_balance = amount
            self.transactions.append(f"Minimum balance set to {amount}")
            return f"Minimum balance set to {amount}"
        else:
            return "Minimum balance must be non-negative."
    


    def close_account(self):
        self.closed = True
        self.balance = 0
        self.loan_balance = 0
        self.transactions.append("Account closed. All balances set to zero.")
        return f"{self.name}, Your account is closed. All balances set to zero and transactions emptied."


acc1= Account("Eyuel", 1000)
acc2= Account("Nehmiya", 2000)
# acc1.is_frozen= True
# acc1.closed= True
print(acc1.deposit(3000))
print(acc1.deposit(0))
print(acc1.withdraw(500))
print(acc1.transfer_funds(200,acc2))
print(acc1.transfer_funds(4000,acc2))
print(acc1.get_balance_from_deposits_withdrawals())
print(acc1.request_loan(5000))
print(acc1.request_loan(0))
print(acc1.repay_loan(0))
print(acc1.repay_loan(4000))
print(acc1.repay_loan(400))
print(acc1.repay_loan(800))
print(acc1.get_loan_statement())
print(acc1.get_statement())
print(acc1.get_full_transaction_history())
print(acc1.view_account_details())
print(acc2.change_account_owner_name('Jossi'))
print(acc1.interest_calculation())
print(acc2.freeze_account())
print(acc2.unfreeze_account())
print(acc1.set_minimum_balance(50))
print(acc2.close_account())