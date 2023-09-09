import re

def extract_passwords(log_file, output_file):
    passwords = []
    emails = []
    with open(log_file, 'r') as log:
        for line in log:
            password_pattern = r'\b(?=\S*\d)(?=\S*[a-zA-Z])\S{8,24}\b'
            email_pattern = r'\S+@\w+\.\w+'
            line = line.strip()  # Remove leading/trailing whitespace
            passwords.extend(re.findall(password_pattern, line))
            emails.extend(re.findall(email_pattern, line))

    ranked_passwords = rank_passwords(passwords)

    with open(output_file, 'w') as pass_file:
        pass_file.write('Passwords\n---------\n')
        for password in ranked_passwords:
            pass_file.write(password + '\n')

        pass_file.write('\n------------------------------------------------------------------------------------------\n\n')

        pass_file.write('Emails\n------\n')
        for email in emails:
            pass_file.write(email + '\n')


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
output_file = 'passwords.txt'
extract_passwords(log_file, output_file)