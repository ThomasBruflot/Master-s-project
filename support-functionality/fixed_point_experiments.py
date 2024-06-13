# This code is used to quickly convert from floating to fixed point format such that it can be used in the Verilog code for all digits there.
# This code converts both thresholds and weights and should be the only code needed to do this conversion after training the SNN in high level using the Python script found in the "high-level-model" folder.

#Representation configuration
INTEGER_PRECISION = 16 
FLOATING_PRECISION = 40
SIGNED_BIT = 1
FP_WIDTH = INTEGER_PRECISION+FLOATING_PRECISION+SIGNED_BIT

## Dependencies:
import numpy as np
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

## Conversion of synaptic_weights
def convert_weights_between_input_and_excitatory_neurons(input_file_path, output_file_path, integer_precision, fraction_precision):
    try:
        # Read the input file
        with open(input_file_path, 'r') as f:
            lines = f.readlines()

        # Convert each line to a list of floating point numbers
        input_lists = []
        for line in lines:
            input_list = [float(entry) for entry in line[1:-2].split(',')]
            input_lists.append(input_list)
        # Transform each entry in each list
        transformed_lists = []
        for lst in input_lists:
            transformed_list = [float_to_fp(entry, integer_precision, fraction_precision) for entry in lst]
            transformed_lists.append(transformed_list)

        # Write the transformed lists to the output file
        try:
            with open(output_file_path, 'w') as f:
                for transformed_list in transformed_lists:
                    f.write("[")
                    f.write(",".join(map(str, transformed_list)))
                    f.write("]")
                    f.write("\n")
        except:
            print("Could not save transformed weights to file")

        print(f"Transformed lists saved to {output_file_path}")
    except Exception as e:
        print(f"Error: {e}")

def convert_thresholds_from_File(input_file_path, output_file_path, integer_precision, fraction_precision):
    try:
        with open(input_file_path, 'r') as f:
            lines = f.readlines()

        # Transform each entry in the list to floating point format
        transformed_list = []
        for line in lines:
            transformed_digit = float_to_fp(float(line.strip()), integer_precision, fraction_precision)
            transformed_list.append(transformed_digit)

        try:
            with open(output_file_path, 'w') as f:
                for digit in transformed_list:
                    f.write(str(digit))
                    f.write("\n")

        except:
            print("Could not save transformed thresholds to file")
                
    except Exception as e:
        print(f"Error: {e}")
        


input_file = "thresholds.txt"
output_file = "thresholds_fixed_" + str(INTEGER_PRECISION) + "_" + str(FLOATING_PRECISION) + "_fp_experiments.txt"
convert_thresholds_from_File(input_file,output_file, INTEGER_PRECISION, FLOATING_PRECISION)


input_file = "conn_X_Ae_converted_corrected.txt"
output_file = "weights_fixed_point_LFSR_to_excitatory_" + str(INTEGER_PRECISION) + "_" + str(FLOATING_PRECISION) + "_fp_experiments.txt"
convert_weights_between_input_and_excitatory_neurons(input_file,output_file, INTEGER_PRECISION, FLOATING_PRECISION)



print("localparam int INTEGER_PRECISION                    = ", str(INTEGER_PRECISION)+";")
print("localparam int WII_PRECISION                        = ", str(INTEGER_PRECISION+1)+";")
print("localparam int FLOATING_PRECISION                   = ", str(FLOATING_PRECISION)+";\n")

print("localparam int FP_WIDTH                             = ", str(FP_WIDTH)+";\n")

print("localparam leakage_cofficient_excitatory            = ", str(FP_WIDTH)+"'b"+float_to_fp(np.exp(-1/100),INTEGER_PRECISION,FLOATING_PRECISION)+";")
print("localparam leakage_cofficient_inhibitory            = ", str(FP_WIDTH)+"'b"+float_to_fp(np.exp(-1/10),INTEGER_PRECISION,FLOATING_PRECISION)+";\n")

print("localparam potent_rest_inhibitory                   = ", str(FP_WIDTH)+"'b"+float_to_fp(-60.0,INTEGER_PRECISION,FLOATING_PRECISION)+";")
print("localparam potent_reset_inhibitory                  = ", str(FP_WIDTH)+"'b"+float_to_fp(-40.0,INTEGER_PRECISION,FLOATING_PRECISION)+";")
print("localparam potent_thres_inhibitory                  = ", str(FP_WIDTH)+"'b"+float_to_fp(-45.0,INTEGER_PRECISION,FLOATING_PRECISION)+";\n")

print("localparam synapse_weight_excitatory_to_inhibitory  = ", str(FP_WIDTH)+"'b"+float_to_fp(22.5,INTEGER_PRECISION,FLOATING_PRECISION)+";")
print("localparam synapse_weight_lateral_inhibition        = ", str(FP_WIDTH)+"'b"+float_to_fp(-120.0,INTEGER_PRECISION,FLOATING_PRECISION)+";\n")

print("localparam potent_rest_excitatory                   = ", str(FP_WIDTH)+"'b"+float_to_fp(-65.0,INTEGER_PRECISION,FLOATING_PRECISION)+";")
print("localparam potent_reset_excitatory                  = ", str(FP_WIDTH)+"'b"+float_to_fp(-60.0,INTEGER_PRECISION,FLOATING_PRECISION)+";")



