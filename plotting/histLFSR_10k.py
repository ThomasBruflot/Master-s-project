import matplotlib.pyplot as plt
import numpy as np


# Read values from file
def read_values_from_file():
    counter = 0
    values = []
    file_path = 'data_only_log.txt' #'data_log_large.txt'
    with open(file_path, 'r') as file:
        for line in file:
            counter += 1
            if counter < 50000:
                try:
                    value = int(line.strip())
                    if 0 <= value <= 65536:
                        values.append(value)
                    else:
                        print(f"Value out of range (0-65536) ignored: {value}")
                except ValueError as e:
                    print(f"Invalid value ignored: {line.strip()}")
            else:
                print("Counter value: ", counter)
                print("Counter limit exceeded, breaking")
                return values
    return values

values = read_values_from_file()
values_arr = np.array(values)
print("Values: ", values)
print(type(values))
# Create histogram
plt.hist(values_arr.flatten(), bins=50, color='blue', edgecolor='black')

# Add title and labels
plt.title('Histogram of Values')
plt.xlabel('Value')
plt.ylabel('Frequency')

# Show the histogram
plt.show()