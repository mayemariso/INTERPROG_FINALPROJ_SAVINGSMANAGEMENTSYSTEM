# SECTION: Global Data
created_accounts = []
invalid_special_characters = ['$', '%', '#', '@', '!', '"', '£', '$', '%', '^', '&', '*', '(', ')', '-', '_', '=', '+', '[', ']', '{', '}', '\\', '|', ';', ':', ',', '.', '<', '>', '/', '?', '~', '`']
greeting_messages = ['Welcome', 'Good day', 'Greetings', 'Hello']


# SECTION: Validation Utilities
def is_numerical_value(value_to_check):
    for character in value_to_check:
        if ('a' <= character <= 'z') or ('A' <= character <= 'Z') or character in invalid_special_characters:
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


def get_continue_prompt(continue_choice):
    if continue_choice == 'yes':
        return True
    elif continue_choice == 'no':
        print("Thank you for using the SEONEA Savings Management System.\n")
        return False


def prompt_yes_no(prompt_text):
    while True:
        user_choice = input(prompt_text).lower()
        if user_choice == 'yes':
            return True
        elif user_choice == 'no':
            print("\nThank you for using the SEONEA Savings Management System.\n")
            return False
        else:
            print("\nPlease respond with yes or no.\n")


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


def create_account(customer_name, customer_pin):
    # account structure: [name, pin, balance, transactions_list, goals_list]
    created_accounts.append([customer_name, customer_pin, 0, [], []])


def read_account_pin(customer_name):
    account_index = find_account_index(customer_name)
    if account_index == -1:
        return ""
    return created_accounts[account_index][1]


def read_account_balance(customer_name):
    account_index = find_account_index(customer_name)
    if account_index == -1:
        return 0
    return created_accounts[account_index][2]


def update_account_balance(customer_name, new_balance):
    account_index = find_account_index(customer_name)
    if account_index != -1:
        created_accounts[account_index][2] = new_balance


def add_transaction(customer_name, transaction_text):
    account_index = find_account_index(customer_name)
    if account_index != -1:
        created_accounts[account_index][3].append(transaction_text)


# SECTION: Savings Goals Helpers
def normalize_text(value):
    return value.strip().lower()


def find_goal_index(customer_name, goal_name):
    account_index = find_account_index(customer_name)
    if account_index == -1:
        return -1
    normalized_goal_name = normalize_text(goal_name)
    goals = created_accounts[account_index][4]
    for index in range(len(goals)):
        if normalize_text(goals[index][0]) == normalized_goal_name:
            return index
    return -1


def get_goals(customer_name):
    account_index = find_account_index(customer_name)
    if account_index == -1:
        return []
    return created_accounts[account_index][4]


def add_savings_goal(customer_name, goal_name, target_amount):
    account_index = find_account_index(customer_name)
    if account_index != -1:
        # goal structure: [goal_name, target_amount, current_amount]
        created_accounts[account_index][4].append([goal_name.strip(), target_amount, 0])


def remove_savings_goal(customer_name, goal_name):
    account_index = find_account_index(customer_name)
    goal_index = find_goal_index(customer_name, goal_name)
    if account_index == -1 or goal_index == -1:
        return
    created_accounts[account_index][4].pop(goal_index)


def contribute_to_goal(customer_name, goal_name, amount):
    account_index = find_account_index(customer_name)
    goal_index = find_goal_index(customer_name, goal_name)
    if account_index == -1 or goal_index == -1:
        return "goal"

    current_balance = read_account_balance(customer_name)
    if amount <= 0 or amount > current_balance:
        return "balance"

    goal = created_accounts[account_index][4][goal_index]
    update_account_balance(customer_name, current_balance - amount)
    goal[2] = goal[2] + amount
    add_transaction(customer_name, f"Contributed ${amount} to goal '{goal[0]}'")
    return "ok"


def list_goals_text(customer_name):
    goals = get_goals(customer_name)
    if not goals:
        return ""
    out = ""
    for g in goals:
        name = g[0]
        target = g[1]
        current = g[2]
        percent = 0
        if target > 0:
            percent = int((current / target) * 100)
        line = f"{name}: ${current}/${target} ({percent}%)"
        if out == "":
            out = line
        else:
            out = out + "\n" + line
    return out


# SECTION: Transaction History Helpers
def record_withdrawal_transaction(transaction_amount, customer_name):
    add_transaction(customer_name, f"Withdrawal recorded           -${transaction_amount}")


def record_deposit_transaction(transaction_amount, customer_name):
    add_transaction(customer_name, f"Deposit recorded              ${transaction_amount}")


def remove_account_from_list(customer_name):
    account_index = find_account_index(customer_name)
    if account_index != -1:
        created_accounts.pop(account_index)


