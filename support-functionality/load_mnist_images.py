


def read_all_images(file_path):
    image_array = []
    label_array = []
    try:
        with open(file_path, 'r') as file:
            for line in file:

                split_line = line.split(",")
                pixel_array = []
                
                for el in split_line[1:]:
                    pixel_array.append(int(el))
                image_array.append(pixel_array)
                label_array.append(split_line[0])


    except FileNotFoundError:
        print(f"The file {file_path} was not found.")
    except ValueError:
        print("The file contains non-numeric data.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return image_array,label_array

file_path = 'MNIST_test.txt'
image_array, label_array = read_all_images(file_path)



def write_all_images(file_path_images, file_path_labels, image_array, label_array):
    try:

        with open(file_path_labels, 'w') as file_2:
            for item in label_array:
                line = str(item)+'\n'
                file_2.write(line)
            
    except FileNotFoundError:
        print(f"The file {file_path_labels} was not found.")
    
    except Exception as e:
        print(f"An error occurred: {e}")
    return 

write_all_images(file_path_images="MNIST_images.txt", file_path_labels="MNIST_labels.txt", image_array=image_array, label_array=label_array)