
# SECTION: Global Data
import os
import file_database as db

created_accounts = []
invalid_special_characters = ['%', '#', '@', '!', '"', '£', '%', '^', '&', '*', '(', ')', '-', '_', '=', '+', '[', ']', '{', '}', '\\', '|', ';', ':', ',', '.', '<', '>', '/', '?', '~', '`']
greeting = 'Welcome'


def save_account_files(customer_name):
    # write pin, balance, transactions and goals to files named by account
    idx = find_account_index(customer_name)
    if idx == -1:
        return
    acc = created_accounts[idx]
    # delegate to file_database helpers
    db.write_pin(customer_name, acc[1])
    db.write_balance(customer_name, acc[2])
    db.write_transactions(customer_name, acc[3])
    db.write_goals(customer_name, acc[4])


def load_all_accounts():
    # find all pin files in current directory
    folder = os.path.dirname(__file__)
    for fname in os.listdir(folder):
        if fname.endswith("_pin.txt"):
            customer_name = fname[:-8]
            # delegate reads to file_database
            pin = db.read_pin(customer_name)
            bal = db.read_balance(customer_name)
            txs = db.read_transactions(customer_name)
            goals = db.read_goals(customer_name)

            # only add if not already present
            if find_account_index(customer_name) == -1:
                created_accounts.append([customer_name, pin, bal, txs, goals])


# SECTION: Input Validation
def is_numerical_value(value_to_check):
    letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    for character in value_to_check:
        if character in letters or character in invalid_special_characters:
            return False
    return True


def is_alphabetic_value(value_to_check):
    for character in value_to_check:
        if ('0' <= character <= '9') or character in invalid_special_characters:
            return False
    return True


def validate_pin_errors(pin_validation_result, customer_pin):
    if not pin_validation_result or not customer_pin:
        print("Please enter a numeric PIN.\n")
        return False
    if len(customer_pin) > 4 or len(customer_pin) < 4:
        print("The PIN must contain exactly 4 digits.\n")
        return False
    return True


def validate_name_errors(name_validation_result):
    if not name_validation_result:
        print("Names may not contain numbers or special characters.\n")
        return False
    return True


# SECTION: Input Prompt Helpers
def prompt_valid_name(prompt_text):
    customer_name = input(prompt_text).title()
    if not customer_name:
        print("\nThis field cannot be left blank.\n")
        return ""
    if not validate_name_errors(is_alphabetic_value(customer_name)):
        return ""
    return customer_name


def prompt_valid_pin(prompt_text):
    customer_pin = input(prompt_text)
    if not validate_pin_errors(is_numerical_value(customer_pin), customer_pin):
        return ""
    return customer_pin


def prompt_positive_amount(prompt_text):
    amount_text = input(prompt_text)
    if not amount_text:
        print("\nA value is required.\n")
        return -1
    if not is_numerical_value(amount_text):
        print("\nPlease enter a valid numeric amount.\n")
        return -1
    return int(amount_text)


def prompt_return_to_account_menu():
    while True:
        choice = input("Would you like to go back to the account menu? (yes/no): ").lower()
        if choice == 'yes':
            return True
        elif choice == 'no':
            return False
        else:
            print("\nPlease respond with yes or no.\n")


# SECTION: Account Data Helpers
def find_account_index(customer_name):
    for index in range(len(created_accounts)):
        if created_accounts[index][0] == customer_name:
            return index
    return -1


def account_exists(customer_name):
    return find_account_index(customer_name) != -1


def _get_account(customer_name):
    account_index = find_account_index(customer_name)
    if account_index == -1:
        return False
    return created_accounts[account_index]


def create_account(customer_name, customer_pin):
    # account structure: [name, pin, balance, transactions_list, goals_list]
    created_accounts.append([customer_name, customer_pin, 0, [], []])
    save_account_files(customer_name)


def read_account_pin(customer_name):
    account = _get_account(customer_name)
    return "" if account is False else account[1]


def read_account_balance(customer_name):
    account = _get_account(customer_name)
    return 0 if account is False else account[2]


def update_account_balance(customer_name, new_balance):
    account = _get_account(customer_name)
    if account is not False:
        account[2] = new_balance
        save_account_files(customer_name)


def add_transaction(customer_name, transaction_text):
    account = _get_account(customer_name)
    if account is not False:
        account[3].append(transaction_text)
        save_account_files(customer_name)


# SECTION: Savings Goals Helpers
def normalize_text(value):
    return value.strip().lower()


def find_goal_index(customer_name, goal_name):
    account = _get_account(customer_name)
    if account is False:
        return -1
    normalized_goal_name = normalize_text(goal_name)
    goals = account[4]
    for index in range(len(goals)):
        if normalize_text(goals[index][0]) == normalized_goal_name:
            return index
    return -1


