//====================================================================
//        Copyright (c) 2023 Nordic Semiconductor ASA, Norway
//====================================================================
// Created : thob at 2024-02-28
//====================================================================

//This module will later connect input images to poisson generators to weight accumulators to neurons and so on.
//First iteration will contain one weight accumulator and one neuron connected.
//Second iteration will contain the poisson generator, one weight accumulator and one neuron connected.

module SNN_top #(
    parameter number_of_neurons = 100,
    parameter total_number_pixels = 784,
    parameter PREV_LAYER_NEURONS = 784, // One comparator for each input pixel to the LFSR.
    parameter WEIGHT_WIDTH = pa_SnnAccelerator::FP_WIDTH,
    parameter POTENT_WIDTH = pa_SnnAccelerator::FP_WIDTH
    )(
    input                                       clk,
    input                                       reset,

    input reg [31:0]                            cycles_before_new_image,
    input                                       generator_enable, // Comes from testbench
    input                                       en, // Enable for the excitatory neurons
    input signed [WEIGHT_WIDTH-1:0]             synapses_weight [number_of_neurons-1:0][total_number_pixels-1:0],
    input signed [POTENT_WIDTH-1:0]             potent_thres [number_of_neurons-1:0],
    input [31:0]                                imageArray [total_number_pixels-1:0], // Comes from testbench, move from LFSR_tb to SNN_top tb.
    input [total_number_pixels-1:0]             spikes,

    
    output wire [number_of_neurons-1:0]         output_spikes_from_excitatory_layer,
    output wire [number_of_neurons-1:0]         output_spikes_from_inhibitory_layer,
    output wire [POTENT_WIDTH-1:0]              potentials_recording [number_of_neurons-1:0], // To read out the potentials to file
    // For debugging purposes
    output wire [POTENT_WIDTH-1:0]              temp_potent [number_of_neurons-1:0],
    output wire [POTENT_WIDTH-1:0]              q_result [number_of_neurons-1:0],    //output quantized to same number of bits as the input
    output wire [POTENT_WIDTH-1:0]	            a [number_of_neurons-1:0],
    output wire [POTENT_WIDTH-1:0]	            b [number_of_neurons-1:0],
    output signed [POTENT_WIDTH-1:0]            converted_potential
);

localparam signed inhibition_strength = pa_SnnAccelerator::synapse_weight_lateral_inhibition; // Here I use -120 another used one (not here) is -17.5 = 64'b1111111111110111010000000000000000000000000000000000000000000000;

