`timescale 1ns / 1ns

// Code heavily changed and adapted to verilog from the systemverilog code found here:
// https://github.com/jasha64/SNN-FPGA/tree/main


module LIF_neuron_2_0 # (
	//Parameterized values
    parameter
    PREV_LAYER_NEURONS = 784,
    WEIGHT_WIDTH = pa_SnnAccelerator::FP_WIDTH,
    POTENT_WIDTH = pa_SnnAccelerator::FP_WIDTH
)(
    input  clk,
    input  rst,
    input  en,

    input signed [WEIGHT_WIDTH-1 : 0] synapses_weight[PREV_LAYER_NEURONS-1 : 0], // To read weights in from file for the ASIC version. In comments are the way to do it for FPGA and RAM cells.
    input signed [POTENT_WIDTH-1 : 0] inhibitory_weights, // Inhibition upon spiking behaviour from the inhibitory neurons
    
    input  [PREV_LAYER_NEURONS-1 : 0]       spike_in,
    input reg signed [POTENT_WIDTH-1:0]     potent_thres,
    output reg signed [POTENT_WIDTH-1 : 0]  potent,  // membrane potential of this neuron
    // For debugging purposes
    output reg signed [POTENT_WIDTH-1:0]    temp_potent,
    output reg signed [POTENT_WIDTH-1:0]    q_result,    //output quantized to same number of bits as the input
    output reg signed [POTENT_WIDTH-1:0]	a,
    output reg signed [POTENT_WIDTH-1:0]	b,
    output reg                              spike_out 
);
    reg signed [POTENT_WIDTH-1 : 0] leakage_coefficient = pa_SnnAccelerator::leakage_cofficient_excitatory; 

    localparam   potent_rest  = pa_SnnAccelerator::potent_rest_excitatory;         // resting potential -0.65mV conv to 
    localparam   potent_reset = pa_SnnAccelerator::potent_reset_excitatory; // -60 mV in the high level module


    reg signed [WEIGHT_WIDTH-1 : 0] potent_in [PREV_LAYER_NEURONS-1 : 0];  // won't exceed weight width
    reg signed [POTENT_WIDTH-1 : 0] sum_potent_in;
     

    reg signed [POTENT_WIDTH-1:0]   a_thres;

    reg signed [POTENT_WIDTH-1:0]   a_adder;
    reg signed [POTENT_WIDTH-1:0]   b_adder;
    
    
    reg         refrac_en;
    reg [3:0]   refrac_timer;  // refractory period
    localparam  refrac_len = 'd5; // Initially 5 in the neuron v but here it is 5

    reg			                    overflow;    //signal to indicate output greater than the range of our format
    wire [POTENT_WIDTH-1:0] adder_out [PREV_LAYER_NEURONS-1:0];

    reg signed [2*POTENT_WIDTH-1:0] mult_result;
    reg signed [POTENT_WIDTH-1:0]   shifted_mult;
    

    always @*
    begin
        for (integer i = 0; i < PREV_LAYER_NEURONS; i = i+1)
            potent_in[i] = spike_in[i] ? synapses_weight[i] : 0;
    end

    always @*
    begin
        sum_potent_in = 0;
        for (integer i = 0; i < PREV_LAYER_NEURONS; i = i+1)
            sum_potent_in = sum_potent_in + potent_in[i];
        sum_potent_in = sum_potent_in + inhibitory_weights; // Add the inhibitory voltage when it is set.
    end

    always @*
    begin
        a = potent - potent_rest; // Update the potential at all times but only read the result when needed
    end

 
    always @ (posedge clk)
    begin
        if (rst) begin
            potent    <= potent_rest;
            spike_out <= 0;
            refrac_en    <= 0;
            refrac_timer <= 0;

        end
        else if (en) begin
            if (refrac_en == 1'b0 && spike_out == 1'b0) begin // We also use the spike_out as condition here since it flags one clock before and we want no integration at spike from the neuron
                potent <= q_result + potent_rest + sum_potent_in; 
                if (potent >= potent_thres) begin
                    spike_out <= 1'b1;  // trigger a spike
                    //potent    <= potent_reset;
                end
            end
            else begin  // in refractory period
                if (spike_out == 1'b1) begin
                    refrac_en <= 1'b1;  // enter refractory period in next clock
                    potent <= potent_reset; // Set the voltage to the reset voltage after spiking
                    spike_out <= 1'b0;
                end else begin
                    potent    <= q_result + potent_rest; //Before it was just potent but now instead the neuron leakes in refractory period since the high level model includes this. potent;
                end
                if (refrac_timer == refrac_len - 1) begin  // end of refractory period
                    refrac_en    <= 1'b0;
                    refrac_timer <= 0;
                end
                else if (refrac_en) refrac_timer <= refrac_timer + 1'b1;
            end
        end 
    end

    qmult leakage_multiplier (
        .ina(a),
        .inb(leakage_coefficient), // Will always just multiply by the leakage coefficient as the b
        .out(q_result),    //output quantized to same number of bits as the input
        .overflow(overflow)

    );
    
endmodule