def get_goals(customer_name):
    account = _get_account(customer_name)
    return [] if account is False else account[4]


def add_savings_goal(customer_name, goal_name, target_amount):
    account = _get_account(customer_name)
    if account is not False:
        # goal structure: [goal_name, target_amount, current_amount]
        account[4].append([goal_name.strip(), target_amount, 0])
        save_account_files(customer_name)


def remove_savings_goal(customer_name, goal_name):
    goal_index = find_goal_index(customer_name, goal_name)
    account = _get_account(customer_name)
    if account is False or goal_index == -1:
        return
    account[4].pop(goal_index)
    save_account_files(customer_name)


def contribute_to_goal(customer_name, goal_name, amount):
    goal_index = find_goal_index(customer_name, goal_name)
    account = _get_account(customer_name)
    if account is False or goal_index == -1:
        return "goal"

    current_balance = read_account_balance(customer_name)
    if amount <= 0 or amount > current_balance:
        return "balance"

    goal = account[4][goal_index]
    update_account_balance(customer_name, current_balance - amount)
    goal[2] = goal[2] + amount
    add_transaction(customer_name, f"Contributed P{amount} to goal '{goal[0]}'")
    save_account_files(customer_name)
    return "ok"


def list_goals_text(customer_name):
    goals = get_goals(customer_name)
    if not goals:
        return ""
    lines = []
    for g in goals:
        name = g[0]
        target = g[1]
        current = g[2]
        percent = 0
        if target > 0:
            percent = int((current / target) * 100)
        lines.append(f"{name}: P{current}/P{target} ({percent}%)")
    return "\n".join(lines)


# SECTION: Transaction History Helpers
def record_withdrawal_transaction(transaction_amount, customer_name):
    add_transaction(customer_name, f"Withdrawal recorded           -P{transaction_amount}")


def record_deposit_transaction(transaction_amount, customer_name):
    add_transaction(customer_name, f"Deposit recorded              P{transaction_amount}")


def remove_account_from_list(customer_name):
    account = _get_account(customer_name)
    if account is not False:
        # remove files associated with this account
        acct_name = account[0]
        created_accounts.remove(account)
        db.delete_account_files(acct_name)


def create_account_history_text(customer_name):
    account = _get_account(customer_name)
    return "" if account is False else "\n".join(account[3])


# SECTION: Menu and Action Handlers
def handle_savings_goals_menu(customer_name):
    goals_menu_active = True
    while goals_menu_active:
        print("\nSavings Goals Tracker")
        print("---------------------")
        print("[1] View Goals")
        print("[2] Add Goal")
        print("[3] Contribute To Goal")
        print("[4] Remove Goal")
        print("[5] Back")
        goals_choice = input("Select an option (1-5): ")

        if goals_choice == "1":
            goals_text = list_goals_text(customer_name)
            if not goals_text:
                print("\nNo goals defined yet.\n")
            else:
                print(f"\n{goals_text}\n")
        elif goals_choice == "2":
            goal_name = input("Enter a name for the goal: ")
            if not goal_name:
                print("\nGoal name required.\n")
            else:
                target_amount = prompt_positive_amount("Enter the target amount for this goal: ")
                if target_amount > 0:
                    add_savings_goal(customer_name, goal_name, target_amount)
                    print("\nGoal added.\n")
                    print("\n" * 24)
        elif goals_choice == "3":
            goal_name = input("Enter the goal name to contribute to: ")
            if not goal_name:
                print("\nGoal name required.\n")
            elif find_goal_index(customer_name, goal_name) == -1:
                print("\nThat goal was not found.\n")
            else:
                amount = prompt_positive_amount("Enter the amount to contribute: ")
                if amount > 0:
                    result = contribute_to_goal(customer_name, goal_name, amount)
                    if result == "ok":
                        print("\nContribution successful.\n")
                        print("\n" * 24)
                    else:
                        print("\nYou do not have enough balance for that contribution.\n")
        elif goals_choice == "4":
            goal_name = input("Enter the goal name to remove: ")
            if not goal_name:
                print("\nGoal name required.\n")
            else:
                remove_savings_goal(customer_name, goal_name)
                print("\nIf the goal existed it was removed.\n")
        elif goals_choice == "5":
            goals_menu_active = False
        else:
            print("\nPlease select a valid option (1-5).\n")


def delete_account_from_system(customer_name):
    remove_account_from_list(customer_name)


