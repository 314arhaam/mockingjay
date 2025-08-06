# MockingJay

Generate synthetic mock data, control randomness and sparsity, and apply custom functions to derive outputs.  
Designed for quick prototyping, testing, or generating datasets programmatically.

---

## 🚀 Features

- Generate `n_samples × n_vars` numeric dataset with controlled random nulls.
- First `n_negative` variables are uniformly spaced between –1 and +1.
- Optional date-based or sequential index column.
- Dynamically apply any mathematical function (as a string) to variables to compute output `y`.
- Basic operator overloading for combining or comparing `Data` instances.

---

## Installation

Clone this repository:

```bash
git clone https://github.com/314arhaam/mockingjay.git
cd mockingjay