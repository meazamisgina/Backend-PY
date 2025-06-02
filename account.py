# from datetime import datetime

class Transaction:
    def __init__(self, amount, narration, transaction_type):
        self.date_time = datetime.now()
        self.amount = amount
        self.narration = narration
        self.transaction_type = transaction_type  

    def __str__(self):
        return f"{self.date_time.strftime('%Y-%m-%d %H:%M:%S')} | {self.transaction_type.title()}: {self.narration} | Amount: {self.amount}"

class Account:
    def __init__(self, account_number, owner, min_balance=0):
        self.__account_number = account_number  
        self.__owner = owner                   
        self.__balance = 0                      
        self.__is_frozen = False                
        self.__min_balance = min_balance        
        self.__loan = 0                         
        self.transactions = []                  


    def get_account_number(self):
        return self.__account_number

    def get_owner(self):
        return self.__owner

    def set_owner(self, new_owner):
        self.__owner = new_owner

    def is_frozen(self):
        return self.__is_frozen

    def deposit(self, amount):
        if self.__is_frozen:
            return "Account is frozen. Cannot deposit."
        if amount <= 0:
            return "Deposit must be positive."
        self.__balance += amount
        txn = Transaction(amount, "Deposit to account", "deposit")
        self.transactions.append(txn)
        return f"Deposited {amount}. New balance: {self.__balance}"


    def withdraw(self, amount):
        if self.__is_frozen:
            return "Account is frozen. Cannot withdraw."
        if amount <= 0:
            return "Withdrawal amount must be positive."
        if self.__balance - amount < self.__min_balance:
            return "Insufficient funds"
        self.__balance -= amount
        txn = Transaction(amount, "Withdrawal from account", "withdrawal")
        self.transactions.append(txn)
        return f"Withdrew {amount}. New balance: {self.__balance}"


    def transfer_funds(self, target_account, amount):
        if self.__is_frozen:
            return "Account is frozen. Cannot transfer."
        if amount <= 0:
            return "Transfer amount must be positive."
        if self.__balance - amount < self.__min_balance:
            return "Insufficient funds"
        if not isinstance(target_account, Account):
            return "Invalid target account."
        self.__balance -= amount
        target_account.__balance += amount
        txn = Transaction(amount, f"Transfer to {target_account.get_account_number()}", "transfer out")
        self.transactions.append(txn)
        target_txn = Transaction(amount, f"Transfer from {self.get_account_number()}", "transfer in")
        target_account.transactions.append(target_txn)
        return f"Transferred {amount} to account {target_account.get_account_number()}. Your new balance is {self.__balance}."

    def get_balance(self):
        balance = 0
        for txn in self.transactions:
            if txn.transaction_type in ["deposit", "transfer in", "loan disbursed"]:
                balance += txn.amount
            elif txn.transaction_type in ["withdrawal", "transfer out", "loan repayment"]:
                balance -= txn.amount
        return balance


    def request_loan(self, amount):
        if self.__is_frozen:
            return "Account is frozen. Cannot request loan."
        if amount <= 0:
            return "Loan amount must be positive."
        self.__loan += amount
        self.__balance += amount
        txn = Transaction(amount, "Loan disbursed", "loan disbursed")
        self.transactions.append(txn)
        return f"Loan of {amount} granted. Current loan balance: {self.__loan}"


    def repay_loan(self, amount):
        if self.__is_frozen:
            return "Account is frozen. Cannot repay loan."
        if amount > 0:
            if self.__balance - amount < self.__min_balance or amount > self.__balance:
                return "Insufficient funds to repay the loan."
            if amount > self.__loan:
                amount=self.__loan
            self.__loan -= amount
            self.__balance -= amount
            txn = Transaction(amount, "Loan repayment", "loan repayment")
            self.transactions.append(txn)
            return f"Repaid {amount}. Remaining loan: {self.__loan}"
        else:
            return "Repayment amount must be positive."
            

    def view_account_details(self):
        return f"Account Number: {self.__account_number}\n Owner: {self.__owner}\n Current Balance: {self.get_balance()} \n Loan Balance: {self.__loan}"


    def change_account_owner(self, new_owner):
        self.set_owner(new_owner)
        return f"Account owner name changed to {self.__owner}"


    def account_statement(self):
        print(f"--- Account Statement for {self.__owner} ---")
        for txn in self.transactions:
            print(txn)
        print(f"Current Balance: {self.get_balance()}")


    def apply_interest(self, rate=0.05):
        if self.__is_frozen:
            return "Account is frozen. Cannot apply interest."
        interest = self.__balance * rate
        self.__balance += interest
        txn = Transaction(interest, f"Interest applied at {rate*100}%", "interest")
        self.transactions.append(txn)
        return f"Interest of {interest} applied. New balance: {self.__balance}"

    def freeze_account(self):
        self.__is_frozen = True
        return "Account has been frozen."

    def unfreeze_account(self):
        self.__is_frozen = False
        return "Account has been unfrozen."


    def set_min_balance(self, amount):
        if amount < 0:
            return "Minimum balance cannot be negative."
        self.__min_balance = amount
        return f"Minimum balance set to {self.__min_balance}"


    def close_account(self):
        self.__balance = 0
        self.transactions.clear()
        self.__loan = 0
        return "Account closed. All balances set to zero and transactions cleared." 