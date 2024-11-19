from preprocess import preprocess_data

def main():
    input_file = 'new_LK_tea_dataset_updated.csv'  # Raw input file
    output_file = 'preprocessed_data.csv'  # Cleaned output file
    
    preprocess_data(input_file, output_file)

if __name__ == "__main__":
    main()
