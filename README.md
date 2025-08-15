# MockingJay

Generate synthetic mock data, control randomness and sparsity, and apply custom functions to derive outputs.  
Designed for quick prototyping, testing, or generating datasets, programmatically.

---

## 🚀 Features

- Generate `n_samples × n_vars` numeric dataset with controlled random nulls.
- Optional date-based or sequential index column.
- Dynamically apply any mathematical function (as a string) to variables to compute output `y`.
- Basic operator overloading for combining or comparing `Data` instances.
- Can be uniform or non-uniform

---

## Installation

Clone this repository:

```bash
git clone https://github.com/314arhaam/mockingjay.git
cd mockingjay
```

## Config

Sample pipeline config that creates two datasets.

```yaml
- name: "data_mock_multi_build"
  args:
    n_samples: 1000
    n_vars: 5
    null_seed: 50
    date_index: True
    uniform: True
  function: 
    - "2*x1+4*x3-x2+x4*np.sin(x2*x1)"
    - "x1 + x0"
  data:
    type: file
    format: csv
    path: "data"
- name: "data_mock_multi_predict"
  args:
    n_samples: 200
    n_vars: 5
    null_seed: 15
    date_index: True
    uniform: True
  function: 
    - "2*x1+4*x3-x2+x4*np.sin(x2*x1)"
    - "x1 + x0"
  data:
    type: file
    format: csv
    path: "data"
```