def create_account_history_text(customer_name):
    account_index = find_account_index(customer_name)
    if account_index == -1:
        return ""
    transaction_text = ""
    for transaction in created_accounts[account_index][3]:
        if transaction_text == "":
            transaction_text = transaction
        else:
            transaction_text = transaction_text + "\n" + transaction
    return transaction_text


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
                print("\n" + goals_text + "\n")
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
            else:
                amount = prompt_positive_amount("Enter the amount to contribute: ")
                if amount > 0:
                    result = contribute_to_goal(customer_name, goal_name, amount)
                    if result == "ok":
                        print("\nContribution successful.\n")
                        print("\n" * 24)
                    elif result == "goal":
                        print("\nThat goal was not found.\n")
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


def delete_account_data(customer_name):
    remove_account_from_list(customer_name)


def handle_deposit(customer_name, current_account_balance):
    finished = False
    while not finished:
        print("\nCurrent Balance: $" + str(current_account_balance))
        print("-------------------------")
        deposit_amount = prompt_positive_amount("Enter the amount to deposit: ")
        if deposit_amount > 0:
            print("\nDeposit completed successfully: $" + str(deposit_amount) + ".\n")
            update_account_balance(customer_name, deposit_amount + current_account_balance)
            record_deposit_transaction(deposit_amount, customer_name)
            current_account_balance = read_account_balance(customer_name)
            print("\nUpdated Balance: $" + str(current_account_balance) + "\n")
            print("\n" * 24)
            finished = True
        elif deposit_amount == 0:
            print("\nPlease enter an amount greater than zero.\n")


def handle_withdrawal(customer_name, current_account_balance):
    if current_account_balance <= 0:
        print("\nYour account balance is currently zero. Please make a deposit and try again later.")
        print("Current Balance: $" + str(current_account_balance) + "\n")
        return

    finished = False
    while not finished:
        print("\nCurrent Balance: $" + str(current_account_balance))
        print("-------------------------")
        withdrawal_amount = prompt_positive_amount("Enter the amount to withdraw: ")
        if withdrawal_amount > current_account_balance:
            print("\nPlease enter an amount within your available balance.\n")
        elif withdrawal_amount > 0:
            print("\nWithdrawal completed successfully: $" + str(withdrawal_amount) + ".\n")
            update_account_balance(customer_name, current_account_balance - withdrawal_amount)
            record_withdrawal_transaction(withdrawal_amount, customer_name)
            current_account_balance = read_account_balance(customer_name)
            print("\nUpdated Balance: $" + str(current_account_balance) + "\n")
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
            print("$" + str(current_account_balance) + "\n")
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
                print(transaction_content + "\n")
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
                            print("Remaining attempts: " + str(remaining_attempts) + ".\n")
                            if remaining_attempts == 0:
                                print("No attempts remain. The system will now shut down.\n")
                                exit()
                        else:
                            delete_account_data(customer_name)
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


# SECTION: Program Entry Point
def main():
    program_exit = False
    while not program_exit:
        print("\nSEONEA Savings Management System")
        print("--------------------------------------------------")
        print("[1] Log In")
        print("[2] Create Account")
        print("[3] Exit")
        main_menu_choice = input("Please select an option (1-3): ")

        if main_menu_choice == "1":
            login_complete = False
            while not login_complete:
                customer_name = prompt_valid_name("Enter your full name: ")
                if customer_name:
                    if not account_exists(customer_name):
                        print("\nNo account was found under that name.\n")
                        login_complete = True
                    else:
                        customer_pin = prompt_valid_pin("Enter your 4-digit PIN: ")
                        if customer_pin:
                            stored_customer_pin = read_account_pin(customer_name)
                            if stored_customer_pin != customer_pin:
                                print("\nThe PIN you entered is incorrect.\n")
                                login_complete = True
                            else:
                                selected_greeting_index = int(len(greeting_messages) * 0.5)
                                print("\n" + greeting_messages[selected_greeting_index] + ", " + customer_name + "!\n")
                                handle_account_menu(customer_name)
                                login_complete = True

        elif main_menu_choice == "2":
            account_created = False
            while not account_created:
                customer_name = prompt_valid_name("Enter your full name: ")
                if customer_name:
                    if account_exists(customer_name):
                        print("\nAn account with this name already exists.\n")
                        account_created = True
                    else:
                        customer_pin = prompt_valid_pin("Enter a 4-digit PIN: ")
                        if customer_pin:
                            confirm_customer_pin = input("Confirm your PIN: ")
                            if confirm_customer_pin != customer_pin:
                                print("\nThe PIN entries do not match.\n")
                            else:
                                create_account(customer_name, customer_pin)
                                print("\nThe account has been created successfully.\n")
                                print("\n" * 24)
                                account_created = True

        elif main_menu_choice == "3":
            print("\nThank you for using the SEONEA Savings Management System.\n")
            exit()
        else:
            print("\nPlease select one of the available options (1-3).\n")


main()
