
import numpy as np
#Partially written with assistance from chatGPT-4
def read_numbers_from_file(file_path):
    numbers_list = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                # Strip the newline character and any whitespace, then convert to an integer
                number = int(line.strip())
                numbers_list.append(number)
    except FileNotFoundError:
        print(f"The file {file_path} was not found.")
    except ValueError:
        print("The file contains non-numeric data.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return numbers_list

# Replace 'numbers.txt' with the path to your text file
file_path = 'data_only_log.txt'
numbers = read_numbers_from_file(file_path)
count = 0
for el in numbers:
    if el < 255:
        count += 1

print(count)
