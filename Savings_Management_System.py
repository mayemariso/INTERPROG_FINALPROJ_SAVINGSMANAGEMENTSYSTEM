import os
import savings_functions as sv
import file_database as db


def main():
    while True:
        print(f"|+====|SEONEA Savings|====+|\n[1] Log In\n[2] Create Account\n[3] Close")
        user = input("Select an option (1-3): ")

        if user == "1":
            while True:
                account_name = input("Enter your name: ").title()
                if not account_name:
                    print("Please don't leave this empty!\n")
                    continue
                check_name = sv.is_alphabetic_value(account_name)
                if not sv.validate_name_errors(check_name):
                    continue
                if not os.path.exists(f"{account_name}.txt"):
                    print("This account does not exist.\n")
                    break
                account_pin = input("Enter your PIN: ")
                check_pin = sv.is_numerical_value(account_pin)
                if not sv.validate_pin_errors(check_pin, account_pin):
                    continue
                else:
                    saved_pin = db.read_pin(account_name)
                    if saved_pin != account_pin:
                        print("You entered the wrong PIN.\n")
                        break
                    else:
                        print(f"\n{sv.greeting}, {account_name}!\n")

                        while True:
                            print(f"|+====|SEONEA Savings|====+|\n[1] Deposit\n[2] Withdraw\n[3] Check Account Balance\n[4] Check Account Transactions\n[5] Savings Goals Tracker\n[6] Delete Account\n[7] Close")
                            user_ch = input("\nSelect an option (1-7): ")
                            current_bal = db.read_balance(account_name)

                            if user_ch == "1":
                                while True:
                                    print(f"\nCurrent Balance: P{current_bal}")
                                    dp_amount = input("How much will you deposit?: ")
                                    if not dp_amount:
                                        print("Please enter a value.")
                                        continue
                                    verify_amount = sv.is_numerical_value(dp_amount)
                                    while not verify_amount:
                                        print("Please enter a valid value.")
                                        print(f"\nCurrent Balance: P{current_bal}")
                                        dp_amount = input("How much will you deposit?: ")
                                        if not dp_amount:
                                            print("Please enter a value.")
                                            continue
                                        verify_amount = sv.is_numerical_value(dp_amount)
                                    dp_amount = int(dp_amount)
                                    if dp_amount <= 0:
                                        print("Please deposit an amount greater than 0!")
                                        continue
                                    print(f"\nSuccessfully deposited P{dp_amount}!")
                                    db.write_balance(account_name, dp_amount + current_bal)
                                    sv.update_account_balance(account_name, dp_amount + current_bal)
                                    sv.record_deposit_transaction(dp_amount, account_name)
                                    current_bal = dp_amount + current_bal
                                    print(f"New Balance: P{current_bal}\n")
                                    break

                            elif user_ch == "2":
                                if current_bal <= 0:
                                    print(f"\nYour balance is currently empty, please deposit and try again later!\nCurrent Balance: P{current_bal}\n")
                                else:
                                    while True:
                                        print(f"\nCurrent Balance: P{current_bal}")
                                        wd_amount = input("How much will you withdraw?: ")
                                        if not wd_amount:
                                            print("Please enter a value.")
                                            continue
                                        verify_amount = sv.is_numerical_value(wd_amount)
                                        while not verify_amount:
                                            print("Please enter a valid value.")
                                            print(f"\nCurrent Balance: P{current_bal}")
                                            wd_amount = input("How much will you withdraw?: ")
                                            if not wd_amount:
                                                print("Please enter a value.")
                                                continue
                                            verify_amount = sv.is_numerical_value(wd_amount)
                                        wd_amount = int(wd_amount)
                                        if wd_amount > current_bal or wd_amount <= 0:
                                            print("\nPlease enter an amount within your available balance. Please try again.")
                                            continue
                                        print(f"\nSuccessfully withdrawn P{wd_amount}!")
                                        db.write_balance(account_name, current_bal - wd_amount)
                                        sv.update_account_balance(account_name, current_bal - wd_amount)
                                        sv.record_withdrawal_transaction(wd_amount, account_name)
                                        current_bal = current_bal - wd_amount
                                        print(f"New Balance: P{current_bal}\n")
                                        break

                            elif user_ch == "3":
                                print(f"\nYour current balance:\nP{current_bal}\n")

                            elif user_ch == "4":
                                txs = db.read_transactions(account_name)
                                if not txs:
                                    print(f"\n|+========|Transaction Log|========+|\nThis is empty.\n")
                                else:
                                    print(f"\n|+========|Transaction Log|========+|\n" + "\n".join(txs))

                            elif user_ch == "5":
                                sv.handle_savings_goals_menu(account_name)

                            elif user_ch == "6":
                                confirmation = input("Are you sure you want to delete this account? (Y/N): ").lower()
                                while confirmation not in ('y', 'n', 'yes', 'no'):
                                    print("\nPlease enter Y or N!")
                                    confirmation = input("Are you sure you want to delete this account? (Y/N): ").lower()
                                if confirmation in ('y', 'yes'):
                                    attempts = 3
                                    while True:
                                        saved_pin = db.read_pin(account_name)
                                        account_pin = input("Enter your PIN: ")
                                        check_pin = sv.is_numerical_value(account_pin)
                                        if not sv.validate_pin_errors(check_pin, account_pin):
                                            continue
                                        if saved_pin != account_pin:
                                            print("Wrong PIN.")
                                            attempts -= 1
                                            print(f"You have {attempts} attempts left.\n")
                                            if attempts == 0:
                                                print("No attempts left, forcing shut down.")
                                                exit()
                                            else:
                                                continue
                                        db.delete_account_files(account_name)
                                        print("Account successfully deleted!")
                                        print("\nThank you for using SEONEA Savings!\n")
                                        exit()
                                else:
                                    continue

                            elif user_ch == "7":
                                print("\nThank you for using SEONEA Savings!\n")
                                exit()
                            else:
                                print("\nPlease enter one of the existing options (1-7).\n")
                                continue

                            use_again = input("Would you like to continue to the main menu? (Y/N): ").lower()
                            while use_again not in ('y', 'n', 'yes', 'no'):
                                print("\nPlease enter Y or N!")
                                use_again = input("\nWould you like to continue? (Y/N): ").lower()
                            if use_again in ('y', 'yes'):
                                continue
                            else:
                                print("\nThank you for using SEONEA Savings. Goodbye!\n")
                                exit()

        elif user == "2":
            while True:
                account_name = input("Enter your name: ").title()
                if not account_name:
                    print("Please don't leave this empty!\n")
                    continue
                check_name = sv.is_alphabetic_value(account_name)
                if not sv.validate_name_errors(check_name):
                    continue
                if os.path.exists(f"{account_name}.txt"):
                    print("This account already exists!\n")
                    continue
                account_pin = input("Enter a 4-DIGIT PIN: ")
                check_pin = sv.is_numerical_value(account_pin)
                if not sv.validate_pin_errors(check_pin, account_pin):
                    continue
                verify_pin = input("Confirm your PIN: ")
                if verify_pin != account_pin:
                    print("PINs do not match.\n")
                    continue
                db.create_account_files(account_name, account_pin)
                sv.load_all_accounts()
                print("Account successfully created!\n")
                break

        elif user == "3":
            print("\nThank you for using SEONEA Savings!\n")
            exit()
        else:
            print("\nPlease enter one of the existing options (1-3).\n")
            continue


if __name__ == "__main__":
    main()
