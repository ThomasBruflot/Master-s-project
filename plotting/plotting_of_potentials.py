import matplotlib.pyplot as plt

def twos_comp(val,integer_precision,fraction_precision):
    flipped = ''.join(str(1-int(x))for x in val)
    length = '0' + str(integer_precision+fraction_precision) + 'b'
    bin_literal = format((int(flipped,2)+1),length)
    return bin_literal


def float_to_fp(num,integer_precision,fraction_precision):   
    if(num<0):
        sign_bit = 1                                          #sign bit is 1 for negative numbers in 2's complement representation
        num = -1*num
    else:
        sign_bit = 0
    precision = '0'+ str(integer_precision) + 'b'
    integral_part = format(int(num),precision)
    fractional_part_f = num - int(num)
    fractional_part = []
    for i in range(fraction_precision):
        d = fractional_part_f*2
        fractional_part_f = d -int(d)        
        fractional_part.append(int(d))
    fraction_string = ''.join(str(e) for e in fractional_part)
    if(sign_bit == 1):
        binary = str(sign_bit) + twos_comp(integral_part + fraction_string,integer_precision,fraction_precision)
    else:
        binary = str(sign_bit) + integral_part+fraction_string
    return str(binary)


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


def read_potentials(input_file_path, integer_precision, fraction_precision):
    try:
        converted_list = []
        # Read the input file
        with open(input_file_path, 'r') as f:
            lines = f.readlines()

        # Convert each line to a list of floating point numbers
        for line in lines[530:540]:
            if ("x" not in line):
                transformed_digit = fp_to_float(line[:-2], integer_precision, fraction_precision)
                converted_list.append(transformed_digit)


        return converted_list
    except Exception as e:
        print(f"Error: {e}")

potentials_list = read_potentials("potential_recording_for_plotting_index_23.txt",10,53)

def plot_the_potentials(potentials):
    xs = [x for x in range(len(potentials))]
    plt.stem(xs, potentials)
    plt.show()
    plt.close()

plot_the_potentials(potentials_list)