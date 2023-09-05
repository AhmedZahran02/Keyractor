import sys
import os


# function entity should contain Name and body and parameters
functions_entities = []




sus_file = "./heck.py"

if not os.path.exists(sus_file): 
    print("File Doesn't Exist ... Please Check It And Try Again")
    exit(0)

file_content = ""
main_body = ""
with open(sus_file) as file: 
    for line in file:
        file_content += line
        if line[0] != ' ' and line[0:4] != "def " and line[0] != '\n':
            main_body += line


file_size = len(file_content)

def generate_function(start_index, spaces_before):
    # now start index should be placed on the f in def keyword we need to make sure it's def keyword not some 
    # random variable
    global file_content
    global file_size
    start = start_index
    start_index += 3
    
    while file_content[start_index] == ' ': start_index += 1

    #now we should be on the first character of the function name
    function_name = ""
    while (file_content[start_index] != '('): 
        function_name += file_content[start_index]
        start_index += 1
    
    while (file_content[start_index] != '\n'): start_index += 1
    start_index += 1
    #now we search for a line that starts with spaces equal to the spaces before the function definition
    # def func():
    #     blabla...
    # main

    function_body = ""

    while start_index < file_size:
        spaces_counter = 0
        while start_index < file_size and file_content[start_index] == ' ': 
            start_index += 1
            spaces_counter += 1

        if spaces_counter == spaces_before and file_content[start_index + 1] != '\n': # to elimiate empty lines
            functions_entities.append([function_name,function_body,start, start_index - spaces_counter])
            return start_index
        
        while start_index < file_size and file_content[start_index] != '\n':
            function_body += file_content[start_index]
            start_index += 1
        start_index += 1
    functions_entities.append([function_name,function_body,start, start_index - spaces_counter])
    return start_index


def handleMatcher(matching, char):
    if matching == 0 and char == 'd':
        matching = matching + 1
    elif matching == 1 and char == 'e':
        matching = matching + 1
    elif matching == 2 and char == 'f':
        matching = matching + 1
    else:
        matching = 0
    return matching


def main_func():
    global functions_entities,main_body
    spaces = 0
    for i in range(0,file_size):
        if file_content[i : i+4] == "def ":
            i = generate_function(i,spaces) - 1
            
        if i < file_size and file_content[i] == ' ':
            spaces += 1
        else: 
            spaces = 0
    functions_entities.append(["main",main_body])
    return functions_entities

print(main_func())