import os


def validator(value):
    if not value:
        return False
    for character in value:
        if character < '0' or character > '9':
            return False
    return True

def account_exists(name):
    return os.path.exists(f"{name}.txt")


def create_account_files(name, pin):
    # create transaction log
    acct_file = open(f"{name}.txt", "x")
    acct_file.close()
    # create balance file
    bal = open(f"{name}_bal.txt", "w")
    bal.write("0")
    bal.close()
    # create pin file
    pinf = open(f"{name}_pin.txt", "w")
    pinf.write(str(pin))
    pinf.close()
    # create goals file (empty)
    goalsf = open(f"{name}_goals.txt", "w")
    goalsf.close()


def read_pin(name):
    if not os.path.exists(f"{name}_pin.txt"):
        return ""
    fh = open(f"{name}_pin.txt", "r")
    val = fh.read().strip()
    fh.close()
    return val


def read_balance(name):
    if not os.path.exists(f"{name}_bal.txt"):
        return 0
    fh = open(f"{name}_bal.txt", "r")
    txt = fh.read().strip()
    fh.close()
    if validator(txt):
        return int(txt)
    return 0


def write_balance(name, amount):
    fh = open(f"{name}_bal.txt", "w")
    fh.write(str(amount))
    fh.close()


def append_transaction(name, text):
    if not os.path.exists(f"{name}.txt"):
        create_account_files(name, "")
    fh = open(f"{name}.txt", "a")
    fh.write(text.replace('\n', ' ') + "\n")
    fh.close()


def read_transactions(name):
    if not os.path.exists(f"{name}.txt"):
        return []
    fh = open(f"{name}.txt", "r")
    lines = [line.rstrip('\n') for line in fh]
    fh.close()
    return lines


def delete_account_files(name):
    for fname in (f"{name}.txt", f"{name}_pin.txt", f"{name}_bal.txt", f"{name}_goals.txt"):
        if os.path.exists(fname):
            os.remove(fname)


def write_pin(name, pin):
    fh = open(f"{name}_pin.txt", "w")
    fh.write(str(pin))
    fh.close()


def write_transactions(name, tx_list):
    fh = open(f"{name}.txt", "w")
    for t in tx_list:
        fh.write(t.replace('\n', ' ') + "\n")
    fh.close()


def write_goals(name, goals_list):
    fh = open(f"{name}_goals.txt", "w")
    for g in goals_list:
        fh.write(f"{g[0]}|{g[1]}|{g[2]}\n")
    fh.close()


def read_goals(name):
    goals = []
    if not os.path.exists(f"{name}_goals.txt"):
        return goals
    fh = open(f"{name}_goals.txt", "r")
    for line in fh:
        parts = line.rstrip('\n').split('|')
        if len(parts) == 3:
            gname = parts[0]
            target = int(parts[1]) if validator(parts[1]) else 0
            current = int(parts[2]) if validator(parts[2]) else 0
            goals.append([gname, target, current])
    fh.close()
    return goals
