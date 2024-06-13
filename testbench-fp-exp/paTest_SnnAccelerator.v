package paTest_SnnAccelerator;

    localparam integer CLK_HALF_PERIOD                  = 2;
    localparam integer SCK_HALF_PERIOD                  = 25;
  
    localparam integer N                                = 784;
    localparam integer M                                = 8;
  
    localparam int IMAGE_SIZE                           = 784;                  // Size of the image to infer
    localparam int IMAGE_SIZE_BITS                      = 8;
    localparam int PIXEL_MAX_VALUE                      = 255;                  // Maximum value of each pixel
    localparam int PIXEL_BITS                           = 8;


    //1 16 47
    localparam int INTEGER_PRECISION                    = 16;
    localparam int WII_PRECISION                        = 17;
    localparam int FLOATING_PRECISION                   = 47;

    localparam int FP_WIDTH                             = 64;

    
    localparam leakage_cofficient_excitatory            = 64'b0000000000000000011111101011100111110011111101001010111001110011; //e^(-1/100)
    localparam leakage_cofficient_inhibitory            = 64'b0000000000000000011100111101000110110110011001110101010010101100; //e^(-1/10)

    localparam potent_rest_inhibitory                   = 64'b1111111111100010000000000000000000000000000000000000000000000000; // -0.65mV
    localparam potent_reset_inhibitory                  = 64'b1111111111101001100000000000000000000000000000000000000000000000; // -0.45 mV 
    localparam potent_thres_inhibitory                  = 64'b1111111111101100000000000000000000000000000000000000000000000000; // -0.40 mV

    localparam synapse_weight_excitatory_to_inhibitory  = 64'b0000000000001011010000000000000000000000000000000000000000000000; // 22.5
    localparam synapse_weight_lateral_inhibition        = 64'b1111111111000100000000000000000000000000000000000000000000000000; //-120.0

    localparam potent_rest_excitatory                   = 64'b1111111111011111100000000000000000000000000000000000000000000000; // -0.65 mV
    localparam potent_reset_excitatory                  = 64'b1111111111100010000000000000000000000000000000000000000000000000; // -0.60 mV


endpackage