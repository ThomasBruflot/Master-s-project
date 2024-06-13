import numpy as np
def twos_comp(val,integer_precision,fraction_precision):
    flipped = ''.join(str(1-int(x))for x in val)
    length = '0' + str(integer_precision+fraction_precision) + 'b'
    bin_literal = format((int(flipped,2)+1),length)
    return bin_literal



def fp_to_float(s,integer_precision,fraction_precision):       #s = input binary string
    number = 0.0
    i = integer_precision - 1
    j = 0
    if(s[0] == '1'):
        s_complemented = twos_comp((s[1:]),integer_precision,fraction_precision)
    else:
        s_complemented = s[1:]
    while(j != integer_precision + fraction_precision -1):
        number += int(s_complemented[j])*(2**i)
        i -= 1
        j += 1
    if(s[0] == '1'):
        return (-1)*number
    else:
        return number


def analyze_weights(input_file_path):
    try:
        # Read the input file
        with open(input_file_path, 'r') as f:
            lines = f.readlines()

        # Convert each line to a list of floating point numbers
        input_lists = []
        for line in lines:
            input_list = [float(entry) for entry in line[1:-2].split(',')]
            input_lists.append(input_list)

        for lst in input_lists:
            print("Max: ", max(lst))
            print("Min: ", min(i for i in lst if i > 0.0))
        
        return input_lists


    except Exception as e:
        print(f"Error: {e}")
    


def analyze_fixed_point_weights(input_file_path, integer_precision, fraction_precision):
    try:
        # Read the input file
        with open(input_file_path, 'r') as f:
            lines = f.readlines()

        # Convert each line to a list of floating point numbers
        input_lists = []
        for line in lines:
            #print(line[1:-2])
            input_list = [fp_to_float(entry,integer_precision,fraction_precision) for entry in line[1:-2].split(',')]
            input_lists.append(input_list)
        for lst in input_lists:
            print("Max: ", max(lst))
            print("Min: ", min(i for i in lst if i > 0.0))
        
        return input_lists
       
    except Exception as e:
        print(f"Error: {e}")

input_file = "weights_fixed_point_LFSR_to_excitatory_10_53.txt"


def analyze_inhibitory_weights(input_file_path):
    try:
        # Read the input file
        with open(input_file_path, 'r') as f:
            lines = f.readlines()

        # Convert each line to a list of floating point numbers
        input_lists = []
        for line in lines:
            input_list = [float(entry) for entry in line[1:-2].split(',')]
            input_lists.append(input_list)

        for lst in input_lists:
            print("Max: ", max(lst))
            print("Min: ", min(i for i in lst if i > 0.0))
            print("Index max: ", np.argmax(lst))
            print("Index min: ", np.argmin(lst))
        
        return input_lists


    except Exception as e:
        print(f"Error: {e}")

#analyze_inhibitory_weights("Conn_Ae_Ai_converted 1.txt")


def analyze_weights_inhib(input_file_path):
    try:
        # Read the input file
        with open(input_file_path, 'r') as f:
            lines = f.readlines()

        # Convert each line to a list of floating point numbers
        input_lists = []
        for line in lines:
            print(line[1:-2])
            input_list = [float(entry) for entry in line[1:-2].split(',')]
            input_lists.append(input_list)

        print(len(input_lists))
        print(len(input_lists[0]))
        print(len(input_lists[-1]))
        
        return input_lists


    except Exception as e:
        print(f"Error: {e}")

analyze_weights_inhib("conn_Ai_Ae_converted 1.txt")