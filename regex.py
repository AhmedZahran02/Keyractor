import re

def find_passwords(log_file, password_file):
    with open(log_file, 'r') as log:
        for line in log:
            line = line.strip()  # Remove leading/trailing whitespace
            passwords = re.findall(r'\b(?=\w*\d)(?=\w*[a-zA-Z])\w{8,24}\b', line)

            with open(password_file, 'a') as pass_file:
                for password in passwords:
                    pass_file.write(password + '\n')

log_file = 'sus.txt'
password_file = 'passwords.txt'
find_passwords(log_file, password_file)