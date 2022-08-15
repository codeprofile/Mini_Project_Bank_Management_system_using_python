from abc import ABC, abstractmethod
from constants import *


class Bank:
    Accounts = []
    __min_balance = MINIMUM_BALANCE
    _depo_transcation_count = 0
    _withdraw_transcation_count = 0

    def create_acc(self, pan: str, aadhar: str, minimum_balance: float):
        if minimum_balance < Bank.__min_balance:
            print("Minimum Balance for account Opening is 1000 Rupees!!!")
            return False
        account_id = "123456"
        acc = {account_id: {"pan": pan, "aadhar": aadhar, "balance": minimum_balance}}
        Bank.Accounts.append(acc)
        print(f"Account is successfully created with Account_id as {account_id} for pan {pan}")
        return True

    @staticmethod
    def deposit(account_id, amount):
        acc_present = [index for index, acc in enumerate(Bank.Accounts) if list(acc.keys())[0] == account_id]
        if len(acc_present) > 0:
            print(
                f"Current Balance Details with Bank for account_id : {account_id} Balance is {Bank.Accounts[acc_present[0]][account_id]['balance']} ")
            Bank.Accounts[acc_present[0]][account_id]['balance'] = Bank.Accounts[acc_present[0]][account_id][
                                                                       'balance'] + amount
            print(
                f"After deposit Balance Details with Bank for account_id : {account_id} Balance is {Bank.Accounts[acc_present[0]][account_id]['balance']} ")
            Bank._depo_transcation_count += 1
            return True
        else:
            print(f"account_id : {account_id} entered is not present in the system .Please Check again!!")
            return False

    @staticmethod
    def withdraw(account_id, amount):
        acc_present = [index for index, acc in enumerate(Bank.Accounts) if list(acc.keys())[0] == account_id]
        if len(acc_present) > 0:
            if Bank.Accounts[acc_present[0]][account_id]['balance'] > Bank.__min_balance:
                print(
                    f"Current Balance Details with Bank for account_id : {account_id} Balance is {Bank.Accounts[acc_present[0]][account_id]['balance']} ")
                Bank.Accounts[acc_present[0]][account_id]['balance'] = Bank.Accounts[acc_present[0]][account_id][
                                                                           'balance'] - amount
                print(
                    f"After withdrawal Balance Details with Bank for account_id : {account_id} Balance is {Bank.Accounts[acc_present[0]][account_id]['balance']} ")
                Bank._withdraw_transcation_count += 1
                return True
            else:
                print(f"Insufficient balance for withdrawal with Bank for account_id : {account_id} \
                Balance is {Bank.Accounts[acc_present[0]][account_id]['balance']} ")
                Bank._withdraw_transcation_count += 1
                return True
        else:
            print(f"account_id : {account_id} entered is not present in the system .Please Check again!!")
            return False

    @classmethod
    def stats_transaction(self):
        """
        Basic stats of the today .
        """
        print("*" * 20, "Report Start", "*" * 20)
        print("===", "Details", "===", ">>>>", "===", "stats", "===")
        print("No. of unique accounts", " >>>> ", f"{len(Bank.Accounts)}")
        print("Total No. of transaction", " >>>> " f"{Bank._withdraw_transcation_count + Bank._depo_transcation_count}")
        print("*" * 20, "Report End", "*" * 20)

    def _apply_interest(self, acc):
        interest_rate = 0.04
        account_id = list(acc.keys())[0]
        acc[account_id]["balance"] = acc[account_id]["balance"] * interest_rate + (acc[account_id]["balance"] * interest_rate)
        return acc

    def apply_interest_on_all_acc(self):
        account_data = list(map(self._apply_interest, Bank.Accounts))
        Bank.Accounts = account_data
        print("Successfully applied interest rate on all accounts")
        return True

    @classmethod
    def account_info(self, account_id):
        """
        Basic stats of the today .
        """
        for index, acc in enumerate(Bank.Accounts):
            if list(acc.keys())[0] == account_id:
                print("*" * 20)
                print(f"Printing Account details of account_id {account_id}")
                print("*" * 20)
                print(
                    f"PAN Card associated  with account_id {account_id} is : {Bank.Accounts[index][account_id]['pan']}")
                print(
                    f"Aadhar associated with account_id {account_id} is : {Bank.Accounts[index][account_id]['aadhar']}")
                print(
                    f"Current Balance with account_id {account_id} is : {Bank.Accounts[index][account_id]['balance']}")
                return True
        else:
            print(f"Seems like account_id {account_id} is wrongly Provided. please try again !!!")
            return False


class Account(ABC):
    def __init__(self, user_name: str, password: str):
        self.user_name = user_name
        self.password = password

    @abstractmethod
    def signup(self):
        pass

    @abstractmethod
    def login(self):
        pass

    @abstractmethod
    def logout(self):
        pass


