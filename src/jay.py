import numpy as np
import pandas as pd
import datetime, yaml, sys
from typing import Union

class Data:
    """
    A class for generating synthetic mock datasets with optional nulls and a derived column.

    Attributes:
        n_samples (int): Number of samples (rows).
        n_vars (int): Number of variables (columns).
        null_seed (int): Controls sparsity; higher values yield more nulls.
        date_index (bool): Whether to use a datetime index.
        data (pd.DataFrame): Generated dataset.
        func (str): Last applied function string.
    """

    def __init__(
        self, 
        n_samples: int, 
        n_vars: int, 
        null_seed: int, 
        date_index: bool = False,
        uniform: bool = False,
    ) -> None:
        """
        Initializes the Data class and generates mock data.

        Args:
            n_samples (int): Number of rows.
            n_vars (int): Number of features.
            null_seed (int): Parameter controlling frequency of nulls.
            date_index (bool): Whether to use dates in the index column.
            uniform (bool)
        """
        self.n_samples: int = n_samples
        self.n_vars: int = n_vars
        self.null_seed: int = null_seed
        self.date_index: bool = date_index
        self.func: Union[str, None] = None
        self.data: pd.DataFrame
        self.uniform: bool = uniform
        self._generate()

    def __repr__(self) -> str:
        """
        Returns a string representation of the object showing data shapes and last applied function.
        """
        text = f'MockData: non-null: {self.data.dropna().shape}\traw: {self.data.shape}\tFunc: {self.func}' 
        return text

    def __add__(self, other: 'Data') -> pd.DataFrame:
        """
        Adds two Data instances element-wise if shapes match, otherwise returns the larger dataset.

        Args:
            other (Data): Another Data object.

        Returns:
            pd.DataFrame: Result of addition or fallback data.
        """
        if self.data.shape == other.data.shape:
            return self.data + other.data
        else:
            return self.data if self.n_samples > other.n_samples else other.data

    def __sub__(self, other: 'Data') -> pd.DataFrame:
        """
        Subtracts two Data instances element-wise if shapes match, otherwise returns the larger dataset.

        Args:
            other (Data): Another Data object.

        Returns:
            pd.DataFrame: Result of subtraction or fallback data.
        """
        if self.data.shape == other.data.shape:
            return self.data - other.data
        else:
            return self.data if self.n_samples > other.n_samples else other.data

    def __mul__(self, other: 'Data') -> pd.DataFrame:
        """
        Concatenates data from two instances if column counts match, otherwise returns the larger dataset.

        Args:
            other (Data): Another Data object.

        Returns:
            pd.DataFrame: Concatenated or fallback data.
        """
        if self.data.shape[1] == other.data.shape[1]:
            return pd.concat([self.data, other.data])
        else:
            return self.data if self.n_samples > other.n_samples else other.data

    def _generate(self) -> int:
        """
        Internal method to generate mock data with structured values and controlled nulls.

        Returns:
            int: Always returns 0 after successful generation.
        """
        df_dict: dict[str, np.ndarray] = {}
        span = np.linspace(0, 1, self.n_samples)
        for i in range(self.n_vars):
            a, b = np.random.randint(-100, +100), np.random.randint(-100, +100)
            start, end = min(a, b), max(a, b)
            if self.uniform:
                power_val = 1
            else:
                power_val = np.linspace(0.1, 1, 10)[np.random.randint(0, 10)]
                if  np.random.randint(0, 1):
                    power_val = 1/power_val
            val = start + (end - start) * span**power_val
            df_dict[f'x{i}'] = val

        df = pd.DataFrame(df_dict)

        mask = np.random.randint(0, self.null_seed, df.shape) > 0
        mask_df = pd.DataFrame(mask).rename(
            columns=dict(zip(range(len(df_dict)), list(df_dict.keys())))
        )

        self.data = df[mask_df]
        self._add_index()
        return 0

    def _add_index(self) -> None:
        """
        Adds an index column to the DataFrame: either datetime-based or numeric.
        """
        cols = list(self.data.columns)
        if self.date_index:
            self.data['index_column'] = [
                (datetime.datetime.now() + datetime.timedelta(i)).strftime('%Y-%m-%d')
                for i in range(self.n_samples)
            ]
        else:
            self.data = self.data.reset_index().rename(columns={'index': 'index_column'})
        self.data = self.data[['index_column', *cols]]

    def apply_func(self, func: str) -> str:
        """
        Evaluates a mathematical expression string on the dataset and stores the result in column 'y'.

        Args:
            func (str): A string expression involving variables like 'x0', 'x1', etc.

        Returns:
            str: The modified function string after variable substitution.
        """
        if (func != None) and (self.n_vars > 10):
            raise NotImplementedError('Currently, function args are simply replaced in formula and when n_vars > 10, this leads to error')
        self.func = func
        try:
            for var in [f'x{j}' for j in range(self.n_vars)]:
                func = func.replace(var, f'self.data["{var}"]')
        except Exception as e:
            raise e
        self.data['y'] = eval(func)
        return func

if __name__ == '__main__':
    # Parse command line argument for YAML config path
    try:
        conf_path: str = sys.argv[1]
    except Exception as e:
        print(e)
        sys.exit(1)

    # Load configuration from YAML
    with open(conf_path, 'r') as cnf:
        configs_list: dict = yaml.safe_load(cnf)
    
    for configs in configs_list:
        print(f"[*] Initialized {configs['name']}")

        # Initialize data object with given arguments
        m: Data = Data(**configs['args'])
        print(f"[*] {m}")
        try:
            # Apply transformation function
            m.apply_func(configs['function'])
            print(f'[*] Function applied: {m}')
        except NotImplementedError:
            print('Error occured {e}\n Saving dataset without applying function')
        # Save result to CSV
        output_filename: str = f'{configs["path"]}/{configs["name"]}.csv'
        m.data.to_csv(output_filename, index = False)
        print(f"[*] Data stored: `{output_filename}`")
        print(m.data.info())
        print(m.data.describe())
