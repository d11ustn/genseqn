import os
from ruamel.yaml import YAML

def sample_list(config_path, main_dir, file_extensions):
    yaml = YAML()

    with open(config_path, 'r') as file:
        config = yaml.load(file)

    # Define base_path; project_name; illumina_data;
    base_path = config.get('sample_path', '')
    project_name = config.get('project_name', '')
    illumina_data = config.get('illumina_data', False)

    if not base_path or not project_name:
        raise ValueError("sample_path or project_name not defined in config.yaml.")

    # Set output folder for {project_name}_db.txt
    output_dir = os.path.join(main_dir, "results")
    # Create {project_name}_db.txt
    output_path = os.path.join(output_dir, f"{project_name}/{project_name}_db.txt")

    # Save information for each sample
    sample_infos = []
    # List to display the successfully loaded samples
    loaded_samples = []
    # Track if any error occurred
    error_occurred = False

    for sample_dir in os.listdir(base_path):
        current_sample_path = os.path.join(base_path, sample_dir)
        if os.path.isdir(current_sample_path):
            sample_info = f"{sample_dir}; "
            data_types = {'ONT': ['ONT', 'ont']}
            if illumina_data:
                data_types['Illumina'] = ['Illumina', 'illumina']

            for data_type, folders in data_types.items():
                folder_found = False
                for folder_name in folders:
                    folder_path = os.path.join(current_sample_path, folder_name)
                    if os.path.exists(folder_path) and os.listdir(folder_path):
                        files = [f for f in os.listdir(folder_path) if any(f.endswith(ext) for ext in file_extensions)]
                        if files:
                            
                            # Check for Illumina data
                            if data_type == 'Illumina' and illumina_data:
                                paired_files = [f for f in files if "_1" in f or "_2" in f]
                                if len(paired_files) != 2 or not (any("_1" in f for f in paired_files) and any("_2" in f for f in paired_files)):
                                    print(f"Incorrect number of paired Illumina files or naming convention not followed in sample: {sample_dir}")
                                    error_occurred = True
                                    break
                            sample_info += f"{data_type}: " + ", ".join(files) + "; "
                            folder_found = True
                            break
                        
                if not folder_found and data_type in data_types:
                    print(f"No {data_type} data found in sample: {sample_dir}")
                    error_occurred = True
                    break

            if not error_occurred:
                sample_infos.append(sample_info)
                loaded_samples.append(sample_dir)
            else:
                break  # Exit the loop if an error occurred

    # Only create and write to the file if no error occurred
    if not error_occurred and sample_infos:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w') as outfile:
            for info in sample_infos:
                outfile.write(info + "\n")
        
        if loaded_samples:  # Check if there are any loaded samples
            print("\nLoaded samples:")
            for sample in loaded_samples:
                print(sample)  # Print each loaded sample folder on a new line
        
        print("\nSamples were loaded successfully!")
        print(f"You set illumina_data to: {illumina_data}\n")


if __name__ == "__main__":
    main_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    config_path = os.path.join(main_dir, "config/config.yaml")
    file_extensions = [".fastq.gz", ".fastq"]

    sample_list(config_path, main_dir, file_extensions)