class Bank_System(Account):
    def __init__(self, user_name: str = None, password: str = None, user_type: int = 0):
        """we check if the user present SYSTEM_LOGIN list .
        if not present we proceed with sign up : create user functionality"""
        # user_type for managing customer and bank official as different user
        self.account_type = user_type
        # SYSTEM_ACCOUNTS : managing user in Bank System DB as in list here
        if user_name in SYSTEM_ACCOUNTS:
            # if user is present in SYSTEM_ACCOUNTS we directly proceed with user login .
            # considering user is done with sign-up (user-creation) process
            super().__init__(user_name, password)
            self.login()
        else:
            print("Sign-Up to Create Account")
            # if user is not present in SYSTEM_ACCOUNTS .
            # we start with user-creation i.e signup process and redirect user into the account with auto-login
            self.signup()
            print("*" * 5, "Re-directing to Login", "*" * 5)
            self.login()

    def signup(self):
        print("Creating account for you !!!!")
        print("Select user type from below Option : ")
        print("1.Customer", "2.Bank official", sep="\n")
        self.account_type = int(input("enter user type here : "))
        while True:
            self.user_name = input("enter user_name  : ")
            # space/white_space character not allowed in username
            if " " in self.user_name:
                print("Space is not allowed while in username . Please Try again !! ")
                continue
            password = input("enter password  : ")
            confirm_password = input("re-enter password to confirm : ")
            if password == confirm_password:
                self.password = password
                print(f"Successfully created account with username as : {self.user_name}")
                DUMMY_CREDENTIALS.append({"user_name": self.user_name, "password": password})
                break
            else:
                print("entered password is not matching. Please try again creating an account!!!")
                continue

    def verify_acc(func):
        def verification(self):
            for acc in DUMMY_CREDENTIALS:
                if acc["user_name"] == self.user_name and self.password == acc["password"]:
                    func(self)
            else:
                print("Functionality can not be access without correct credentials. Please Login")

        return verification

    @verify_acc
    def login(self):
        print(f"Successfully Logged in {self.user_name}")
        LOGIN_DETAILS.append(self.user_name)
        b = Bank()
        if self.account_type == 1:
            while True:
                print("1.Create Savings Account", "2.Deposit", "3.Withdraw", "4.Quit/Logout", sep="\n")
                selected_menu = int(input("Select one from the above Options : "))
                if selected_menu == 1:
                    print("We require pan and aadhar no. to proceed with Account Creation .")
                    while True:
                        pan_no = input("enter pan number : ")
                        aadhar_no = input("enter aadhar number : ")
                        min_bal = float(input("enter initial opening amount : "))
                        if not b.create_acc(pan=pan_no, aadhar=aadhar_no, minimum_balance=min_bal):
                            print("Trying to create fresh account again with!!!")
                            continue
                        break
                elif selected_menu == 2:
                    print("Deposit Process is getting Initiated !!")
                    while True:
                        account_id = input("enter account_id to deposit : ")
                        amount = float(input("enter amount to deposit : "))
                        if not b.deposit(account_id, amount):
                            print("Re-Initiating the Deposit Process")
                            continue
                        break
                elif selected_menu == 3:
                    print("Withdraw Process is getting Initiated !!")
                    while True:
                        account_id = input("enter account_id to withdraw : ")
                        amount = float(input("enter amount to withdraw : "))
                        if not b.withdraw(account_id, amount):
                            print("Re-Initiating the Withdrawal Process")
                            continue
                        break
                elif selected_menu == 4:
                    print("Exiting from the System !!!!")
                    self.logout()
                    print("Thank you!!!. For choosing MY-Bank .Hoping to see you again....")
                    break

                else:
                    print("Wrong Input !!!. Please try again...")
        elif self.account_type == 2:
            while True:
                print("1.stats_transaction", "2.Apply Monthly Interest", "3.Get Account Detail using account_id",
                      "4.Quit/Logout", sep="\n")
                selected_menu = int(input("Select one from the above Options : "))
                if selected_menu == 1:
                    b.stats_transaction()
                elif selected_menu == 2:
                    b.apply_interest_on_all_acc()
                elif selected_menu == 3:
                    while True:
                        account_id = input("enter account_id for search : ")
                        if not b.account_info(account_id):
                            continue
                        break
                elif selected_menu == 4:
                    print("Exiting from the System !!!!")
                    self.logout()
                    print("Thank you!!!. For choosing MY-Bank .Hoping to see you again....")
                    break
                else:
                    print("Wrong Input !!!. Please try again...")

    def logout(self):
        if self.user_name in LOGIN_DETAILS:
            LOGIN_DETAILS.remove(self.user_name)
            return True
        else:
            print("Sorry!!! you are already sign-out or not Logged in ")
            return False
