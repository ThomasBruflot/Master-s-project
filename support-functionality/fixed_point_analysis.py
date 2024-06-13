# This code file contains functions to convert between floating point and fixed point to analyze this before deploying it into my hardware SNN design.
# Source of the functions: https://thedatabus.io/fixed-point
import math
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



print(float_to_fp(-20.5,7,12))
    
print("a:   ", fp_to_float('00001001100000000000',7,12))
print("b:   ", fp_to_float('00000011000100000000',7,12))

print("a*b: ", fp_to_float('00011101000110000000',7,12))


print("a:   ", fp_to_float('11101011100000000000',7,12))
print("b:   ", fp_to_float('00000011000100000000',7,12))

print("a*b: ", fp_to_float('11000000100111000000',7,12))

print("Representing the constants in my neuron model: ")

print("-65.0 mV can be represented as: ", float_to_fp(-65.0,16,47))
print("-60.0 mV can be represented as: ", float_to_fp(-60.0,16,47))
print("-52.0 mV can be represented as: ", float_to_fp(-52.0,16,47))



print("Weights converted (10 samples - later on make a full conversion and store to file)")
print("0.0000000088587 can be represented as: ", float_to_fp(0.0000000088587,16,47))
print("Converted back: ", fp_to_float(float_to_fp(0.0000000088587,16,47),16,47))
print("0.0000000000167 can be represented as: ", float_to_fp(0.0000000000167,16,47))
print("0.0000000000429 can be represented as: ", float_to_fp(0.0000000000429,16,47))
print("0.0000000000095 can be represented as: ", float_to_fp(0.0000000000095,16,47))
print("0.0000000031291 can be represented as: ", float_to_fp(0.0000000031291,16,47))
print("0.0000000000482 can be represented as: ", float_to_fp(0.0000000000482,16,47))
print("0.0000000000531 can be represented as: ", float_to_fp(0.0000000000531,16,47))
print("0.0000000063594 can be represented as: ", float_to_fp(0.0000000063594,16,47))
print("0.0000004422546 can be represented as: ", float_to_fp(0.0000004422546,16,47))
print("0.0000000003258 can be represented as: ", float_to_fp(0.0000000003258,16,47))

print("This is the threshold has as value:      ", fp_to_float("1111011110101110000101000111101011100001010001111010111000000000",16,47))
print("This is the resting has as value:        ", fp_to_float("1111010110011001100110011001100110011001100110011001100110000000",16,47))

print("This is the old leakage coefficient written in fixed point format 1 10 53: ", float_to_fp(0.95,16,47))
print("This is the new leakage coefficient written in fixed point format 1 10 53: ", float_to_fp(0.9900498337491681,16,47))

print("This is the threshold leakage coefficient written in fixed point format 1 10 53: ", float_to_fp(0.999999900000005,16,47))
print("This is the theta plus written in fixed point format 1 10 53: ", float_to_fp(0.05,16,47))


print(math.exp(-1/100))
print(math.exp(-1/10000000))

print(2**10)

print(64-1-10)

print("5.32 mV can be represented as: ", float_to_fp(5.32,16,47))
print("-0.99 can be represented as: ", float_to_fp(-0.99,16,47))


print("Inhibitory params:")
print("-60.0 can be represented as: ", float_to_fp(-60.0,16,47))
print("-40.0 can be represented as: ", float_to_fp(-40.0,16,47))
print("-45.0 can be represented as: ", float_to_fp(-45.0,16,47))
print("leakage coefficient for this neuron: ", np.exp(-1/10))
print("Leakage in fixed point:      ", float_to_fp(np.exp(-1/10),16,47))
print("synaptic weight of 22.5 in fixed point: ", float_to_fp(22.5,16,47))
print("synaptic weight of -120.0 in fixed point: ", float_to_fp(-120.0,16,47))
print("synaptic weight of -17.5.0 in fixed point: ", float_to_fp(-17.5,16,47))


print("Debug weights 16 47: ", fp_to_float("0000000000000000000000000000000000000000000100110000011000011111",16,47))
print("Debug weights 10 53: ", fp_to_float("0000000000000000000000000000000000000100110000011000011111001100",10,53))