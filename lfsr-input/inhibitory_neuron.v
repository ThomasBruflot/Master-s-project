`timescale 1ns / 1ns

// Code heavily changed and adapted to verilog from the systemverilog code found here:
// https://github.com/jasha64/SNN-FPGA/tree/main


module inhibitory_neuron # (
	//Parameterized values
    parameter

    PREV_LAYER_NEURONS = 100,
    WEIGHT_WIDTH = pa_SnnAccelerator::FP_WIDTH,
    POTENT_WIDTH = pa_SnnAccelerator::FP_WIDTH
)(
    input                                   clk,
    input                                   rst,
    input                                   en,
    input                                   spike_in, // Only receive from one excitatory neuron

    output reg                              spike_out 
);


    localparam signed  synapse_weight         = pa_SnnAccelerator::synapse_weight_excitatory_to_inhibitory;
    localparam signed  potent_rest            = pa_SnnAccelerator::potent_rest_inhibitory; // resting potential -60 mV 
    localparam signed  potent_reset           = pa_SnnAccelerator::potent_reset_inhibitory; // -45 mV in the high level module
    localparam signed  potent_thres           = pa_SnnAccelerator::potent_thres_inhibitory; // -40 mV in high level module
    localparam signed  leakage_coefficient    = pa_SnnAccelerator::leakage_cofficient_inhibitory; // 0.9904 in high level module
    
    
    reg signed [POTENT_WIDTH-1:0]   q_result;    //output quantized to same number of bits as the input
    reg signed [POTENT_WIDTH-1:0]	a;
    reg signed [POTENT_WIDTH-1:0]	b;

    reg signed [WEIGHT_WIDTH-1 : 0] potent_in;  // won't exceed weight width
    reg signed [POTENT_WIDTH-1 : 0] sum_potent_in;
    reg signed [POTENT_WIDTH-1 : 0] potent; // membrane potential of this neuron
    
    
    reg         refrac_en;
    reg [3:0]   refrac_timer;  // refractory period
    localparam  refrac_len = 'd2; // Initially 5 in the neuron v but here it is 5


    reg	overflow;    //signal to indicate output greater than the range of our format from the multiplier

    

    always @*
    begin
        potent_in = spike_in ? synapse_weight : 0;
    end


    always @*
    begin
        sum_potent_in = 0;
        sum_potent_in = sum_potent_in + potent_in;
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