//WTA CIRCUIT - find all excitatory that spiked first and then inhibit all others.
reg [number_of_neurons-1:0] can_spike;
reg [number_of_neurons-1:0] transition_indices;
reg enable_WTA;// Initialize the enable to 1 - this controls if we can look for initial spikes for the WTA.
integer k; 
initial begin
    can_spike = {100{1'b1}}; // Set all bits to 1
    transition_indices = {100{1'b0}}; // Set all bits to 0 initially
end

always @(posedge clk) begin
    if(reset) begin 
        enable_WTA <= 1'b0; //Set to 1 to have WTA action - turned off for now.
        can_spike <= {100{1'b1}}; 
        transition_indices = {100{1'b0}}; // Set all bits to 0 initially at reset
    end else if (enable_WTA) begin
        for (k=0; k < number_of_neurons; k = k+1) begin
            if (output_spikes_from_excitatory_layer[k] == 1'b1) begin
                // Mark the index where the transition occurred
                transition_indices[k] <= 1;
                enable_WTA   <= 1'b0;
            end else begin
                // No transition at this index
                transition_indices[k] <= 1'b0; // Not strictly necessary
            end
        end
    end        
    // Here I set can_spike to map to transition indices if any of them spiked.
    if (enable_WTA == 1'b0 && transition_indices) begin
        can_spike <= transition_indices; 
    end

end

//wire [total_number_pixels-1:0] spikes;
genvar i;
reg [POTENT_WIDTH-1:0] inhibitory_weights_accumulated [number_of_neurons-1:0];

// --------------------------------------
//  This section is for randomly choosing one of the output spikes from the excitatory layer and turning of all others. 
reg [6:0] random_number;
reg [6:0] number_of_spikes_at_time_step;
reg [6:0] iterator_for_chosen_spike_index;
//reg [7:0] indices_that_spiked [number_of_neurons-1:0];
reg [number_of_neurons-1:0] updated_spikes; // after randomly choosing one spike from the group of spikes from the excitatory layer
 
LFSR_one_spike_picker spike_picker(
    .clk(clk),
    .reset(reset),
    .enable(en),
    .random_number(random_number)
);

always @(output_spikes_from_excitatory_layer)
begin
    number_of_spikes_at_time_step = 0;
    iterator_for_chosen_spike_index = 0;
    for (integer l = 0; l < number_of_neurons; l=l+1) begin
        if (output_spikes_from_excitatory_layer[l]) begin
            number_of_spikes_at_time_step = number_of_spikes_at_time_step + 1;

        end
    end 
    iterator_for_chosen_spike_index = random_number % number_of_spikes_at_time_step; // Eg random number is 47 then modulo 3 gives 2 
    // Choose then eg number 3 of the spikes in order from 0 to 100. so say neuron 40, 60 and 74 spiked then I choose 74 but if the modulo gave 1 I would choose 60 and if it gave out 0 I would choose 40.
    for (integer s = 0; s < number_of_neurons; s=s+1) begin
        if (output_spikes_from_excitatory_layer[s]) begin
            if (iterator_for_chosen_spike_index == 0) begin
                updated_spikes[s] = 1;
                iterator_for_chosen_spike_index = 100; // just to kill it off so no other spikes after this
            end else begin
                iterator_for_chosen_spike_index = iterator_for_chosen_spike_index - 1;
                updated_spikes[s] = 0;
            end
        end else begin
            updated_spikes[s] = 0;
        end
    end
end

// --------------------------------------

//LFSR input_image_encoder (
//    .clk(clk),
//    .reset(reset),
//    .cycles_before_new_image(cycles_before_new_image),
//    .enable(generator_enable),
//    .imageArray(imageArray),
//    .spike(spikes)
//
//);

//fxp2float converter(
//    .in(potentials_recording[0]),
//    .out(converted_potential)
//);
always @ (output_spikes_from_inhibitory_layer)
begin
    // Initialize the inhibition
    for (integer j = 0; j < number_of_neurons; j=j+1) begin
        inhibitory_weights_accumulated[j] = 0;

    end


    for (integer i = 0; i < number_of_neurons; i = i+1) begin
        if(output_spikes_from_inhibitory_layer[i]) begin
            for (integer k = 0; k < number_of_neurons; k=k+1) begin
                if (k != i) begin
                    inhibitory_weights_accumulated[k] += inhibition_strength;
                end
            end
        end
        
    end
end

generate
    for (i = 0; i < number_of_neurons; i = i + 1) begin

        wire [total_number_pixels-1:0] local_spikes; // one wire collection per neuron
        // Conditionally assign the spikes signal based on can_spike to ensure WTA behaviour
        assign local_spikes = can_spike[i] ? spikes : 0; // or whatever default value you want when can_spike[i] is 0

        LIF_neuron_2_0 neuron_instance (
            .clk(clk),
            .rst(reset),
            .en(en),
            .synapses_weight(synapses_weight[i]), // One group of weights per neuron in the network.
            .inhibitory_weights(inhibitory_weights_accumulated[i]),
            .spike_in(local_spikes),
            .potent_thres(potent_thres[i]),
            .potent(potentials_recording[i]),
            .temp_potent(temp_potent[i]),
            .q_result(q_result[i]),
            .a(a[i]),
            .b(b[i]),
            .spike_out(output_spikes_from_excitatory_layer[i])
        );

        inhibitory_neuron inhibitory_neuron_instance (
            .clk(clk),
            .rst(reset),
            .en(en),
            .spike_in(updated_spikes[i]),
            .spike_out(output_spikes_from_inhibitory_layer[i])
        );

    end
endgenerate



endmodule


