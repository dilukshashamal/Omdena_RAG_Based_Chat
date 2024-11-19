import pandas as pd

def preprocess_by_class(data: pd.DataFrame, class_type: str) -> pd.DataFrame:
    # Filter rows by the given class type
    filtered_data = data[data['class'] == class_type]
    
    # Clean and normalize text content
    filtered_data['text_content'] = filtered_data['text_content'].str.strip()  # Remove leading/trailing spaces
    filtered_data['text_content'] = filtered_data['text_content'].str.replace('\n', ' ')  # Replace newlines with spaces
    
    # Add a source column for identification
    filtered_data['source'] = class_type.upper()
    
    return filtered_data


def preprocess_data(input_file: str, output_file: str):

    # Load the raw data
    raw_data = pd.read_csv(input_file)
    
    # Preprocess for each class type
    act_data = preprocess_by_class(raw_data, 'act')
    circulars_data = preprocess_by_class(raw_data, 'circular')
    guidelines_data = preprocess_by_class(raw_data, 'guideline')
    regulations_data = preprocess_by_class(raw_data, 'regulation')
    
    # Combine all preprocessed data
    combined_data = pd.concat([act_data, circulars_data, guidelines_data, regulations_data], ignore_index=True)
    
    # Add unique ID for retrieval
    combined_data['id'] = combined_data.index + 1
    
    # Save to CSV
    combined_data[['id', 'class', 'text_content', 'source']].to_csv(output_file, index=False)
    print(f"Preprocessed data saved to {output_file}")
    return combined_data
