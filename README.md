# MockingJay

Generate synthetic mock data, control randomness and sparsity, and apply custom functions to derive outputs.  
Designed for quick prototyping, testing, or generating datasets programmatically.

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