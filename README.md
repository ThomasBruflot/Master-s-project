# Master-s-project
Project made in relation to my Master's thesis at NTNU Spring semester 2024. The project is a Spiking Neural Network ASIC implementation in Verilog based on a high level model made in Python. Additionally the project includes supporting functionality made in Python.

The folder "fp-exp" contains the design used for fixed point experiments where the fixed point fractional bit width was altered and the effects were studied. 

The folder "lfsr-input" contains the SNN hardware design that used lfsr input encoding.

The "synthesized-design" folder contains the design used to do area estimates and power estimates. It can be modified to include interface input spikes or lfsr input encoding.

The two testbench folders contains testbenches and packages for the fixed point experiments design and the lfsr input encoding design.

The "operator" folder contains the multiplier module used for fixed point multiplication.

The "high-level-model" folder contains the Python implementation of the SNN and the code needed to extract weights, threshold values, neuron assignments and input encoding from the high level Poisson encoder.

The "plotting" folder contains scripts for plotting some of the results.

The "python-verification-scripting" folder contains various scripts used to verify the SNN design and the high level model in Python.