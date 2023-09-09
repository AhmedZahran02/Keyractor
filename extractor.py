import re
from subprocess import call
import time

class PasswordObject:
    password = ""
    domain = ""
    username = ""

    def __init__(self, password, domain, username):
        self.password = password
        self.domain = domain
        self.username = username


def extract_passwords(log_file, output_file):
    passwords = []
    emails = []

    curr_line_passwords = []
    user_line = ""
    domain_line = ""

    with open(log_file, 'r') as log:
        for line in log:
            password_pattern = r'\b(?=\S*\d)(?=\S*[a-zA-Z])\S{8,24}\b'
            email_pattern = r'\S+@\w+\.\w+'
            line = line.strip()  # Remove leading/trailing whitespace
            curr_line_passwords = re.findall(password_pattern, line)

            username = ""
            domain = ""
            if user_line != "":
                username = user_line.split()[-1]
            if domain_line != "":
                domain = domain_line.split()[-1]

            for password in curr_line_passwords:
                passwordObj = PasswordObject(password, domain, username)
                passwords.append(passwordObj)
            emails.extend(re.findall(email_pattern, line))

            domain_line = user_line
            user_line = line
    

    ranked_passwords = rank_passwords(passwords)

    with open(output_file, 'w') as pass_file:
        pass_file.write(f'Password {" ":20} Potential Username {" ":21} Potential Domain \n-------------------------------------------------------------------------------------------------\n')
        for passwordObj in ranked_passwords:
            pass_file.write(f'{passwordObj.password:30} {passwordObj.username:40} {passwordObj.domain:40} \n')

        pass_file.write('\n-------------------------------------------------------------------------------------------------\n\n')

        pass_file.write('Emails\n------\n')
        for email in emails:
            pass_file.write(email + '\n')


def rank_passwords(passwords):
    ranked_passwords = {}
    default_score = 0

    for passwordObj in passwords:
        if passwordObj not in ranked_passwords:
            ranked_passwords[passwordObj] = default_score

    for passwordObj in ranked_passwords:
        if has_special_character(passwordObj.password):
            ranked_passwords[passwordObj] += 15
        if has_capital_character(passwordObj.password):
            ranked_passwords[passwordObj] += 10

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

mode = 0
while mode != "1" and mode != "2":
    print("\n1- Text File (log.txt)")
    print("2- RSA Encrypted File (log.rsa)")
    mode = input("Enter the type of file to extract from: ")

if mode == 2:
    encrypted = 'log.rsa'
    call(["./rsa.exe", "10527635191", "8343962999", "8","log.rsa","log.txt"])
    time.sleep(3)

log_file = 'log.txt'
output_file = 'output.txt'
extract_passwords(log_file, output_file)