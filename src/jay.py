import numpy as np
import pandas as pd
import datetime, yaml, sys

class Data:
    def __init__(self, n_samples: int, n_vars: int, null_seed: int, n_negative: int = 3, date_index = False):
        if n_vars < n_negative:
            raise ValueError('Number of negative rows cannot be larger that number of variables')
        self.n_samples = n_samples
        self.n_vars = n_vars
        self.null_seed = null_seed
        self.n_negative = n_negative
        self.date_index = date_index
        self.func = None
        self._generate()
    def __repr__(self):
        text = f'MockData: non-null: {self.data.dropna().shape}\traw: {self.data.shape}\tFunc: {self.func}' 
        return text
    def __add__(self, other):
        if self.data.shape == other.data.shape:
            return self.data + other.data
        else:
            return self.data and self.n_samples > other.n_samples or other.data
    def __sub__(self, other):
        if self.data.shape == other.data.shape:
            return self.data - other.data
        else:
            return self.data and self.n_samples > other.n_samples or other.data
    def __mul__(self, other):
        if self.data.shape[1] == other.data.shape[1]:
            return pd.concat([self.data, other.data])
        else:
            return self.data and self.n_samples > other.n_samples or other.data
    def _generate(self):
        df_dict = {}
        for i in range(self.n_vars):
            if i < self.n_negative:
                val = np.linspace(-1, +1, self.n_samples)
            else:
                val = (np.linspace(-1, +1, self.n_samples) - np.random.rand())*np.random.randint(1, 50)
            df_dict[f'x{i}'] = val
        df = pd.DataFrame(df_dict)
        mask = np.random.randint(0, self.null_seed, df.shape) > 0
        mask = pd.DataFrame(mask).rename(
            columns = dict(zip(range(len(df_dict.keys())), list(df_dict.keys())))
        )
        self.data = df[mask]
        self._add_index()
        return 0
    def _add_index(self):
        cols = list(self.data.columns)
        if self.date_index:
            self.data['index_column'] = [(datetime.datetime.now() + datetime.timedelta(i)).strftime('%Y-%m-%d') for i in range(self.n_samples)]
        else:
            self.data = self.data.reset_index().rename(columns = {'index': 'index_column'})
        self.data = self.data[['index_column', *cols]]
    def apply_func(self, func: str):
        self.func = func
        try:
            for var in [f'x{j}' for j in range(self.n_vars)]:
                func = func.replace(var, f'self.data["{var}"]')
        except Exception as e:
            raise(e)
        self.data['y'] = eval(func)
        return func

if __name__ == '__main__':
    try:
        conf_path = sys.argv[1]
    except Exception as e:
        print(e)
    with open(conf_path, 'r') as cnf:
        configs = yaml.safe_load(cnf)
    print("[*] INITIALIZE")
    m = Data(**configs['args'])
    print(f"[*] {m}")
    m.apply_func(configs['function'])
    print(f'[*] Function applied: {m}')
    m.data.to_csv(f'D:/repo/mockingjay/data/{configs["name"]}.csv')
    print(f"[*] Data stored: `D:/repo/mockingjay/data/{configs["name"]}.csv`")