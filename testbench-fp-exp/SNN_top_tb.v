// Testbench for the SNN Verilog module used for fixed point experiments
module SNN_top_tb #(
  parameter total_number_pixels = 784,
  parameter PREV_LAYER_NEURONS = 784, // One comparator for each input pixel to the LFSR.
  parameter WEIGHT_WIDTH = paTest_SnnAccelerator::FP_WIDTH,
  parameter POTENT_WIDTH = paTest_SnnAccelerator::FP_WIDTH,
  parameter number_of_excitatory_neurons = 100,
  parameter number_of_input_spike_trains = 10000
  )();

    // DUT Input signals
    reg                                         clk_in;
    reg                                         reset_in;
    reg                                         generator_enable_in; // Comes from testbench
    reg                                         en_in; // Enable for the excitatory neurons
    reg signed [POTENT_WIDTH-1:0]               potent_thresholds_from_file [number_of_excitatory_neurons-1:0];
    reg [31:0]                                  imageArray_in [0:total_number_pixels-1]; // Comes from testbench, move from LFSR_tb to SNN_top tb.
    reg [number_of_excitatory_neurons-1:0]      output_spikes_from_excitatory_layer_register;
    reg [number_of_excitatory_neurons-1:0]      output_spikes_from_inhibitory_layer_register;
    reg [POTENT_WIDTH-1:0] potentials_recording [number_of_excitatory_neurons-1:0]; // To read out the potentials to file

    reg [WEIGHT_WIDTH-1:0]                      test_weights [number_of_excitatory_neurons-1:0][total_number_pixels-1:0];  //[0:100][0:783];
    integer                                     fileWeights;
    integer                                     number_of_weights_per_array;
    integer                                     file;
    integer                                     fileLabel;
    integer                                     fileImg;
    integer                                     file_assignments;
    integer                                     images_to_test;
    integer                                     number_of_weight_arrays; // 100 because there are 100 excitatory neurons for the LFSR to connect to and then there are 784 connections to each neuron one for each pixel value in the image. All image pixels are fed to each excitatory neuron.
    string                                      file_name;
    integer                                     img;
    integer                                     test_images[0:10000][0:783];
    integer                                     test_image[0:783];
    reg [paTest_SnnAccelerator::PIXEL_BITS-1:0] IMAGE [0:paTest_SnnAccelerator::IMAGE_SIZE-1];
    integer                                     NEW_IMAGE;
    integer                                     num_items;
    integer                                     test_labels[0:10000]; 
    reg [31:0]                                  spike_count [number_of_excitatory_neurons-1:0]; // Array to hold the spike count for each index
    reg [31:0]                                  max_spike_index;
    reg [31:0]                                  max_spike_count;
    reg                                         reset_count;
    integer                                     neuron_assignments [number_of_excitatory_neurons-1:0];
    integer                                     classified_digit;
    reg                                         correct_classification;
    integer                                     number_of_correct_classifications;
    integer                                     pseudo_number_of_correct_classifications;
    reg [31:0]                                  classified_label;
    reg [31:0]                                  total_number_of_spikes;
    integer                                     filePotentials;
    string                                      file_name_potentials;
    integer                                     index_to_store_potential = 23;//17;
    real                                        converted_potential_real;
    reg signed [POTENT_WIDTH-1:0]               converted_potential;
    integer                                     fileThresholds;
    string                                      file_name_thresholds;
    reg [31:0]                                  cycles_before_new_image;

    // For debugging purposes
    reg signed [POTENT_WIDTH-1:0]               temp_potent_rec  [number_of_excitatory_neurons-1:0];
    reg signed [POTENT_WIDTH-1:0]               q_result_rec  [number_of_excitatory_neurons-1:0];    //output quantized to same number of bits as the input
    reg signed [POTENT_WIDTH-1:0]	              a_rec [number_of_excitatory_neurons-1:0];
    reg signed [POTENT_WIDTH-1:0]	              b_rec [number_of_excitatory_neurons-1:0];
    reg [total_number_pixels-1:0]               input_spikes;
    reg [49:0]                                  input_spike_trains_parsed [number_of_input_spike_trains-1:0][total_number_pixels-1:0];
    reg                                         start_inputting;
    reg                                         start_counting = 0;
    integer                                     input_counter;
    integer                                     spike_train_pointer = 0;
    
    
    // Instantiate the DUT (Device Under Test)
    SNN_top DUT (
        .clk(clk_in),
        .reset(reset_in),
        .cycles_before_new_image(cycles_before_new_image),
        .generator_enable(generator_enable_in),
        .en(en_in),
        .synapses_weight(test_weights), // one read from test_weights at a time then. This could be issue with transfer to reg signed [31:0] from integer tbh. Will need to sort.
        .potent_thres(potent_thresholds_from_file),
        .imageArray(test_image), // Try to feed it in as integer to a 31 bit register - maybe it works
        .spikes(input_spikes),
        .output_spikes_from_excitatory_layer(output_spikes_from_excitatory_layer_register),
        .output_spikes_from_inhibitory_layer(output_spikes_from_inhibitory_layer_register),
        .potentials_recording(potentials_recording),
        .temp_potent(temp_potent_rec),
        .q_result(q_result_rec),
        .a(a_rec),
        .b(b_rec),
        .converted_potential(converted_potential)
    );


    initial begin
        clk_in = 0; // Set the initial value of the clock to 0
        number_of_correct_classifications = 0;
        pseudo_number_of_correct_classifications = 0;
        input_counter = 0;
    end

    // Clock generation - toggle the clock every 1 time unit.
    always #1 clk_in = ~clk_in;


    // Task to count spikes for each index
    task automatic count_spikes(
      input reg [number_of_excitatory_neurons-1:0] spikes
    );
      integer i;
      begin
          for (i = 0; i < number_of_excitatory_neurons; i = i + 1) begin
              spike_count[i] = spike_count[i] + spikes[i];
          end
      end
    endtask

    // Task to find the index with the most spikes
    task automatic find_max_spike_index(
      output reg [31:0] index,
      output reg [31:0] count
    );
      integer i;
      begin
          index = 0;
          count = 0;
          for (i = 0; i < number_of_excitatory_neurons; i = i + 1) begin
              if (spike_count[i] > count) begin
                  index = i;
                  count = spike_count[i];
              end
          end
      end
    endtask

    //Parse neuron assignments from file - only need to do this once
    task automatic read_neuron_assignments
      (
      input string file_name,
      input integer array_depth
      );
      file_assignments = $fopen(file_name, "r");
      if (file_assignments != 0) begin
        for (int i = 0; i < array_depth; i = i + 1) begin
          num_items = $fscanf(file_assignments, "%d", neuron_assignments[i]);
          $display("Neuron [%d] maps to: %d", i, neuron_assignments[i]);
          if (num_items == 0)
            break;
        end
      end else begin
        $display("Error opening the file for neuron assignment reading");
      end
    endtask

    


    // Always block to call the count_spikes task on every clock cycle
    always @(posedge clk_in) begin
      if (reset_count) begin
          // Reset spike counts
          integer j;
          for (j = 0; j < number_of_excitatory_neurons; j = j + 1) begin
              spike_count[j] <= 0;
          end
          max_spike_index <= 0;
          max_spike_count <= 0;
      end else begin
          count_spikes(output_spikes_from_excitatory_layer_register);
      end
      
      if (start_inputting == 1) begin
        input_one_set_of_spikes_to_SNN();
      end
      if (start_counting == 1) begin
        input_counter <= input_counter + 1;
      end
    end
    
    task automatic write_potentials_to_file (
      input string file_name,
      input integer index_to_store
    );
    filePotentials = $fopen(file_name, "a");
    if (filePotentials != 0) begin
      $fwrite(filePotentials, "%b \n", potentials_recording[index_to_store]);
      $fclose(filePotentials);
    end else begin
      $display("Error opening the file for potentials writing");
    end
  
    endtask

    task automatic sum_spikes_over_labels_and_classify (
      input integer image_number,
      output reg [31:0] classified_label,
      output reg [64:0] total_number_of_spikes // number_of_spikes_from_all_neurons_with_neuron_assignment_for_classified_label
    );
    integer l; // For looping over the possible labels
    integer i; // For looping through the neuron assignment register
    integer s; // for printing all spike counts for debug
    reg [64:0] sum_per_label [9:0]; // Total amount of spikes per label in the dataset
    reg [64:0] largest_sum_found = 0;
    reg [64:0] second_largest_sum_found = 0;
    reg [64:0] third_largest_sum_found = 0;
    reg [9:0] label_with_largest_sum = 0; // The label that had the highest total amount of spikes from the excitatory neurons assigned to that label
    reg [9:0] label_with_second_largest_sum = 0;
    reg [9:0] label_with_third_largest_sum = 0;
    for(l=0; l < 10; l = l+1) begin // Loop through each possible label for the dataset
      sum_per_label[l] = 0; // Initialize the sum to zero
      for (i = 0; i < number_of_excitatory_neurons; i = i+1) begin // Then I group the neurons assigned to this label by scanning the neuron assignment register
        if (neuron_assignments[i] == l) begin
          sum_per_label[l] = sum_per_label[l] + spike_count[i]; // If the neuron belongs to this label we add the spike count to the total sum.
        end
      end
      $display("Spike count for label %d = %d", l, sum_per_label[l]);
      if (sum_per_label[l] > largest_sum_found) begin
        //$display("The sum was larger than the previous sum! The largest sum_found was previously: %d", largest_sum_found);
        largest_sum_found = sum_per_label[l];
        //$display("The sum was larger than the previous sum! The largest sum_found was updated to: %d", largest_sum_found);
        label_with_largest_sum = l;
      end else if (sum_per_label[l] > second_largest_sum_found) begin // For debug purposes
        second_largest_sum_found = sum_per_label[l];
        label_with_second_largest_sum = l;
      end else if (sum_per_label[l] > third_largest_sum_found) begin
        third_largest_sum_found = sum_per_label[l];
        label_with_third_largest_sum = l;
      end

    end

    $display("Top three: %d %d %d",label_with_largest_sum, label_with_second_largest_sum, label_with_third_largest_sum);
    if (test_labels[image_number] == label_with_largest_sum || test_labels[image_number] == label_with_second_largest_sum || test_labels[image_number] == label_with_third_largest_sum) begin
      pseudo_number_of_correct_classifications += 1;
    end 

    classified_label = label_with_largest_sum;
    total_number_of_spikes = sum_per_label[label_with_largest_sum];
    $display("The classified digit of the SNN is: %d", classified_label);
    $display("The total number of spikes for this label was: %d", total_number_of_spikes);
    $display("The actual label for this image is: %d", test_labels[image_number]);
    if (test_labels[image_number] == classified_label) begin
      correct_classification = 1;
      number_of_correct_classifications = number_of_correct_classifications + 1;
    end else begin
      correct_classification = 0;
    end
    $display("The classified digit of the SNN was correct or not 1/0: %b", correct_classification);
    endtask

  
  // Parse thresholds separated by new line in file
  task automatic parse_thresholds (
    input string file_name,
    input integer number_of_thresholds);

    fileThresholds = $fopen(file_name, "r");
    if (fileThresholds != 0) begin
      for (int i = 0; i < number_of_thresholds; i = i + 1) begin
        num_items = $fscanf(fileThresholds, "%b", potent_thresholds_from_file[i]);
        if (num_items == 0)
          break;
      end
      $fclose(fileThresholds);
    end else begin
      $display("Error opening the file for thresholds parsing");
    end
  endtask


    // Parse weights separated by new line
    task automatic parse_weights (
        input string file_name,
        input integer array_number,
        input integer array_depth);
    
        fileWeights = $fopen(file_name, "r");
        if (fileWeights != 0) begin
          // Read and parse the text fileImg
          for (int i = 0; i < array_number; i++) begin
            for (int j = 0; j < array_depth; j++) begin
              if (j < 1)
                $fscanf(fileWeights, "[%b, ", test_weights[i][j]);
              else if (j < array_depth-1)
                $fscanf(fileWeights, "%b,", test_weights[i][j]);
              else
                $fscanf(fileWeights, "%b]", test_weights[i][j]);
            end
            // Read and Consume the newline character
            $fgetc(fileWeights);
          end
    
          $fclose(fileWeights);
    
        end else begin
          $display("Error opening the file for weight parsing");
        end
    endtask

    
    // Parse digits one after the other
    task parse_digits (
      input string file_name,
      input integer digit_number);

      fileLabel = $fopen(file_name, "r");
      if (fileLabel != 0) begin
        for (int i = 0; i < digit_number; i = i + 1) begin
          num_items = $fscanf(fileLabel, "%d", test_labels[i]);
          $display("Read label in iteration %d is %d", i, test_labels[i]);
          if (num_items == 0)
            break;
        end
      end else begin
        $display("Error opening the file for label reading");
      end
    endtask

    // Parse images separated by new line
    task automatic parse_images (
        input string file_name,
        input integer array_number,
        input integer array_depth);
    
        fileImg = $fopen(file_name, "r");
        if (fileImg != 0) begin
          // Read and parse the text fileImg
          for (int i = 0; i < array_number; i++) begin
            for (int j = 0; j < array_depth; j++) begin
              if (j < 1)
                $fscanf(fileImg, "[%d, ", test_images[i][j]);
              else if (j < array_depth-1)
                $fscanf(fileImg, "%d,", test_images[i][j]);
              else
                $fscanf(fileImg, "%d]", test_images[i][j]);
            end
            // Read and Consume the newline character
            $fgetc(fileImg);
          end
    
          $fclose(fileImg);
    
        end else begin
          $display("Error opening the file for image parsing");
        end
    endtask

    // Task to read spike trains from a file
    task read_spike_trains;
      // File handler
      integer file;
      // Loop variables
      integer i, j, k;

    
      // Open the file for reading
      file = $fopen("input_spikes_full_dataset.txt", "r");
      if (file != 0) begin
        // Read and parse the text file
        for (int k = 0; k < number_of_input_spike_trains; k++) begin
          for (int i = 0; i < total_number_pixels; i++) begin
            for (int j = 0; j < 50; j++) begin
              if (j < 1)
                $fscanf(file, "[%b, ", input_spike_trains_parsed[k][i][j]);
              else if (j < 50-1)
                $fscanf(file, "%b,", input_spike_trains_parsed[k][i][j]);
              else
                $fscanf(file, "%b]", input_spike_trains_parsed[k][i][j]);
                if (input_spike_trains_parsed[k][i][j] && k == 0) begin // Just evaluate the first one
                  $display("Read: input_spike_trains_parsed[%0d][%0d][%0d]", k, i, j);
                end
            end
          end
          // Read and Consume the newline character
          $fgetc(file);
        end
  
        $fclose(file);
  
      end else begin
        $display("Error opening the file for weight parsing");
      end
    endtask

    task automatic input_one_set_of_spikes_to_SNN;
      
      integer i;

      if (input_counter < 49) begin
        for (int i = 0; i < total_number_pixels; i++) begin
          input_spikes[i] = input_spike_trains_parsed[spike_train_pointer][i][input_counter]; // Go through each of the 784 lists and then store the value at the correct time stamp at the specified list index in the input spike train register
        end
      end else begin 
        for (int i = 0; i < total_number_pixels; i++) begin
          input_spikes[i] = 0;
        end
      end

    endtask


    // SIMPLE TIME-HANDLING TASK
	  task wait_ns;
        input   tics_ns;
        integer tics_ns;
        #tics_ns;
    endtask

  
    initial begin

        
        reset_in = 1;
        reset_count = 1;

        #3;
        reset_in = 0;
        reset_count = 0;
    

        
        number_of_weights_per_array = 784;
        number_of_weight_arrays = 100;

        read_spike_trains();
        // Get weights and convert from ASCII char to int
        file_name = "weights_fixed_point_LFSR_to_excitatory_16_10_fp_experiments.txt";
        parse_weights(.file_name (file_name), .array_number(number_of_weight_arrays), .array_depth(number_of_weights_per_array));
        
        /*****************************************************************************************************************************************************************************************************************/
        /* Inference */
        /*****************************************************************************************************************************************************************************************************************/            
        images_to_test = number_of_input_spike_trains;
        
        // Get test_lables and convert from ASCII char to int
        file_name = "MNIST_labels.txt";
        parse_digits(.file_name (file_name), .digit_number(images_to_test));
        
        // Get Images 
        file_name = "MNIST_images.txt";
        parse_images(.file_name(file_name), .array_number(images_to_test), .array_depth(784));
        
        // Get neuron assignments
        file_name = "neuron_assignments.txt";
        read_neuron_assignments(file_name, number_of_excitatory_neurons);

        file_name_thresholds = "thresholds_fixed_16_10_fp_experiments.txt";
        parse_thresholds(.file_name (file_name_thresholds), .number_of_thresholds(number_of_excitatory_neurons));

       
        for (img = 0; img < images_to_test; img = img + 1) begin
        
          // Marshall the new image to send
          test_image = test_images[img];
        
  
          start_inputting = 1;
          #1;
          start_counting = 1;
          en_in = 1;

          #498;
          start_inputting = 0;
          start_counting = 0;
          input_counter = 0;

          find_max_spike_index(max_spike_index, max_spike_count);

          sum_spikes_over_labels_and_classify(img, classified_label, total_number_of_spikes);

          reset_in = 1;
          reset_count = 1;

          en_in = 0;
          spike_train_pointer = spike_train_pointer + 1; //Change which image to read

          #3;
          reset_in = 0;
          reset_count = 0;
        
        end 
   
    $display("Number of correct classifications: %d", number_of_correct_classifications);
    $display("Accuracy if we say it can get the label as top three - just for debugging purposes: %d", pseudo_number_of_correct_classifications); 
    

        
    $finish;
    end
endmodule
