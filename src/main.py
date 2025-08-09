import numpy as np
import pandas as pd
import datetime, yaml, sys
from typing import Union
from jay import *
from pipeline import *

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
    
    p = Pipeline(configs_list)
    p()