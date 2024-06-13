

def analyze_assignments(input_file_path):
    neuron_assignment_count = [0,0,0,0,0,0,0,0,0,0]
    try:
        # Read the input file
        with open(input_file_path, 'r') as f:
            lines = f.readlines()

            for k in range(10):
                for i in range(len(lines)):
                    if (int(lines[i]) == k):
                        neuron_assignment_count[k] += 1
        print("Count: ", neuron_assignment_count)
        print("Index: ", "[0,  1, 2,  3, 4, 5,  6, 7,  8,  9]")

    except Exception as e:
        print(f"Error: {e}")

analyze_assignments("neuron_assignments.txt")