# this file is used to convert potential recordings of different excitatory neurons to fixed point to analyze the potential value and debug the neuron behavior

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


def transform_potentials(input_file_path, output_file_path, integer_precision, fraction_precision):
    print("Transforming...")
    try:
        # Read the input file
        with open(input_file_path, 'r') as f:
            lines = f.readlines()

        # Transform each entry in the list to floating point format
        transformed_list = []
        for line in lines:

            if ("x" not in line):
                transformed_digit = fp_to_float(line[:-1], integer_precision, fraction_precision)
                transformed_list.append(transformed_digit)

        try:
            with open(output_file_path, 'w') as f:
                for digit in transformed_list:
                    f.write(str(digit))
                    f.write("\n")

        except:
            print("Could not save transformed weights to file")
                
    except Exception as e:
        print(f"Error: {e}")


def transform_multiple_potentials(input_file_path, output_file_path, integer_precision, fraction_precision):
    print("Transforming multiple potentials...")
    try:
        # Read the input file
        with open(input_file_path, 'r') as f:
            lines = f.readlines()

        # Open the output file
        with open(output_file_path, 'w') as f_out:
            # Transform each line in the file
            for line in lines:
                # Split the line into individual digits
                digits = line.strip().split(' ')
                
                # Transform each digit and collect them in a list
                transformed_digits = [fp_to_float(digit, integer_precision, fraction_precision) for digit in digits if "x" not in digit]
                print(transformed_digits)
                # Join the transformed digits with a space and write to the output file
                transformed_line = ' '.join(map(str, transformed_digits))
                print(transformed_line)
                f_out.write(transformed_line + "\n")

    except Exception as e:
        print(f"Error: {e}")

input_file = "multi_potential_recording.txt"
output_file = "multi_converted_potentials_3.txt"
transform_multiple_potentials(input_file,output_file, 3, 60)