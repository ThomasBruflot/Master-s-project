

//LFSR module for choosing randomly one of the spiking neurons per time step.


module LFSR_one_spike_picker #(
    parameter total_number_pixels = 10 
)(
    input                                           clk,
    input                                           reset,
    input                                           enable, // The enable signal is for turning on spike_index_finding                                           
    output reg [6:0]                                random_number // Used to choose which index will be 1
);
  
    reg [6:0]        lfsr_reg;
    integer           i;
    assign random_number = lfsr_reg >= 7'd100 ? 7'd100 : lfsr_reg; // Cap output to 100.

    always_ff @(posedge clk, posedge reset) begin
       if(reset) begin
        lfsr_reg <= 7'd53; //Seed
       end else if(enable) begin
             lfsr_reg[6:1] <= lfsr_reg[5:0];
             lfsr_reg[0]    <= ~(lfsr_reg[6] ^ lfsr_reg[4] ^ lfsr_reg[0]); 

          end
    end



endmodule

