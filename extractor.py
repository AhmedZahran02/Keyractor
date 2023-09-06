import re

def extract_passwords(log_file, password_file):
    passwords = []
    with open(log_file, 'r') as log:
        for line in log:
            pattern = r'\b(?=\S*\d)(?=\S*[a-zA-Z])\S{8,24}\b'
            line = line.strip()  # Remove leading/trailing whitespace
            passwords.extend(re.findall(pattern, line))

    ranked_passwords = rank_passwords(passwords)

    with open(password_file, 'w') as pass_file:
        for password in ranked_passwords:
            pass_file.write(password + '\n')


def rank_passwords(passwords):
    ranked_passwords = {}
    default_score = 0

    for password in passwords:
        if password not in ranked_passwords:
            ranked_passwords[password] = default_score

    for password in ranked_passwords:
        if has_special_character(password):
            ranked_passwords[password] += 15
        if has_capital_character(password):
            ranked_passwords[password] += 10

    # Sort passwords by scores in descending order
    sorted_passwords = sorted(ranked_passwords.keys(), key=lambda password: ranked_passwords[password], reverse=True)
    return sorted_passwords

def has_capital_character(string):
    pattern = r'[A-Z]'  # Regular expression pattern to match any capital character
    match = re.search(pattern, string)
    return match is not None

def has_special_character(string):
    pattern = r'[^a-zA-Z0-9\s]'  # Regular expression pattern to match any non-alphanumeric character except whitespace
    match = re.search(pattern, string)
    return match is not None


log_file = 'sus.txt'
password_file = 'passwords.txt'
extract_passwords(log_file, password_file)