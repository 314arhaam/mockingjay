import inquirer
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
    ]

    # Prompt the user for inputs
    answers = inquirer.prompt(questions)

    # Parse the inputs
    n_samples = int(answers['n_samples'])
    n_vars = int(answers['n_vars'])
    null_seed = int(answers['null_seed'])
    date_index = answers['date_index'] == 'yes'
    uniform = answers['uniform'] == 'yes'

    # Create the Data object
    try:
        data_obj = Data(
            n_samples=n_samples,
            n_vars=n_vars,
            null_seed=null_seed,
            date_index=date_index,
            uniform=uniform
        )

        # Display the generated data
        print("\nDataset generated successfully!")
        print(data_obj.data)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()