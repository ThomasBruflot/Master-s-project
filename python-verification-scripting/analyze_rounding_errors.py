# This file contains code to figure out the rounding error of the synaptic weights in the SNN such that a comparison of the error is shown in the report
# I need to read in the synaptic weights from the original file and from different fixed point files and convert the fixed point ones to decimal again and then compare.

## Dependencies:
import numpy as np
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

## Conversion of synaptic_weights
def convert_weights_between_input_and_excitatory_neurons(input_file_path, output_file_path, integer_precision, fraction_precision):
    try:
        # Read the input file
        with open(input_file_path, 'r') as f:
            lines = f.readlines()

        # Convert each line to a list of floating point numbers
        input_lists = []
        for line in lines:
            #print(line[1:-2])
            input_list = [float(entry) for entry in line[1:-2].split(',')]
            input_lists.append(input_list)
        #print(input_list)
        # Transform each entry in each list
        transformed_lists = []
        for lst in input_lists:
            transformed_list = [float_to_fp(entry, integer_precision, fraction_precision) for entry in lst]
            transformed_lists.append(transformed_list)
        #print("tr ", transformed_list)

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


def load_synaptic_weights(input_file_path, integer_precision, fraction_precision):
    try:
        # Read the input file
        with open(input_file_path, 'r') as f:
            lines = f.readlines()

        # Convert each line to a list of floating point numbers
        input_lists = []
        for line in lines:
            #print(line[1:-2])
            input_list = [float(entry) for entry in line[1:-2].split(',')]
            input_lists.append(input_list)

        rounded_lists = []
        for lst in input_lists:
            transformed_list = [float_to_fp(entry, integer_precision, fraction_precision) for entry in lst]   
            transformed_back_list = [fp_to_float(entry, integer_precision, fraction_precision) for entry in transformed_list]
            rounded_lists.append(transformed_back_list)


        #print(rounded_lists[0][20])
        #print(input_lists[0][20])

        return input_lists, rounded_lists
    except Exception as e:
        print(f"Error: {e}")

INTEGER_PRECISION = 16
FRACTIONAL_PRECISION = 47
original_weights, rounded_weights = load_synaptic_weights("conn_X_Ae_converted_corrected.txt", INTEGER_PRECISION, FRACTIONAL_PRECISION)

def get_rounding_errors(original_weights, rounded_weights):
    total_diff_array = []
    for i in range(0,len(original_weights)):
        diff_array = []
        for k in range(0,len(original_weights[0])):
            diff_array.append(np.abs(original_weights[i][k]-rounded_weights[i][k]))
        total_diff_array.append(diff_array)
    #print(total_diff_array[0])
    return total_diff_array

rounding_errors_per_weight_per_neuron = get_rounding_errors(original_weights, rounded_weights)

def visualize_max_errors_per_neuron(rounding_errors):
    #maximum_error_per_neuron = []
    #for array in rounding_errors:
    #    maximum_error_per_neuron.append(max(array))
    c = "red"
    c2 = "black"
    _fig = plt.figure()
    plt.xlabel('Neuron index', fontdict = {'fontsize' : 14})
    plt.ylabel('Log10(Rounding errors)', fontdict = {'fontsize' : 14})
    title_string = 'Logarithmic boxplot of rounding errors with ' + str(FRACTIONAL_PRECISION) + ' fractional bits'
    plt.title(title_string, fontdict = {'fontsize' : 18})
    plt.gca().set_xticklabels([str(i) if i % 5 == 0 else '' for i in range(1,101)])
    plt.boxplot(np.log10(np.array(rounding_errors)).T, notch=False, patch_artist=True,
            #boxprops=dict(facecolor=c, color=c2),
            boxprops=dict(color=c2),
            capprops=dict(color=c2),
            whiskerprops=dict(color=c2),
            flierprops=dict(marker='o', markersize=4, color=c, markeredgecolor=c),
            medianprops=dict(markersize = 10, color=c), 
            )
    plt.show()

visualize_max_errors_per_neuron(rounding_errors_per_weight_per_neuron)


# Boxplot of original weights distribution to understand impact of rounding


