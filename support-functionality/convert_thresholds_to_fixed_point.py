# This file takes in all the thresholds that have been adjusted during training, converts them and stores them in file



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
    #print(str(binary))
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

def convert_thresholds_from_File(input_file_path, output_file_path, integer_precision, fraction_precision):
    print("Transforming thresholds...")
    try:
        # Read the input file
        with open(input_file_path, 'r') as f:
            lines = f.readlines()

        # Transform each entry in the list to floating point format
        transformed_list = []
        for line in lines:
            #x = float("{:.5f}".format(float(line.strip())))
            #print(x)
            #print(line.strip())
            #print(line[:-1])
            #print(float(line))
            #print(float(line[:-1]))
            transformed_digit = float_to_fp(float(line.strip()), integer_precision, fraction_precision)
            print(line.strip())
            print(transformed_digit)
            transformed_list.append(transformed_digit)

        try:
            with open(output_file_path, 'w') as f:
                for digit in transformed_list:
                    #print(len(digit))
                    print(digit)
                    f.write(str(digit))
                    f.write("\n")

        except:
            print("Could not save transformed thresholds to file")
                
    except Exception as e:
        print(f"Error: {e}")


input_file = "thresholds.txt"
output_file = "thresholds_fixed_16_47.txt"
convert_thresholds_from_File(input_file,output_file, 16, 47)


def threshold_verification(input_file_path, integer_precision, fraction_precision):
    try:
        
        # Read the input file
        with open(input_file_path, 'r') as f:
            lines = f.readlines()
            for line in lines:
                print(fp_to_float(line, integer_precision, fraction_precision))

    except Exception as e:
        print(f"Error: {e}")

#threshold_verification("thresholds_fixed_16_47.txt",16,47)