def handle_deposit(customer_name, current_account_balance):
    finished = False
    while not finished:
        print(f"\nCurrent Balance: P{current_account_balance}")
        print("-------------------------")
        deposit_amount = prompt_positive_amount("Enter the amount to deposit: ")
        if deposit_amount > 0:
            print(f"\nDeposit completed successfully: P{deposit_amount}.\n")
            update_account_balance(customer_name, deposit_amount + current_account_balance)
            record_deposit_transaction(deposit_amount, customer_name)
            current_account_balance = read_account_balance(customer_name)
            print(f"\nUpdated Balance: P{current_account_balance}\n")
            print("\n" * 24)
            finished = True
        elif deposit_amount == 0:
            print("\nPlease enter an amount greater than zero.\n")


def handle_withdrawal(customer_name, current_account_balance):
    if current_account_balance <= 0:
        print("\nYour account balance is currently zero. Please make a deposit and try again later.")
        print(f"Current Balance: P{current_account_balance}\n")
        return

    finished = False
    while not finished:
        print(f"\nCurrent Balance: P{current_account_balance}")
        print("-------------------------")
        withdrawal_amount = prompt_positive_amount("Enter the amount to withdraw: ")
        if withdrawal_amount > current_account_balance:
            print("\nPlease enter an amount within your available balance.\n")
        elif withdrawal_amount > 0:
            print(f"\nWithdrawal completed successfully: P{withdrawal_amount}.\n")
            update_account_balance(customer_name, current_account_balance - withdrawal_amount)
            record_withdrawal_transaction(withdrawal_amount, customer_name)
            current_account_balance = read_account_balance(customer_name)
            print(f"\nUpdated Balance: P{current_account_balance}\n")
            print("\n" * 24)
            finished = True


def handle_account_menu(customer_name):
    account_menu_active = True
    while account_menu_active:
        print("\nSEONEA Savings Management System")
        print("--------------------------------------------------")
        print("[1] Deposit Funds")
        print("[2] Withdraw Funds")
        print("[3] View Account Balance")
        print("[4] View Transaction History")
        print("[5] Savings Goals Tracker")
        print("[6] Delete Account")
        print("[7] Back to Main Menu")
        account_menu_choice = input("\nPlease select an option (1-7): ")

        current_account_balance = read_account_balance(customer_name)

        if account_menu_choice == "1":
            handle_deposit(customer_name, current_account_balance)
            if not prompt_return_to_account_menu():
                account_menu_active = False
        elif account_menu_choice == "2":
            handle_withdrawal(customer_name, current_account_balance)
            if not prompt_return_to_account_menu():
                account_menu_active = False
        elif account_menu_choice == "3":
            print("\nCurrent Account Balance:")
            print(f"P{current_account_balance}\n")
            if not prompt_return_to_account_menu():
                account_menu_active = False
        elif account_menu_choice == "4":
            transaction_content = create_account_history_text(customer_name)
            if not transaction_content:
                print("\nTransaction History")
                print("------------------")
                print("No transactions have been recorded yet.\n")
            else:
                print("\nTransaction History")
                print("------------------")
                print(f"{transaction_content}\n")
            if not prompt_return_to_account_menu():
                account_menu_active = False
        elif account_menu_choice == "5":
            handle_savings_goals_menu(customer_name)
            if not prompt_return_to_account_menu():
                account_menu_active = False
        elif account_menu_choice == "6":
            deletion_confirmation = input("Would you like to permanently delete this account? (yes/no): ").lower()
            while deletion_confirmation != 'yes' and deletion_confirmation != 'no':
                print("\nPlease respond with yes or no.\n")
                deletion_confirmation = input("Would you like to permanently delete this account? (yes/no): ").lower()

            if deletion_confirmation == 'yes':
                remaining_attempts = 3
                deleted = False
                while remaining_attempts > 0 and not deleted:
                    stored_customer_pin = read_account_pin(customer_name)
                    customer_pin = prompt_valid_pin("Enter your PIN: ")
                    if customer_pin:
                        if stored_customer_pin != customer_pin:
                            print("\nThe PIN you entered is incorrect.\n")
                            remaining_attempts = remaining_attempts - 1
                            print(f"Remaining attempts: {remaining_attempts}.\n")
                            if remaining_attempts == 0:
                                print("No attempts remain. The system will now shut down.\n")
                                exit()
                        else:
                            delete_account_from_system(customer_name)
                            print("\nThe account has been deleted successfully.")
                            print("Thank you for using the SEONEA Savings Management System.\n")
                            deleted = True
                            print("\n" * 24)
                            exit()

            elif deletion_confirmation == 'no':
                return
            else:
                print("An unexpected condition occurred. The system will now shut down.\n")
                exit()
        elif account_menu_choice == "7":
            account_menu_active = False
        else:
            print("\nPlease select one of the available options (1-7).\n")

load_all_accounts()
