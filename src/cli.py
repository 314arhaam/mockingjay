import inquirer
import yaml
from jay import Data

def main():
    print("Welcome to the Data Generator CLI!")

    # Define the questions for the interactive menu
    questions = [
        inquirer.Text('n_samples', message="Enter the number of samples (rows)", validate=lambda _, x: x.isdigit()),
        inquirer.Text('n_vars', message="Enter the number of variables (columns)", validate=lambda _, x: x.isdigit()),
        inquirer.Text('null_seed', message="Enter the null seed (higher values yield more nulls)", validate=lambda _, x: x.isdigit()),
        inquirer.List('date_index', message="Use a datetime index?", choices=['yes', 'no']),
        inquirer.List('uniform', message="Generate uniform data?", choices=['yes', 'no']),
        inquirer.Text('filename', message="Enter the base filename (without extension)"),
    ]

    # Prompt the user for inputs
    answers = inquirer.prompt(questions)

    # Parse the inputs
    n_samples = int(answers['n_samples'])
    n_vars = int(answers['n_vars'])
    null_seed = int(answers['null_seed'])
    date_index = answers['date_index'] == 'yes'
    uniform = answers['uniform'] == 'yes'
    filename = answers['filename']

    # Create the Data object
    try:
        data_obj = Data(
            n_samples=n_samples,
            n_vars=n_vars,
            null_seed=null_seed,
            date_index=date_index,
            uniform=uniform
        )

        # Save the generated data to a CSV file
        data_obj.data.to_csv(f"{filename}.csv", index=False)
        print(f"\nDataset saved to {filename}.csv")

        # Save the configuration to a YAML file
        config = {
            'n_samples': n_samples,
            'n_vars': n_vars,
            'null_seed': null_seed,
            'date_index': date_index,
            'uniform': uniform,
        }
        with open(f"{filename}_config.yaml", 'w') as yaml_file:
            yaml.dump(config, yaml_file, default_flow_style=False)
        print(f"Configuration saved to {filename}_config.yaml")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()