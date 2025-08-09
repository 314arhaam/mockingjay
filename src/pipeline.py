import numpy as np
import pandas as pd
import datetime, yaml, sys
from typing import Union
from jay import *

class Pipeline:
    def __init__(self, configs_list: list):
        self.configs_list = configs_list
        self.data = []
    
    def __call__(self):
        for configs in self.configs_list:
            print(f"[*] Initialized {configs['name']}")

            # Initialize data object with given arguments
            m: Data = Data(**configs['args'])
            self.data.append(m)
            print(f"[*] {m}")
            try:
                # Apply transformation function
                for fun_index, fun in enumerate(configs['function']):
                    output_name = f'y{fun_index}'
                    m.apply_func(fun, output_name)
                    print(f'[*] Function applied: {m}')
            except NotImplementedError:
                print('Error occured {e}\n Saving dataset without applying function')
            # Save result to CSV
            if configs['data']['type'] == 'file':
                if configs['data']['format'] == 'csv':
                    output_filename: str = f'{configs["data"]["path"]}/{configs["name"]}.csv'
                    m.data.to_csv(output_filename, index = False)
                elif configs['data']['format'] == 'parquet':
                    output_filename: str = f'{configs["data"]["path"]}/{configs["name"]}.csv'
                    m.data.to_parquet(output_filename, index = False)
                print(f"[*] Data stored: `{output_filename}`")
            print(m.data.info())
            print(m.data.describe())