//LFSR module for generating spike pattern from pixel values.

module LFSR #(
    parameter total_number_pixels = 784 
)(
    input                                           clk,
    input                                           reset,
    input                                           enable, // The enable signal is for turning on ability to switch the pointer or have spiking behaviour
    input reg [31:0]                                cycles_before_new_image,
    input reg  [31:0]                               imageArray [0:total_number_pixels-1],

    output reg [15:0]                               data,
    output reg [total_number_pixels-1:0]            spike // One spike train for each pixel value in the image
);
  
    reg [15:0]        lfsr_reg;
    reg [15:0]        counter;  // Bit width log2(cycles_before_new_image)
    reg               finish_signal; // Signals that the counter has finished and the comparison time is over for the image
    integer           i;
    assign data = lfsr_reg;

    always_ff @(posedge clk, posedge reset) begin
       if(reset) begin
        lfsr_reg <= 16'h32; //Switch to something 16-bit instead. - Previous value here was: 16'hdeadbeef, trenger å finne en god seed.
       end else if(enable) begin
             lfsr_reg[15:1] <= lfsr_reg[14:0];
             lfsr_reg[0]    <= ~(lfsr_reg[15] ^ lfsr_reg[4] ^ lfsr_reg[2] ^ lfsr_reg[1]); //Indexing here is chosen from the paper of Wenzhe Guo.
          end
    end

    // This always block contains the spike generation from the LFSR
    always @(posedge clk, posedge reset) begin
        if (reset) begin
            spike <= 0;
        end 
        else if (!finish_signal) begin
            for (i = 0; i < total_number_pixels-1; i = i + 1) begin
                if (data < imageArray[i] && enable) begin 
                    //The random generated number is smaller than the pixel value at index - i
                    spike[i] <= 1; 
                end else begin
                    spike[i] <= 0;
                end
            end

    end
    end

    //Counter block -- Needed to count cycles for each image to be compared to the LFSR register values.
    always @(posedge clk, posedge reset) begin
        if (reset) begin
            counter <= 0;
            finish_signal <= 0;
        end else if (counter < cycles_before_new_image && enable) begin 
            counter <= counter + 1; 
            finish_signal <= 0;
        end else if (counter >= cycles_before_new_image) begin
            finish_signal <= 1;
            counter <= 0;
        end
    end

endmodule