def visualize_synaptic_weight_strength_per_neuron(original_weights):
    #maximum_error_per_neuron = []
    #for array in rounding_errors:
    #    maximum_error_per_neuron.append(max(array))
    c = "red"
    c2 = "black"
    _fig = plt.figure()
    plt.xlabel('Neuron index')
    plt.ylabel('Log10(Synaptic weight strength)')
    title_string = 'Logarithmic boxplot of synaptic weight strength per neuron'
    plt.title(title_string, fontdict = {'fontsize' : 18})
    plt.gca().set_xticklabels([str(i) if i % 5 == 0 else '' for i in range(1,101)])
    #plt.boxplot(np.emath.logn(100, original_weights).T, notch=False, patch_artist=True,
    plt.boxplot(np.log10(np.array(original_weights)).T, notch=False, patch_artist=True,
        boxprops=dict(facecolor="gray", color=c2),
        capprops=dict(color=c2),
        whiskerprops=dict(color=c2),
        flierprops=dict(marker='o', markersize=4, color=c, markeredgecolor=c),
        medianprops=dict(markersize = 10, color=c)
        )
    plt.show()

#visualize_synaptic_weight_strength_per_neuron(original_weights)



def visualize_synaptic_weight_strength_histogram(original_weights):
    _fig = plt.figure()
    plt.xlabel('Synaptic weight strength',fontdict={'fontsize': 14})
    plt.ylabel('Number of weights in the bin - Logarithmicly scaled',fontdict={'fontsize': 14})
    title_string = 'Histogram of synaptic weight strength'
    plt.title(title_string, fontdict={'fontsize': 18})
    
    # Use a logarithmic scale if the data spans several orders of magnitude
    plt.yscale('log')
    
    # Adjust the number of bins to better suit the data range and distribution
    num_bins = 200  # You can adjust this number based on your specific dataset
    
    # Use scientific notation for better readability
    #plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
    
    # Create histogram
    plt.hist(original_weights, bins=num_bins)#, alpha=0.75)
    
    plt.show()
#visualize_synaptic_weight_strength_histogram(original_weights)

#flat_weights = np.array(original_weights).flatten()
#print("Average: ", np.average(flat_weights))
#print("Median: ", np.median(flat_weights))
#print("Standard deviation: ", np.std(flat_weights))



print(len(original_weights))
print(len(original_weights[0]))

print(len(rounding_errors_per_weight_per_neuron))
print(len(rounding_errors_per_weight_per_neuron[0]))

def visualize_rounding_errors_for_fractional_bits():
    full_rounding_error_array_for_all_fractional_precisions_flat = []
    x_axis = []
    for fractional_bits in range(4,48):
        x_axis.append(fractional_bits)
        original_weights = []
        rounded_weights = []
        original_weights, rounded_weights = load_synaptic_weights("conn_X_Ae_converted_corrected.txt", INTEGER_PRECISION, fractional_bits)
        rounding_errors_per_weight_per_neuron_np = np.array(get_rounding_errors(original_weights, rounded_weights)).flatten()
        full_rounding_error_array_for_all_fractional_precisions_flat.append(rounding_errors_per_weight_per_neuron_np)
    c = "red"
    c2 = "black"
    _fig = plt.figure()
    plt.xlabel('Number of fractional bits')
    plt.ylabel('Log10(Rounding errors)')
    title_string = 'Logarithmic boxplot of rounding errors using different fractional precisions'
    plt.title(title_string, fontdict = {'fontsize' : 18})
    plt.boxplot(np.log10(np.array(full_rounding_error_array_for_all_fractional_precisions_flat)).T, positions=x_axis, notch=False, patch_artist=True,
            #boxprops=dict(facecolor=c, color=c2),
            boxprops=dict(color=c2),
            capprops=dict(color=c2),
            whiskerprops=dict(color=c2),
            flierprops=dict(marker='o', markersize=4, color=c, markeredgecolor=c),
            medianprops=dict(markersize = 10, color=c), 
            )
    plt.show()

#visualize_rounding_errors_for_fractional_bits()
