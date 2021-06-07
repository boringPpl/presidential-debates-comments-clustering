#!/usr/bin/env python

"""
This extracts the first 1000 lines of vecs1.tsv and vecs2.tsv
as well as the first 1000 lines of meta_lab.tsv
"""

import numpy as np
import pandas as pd

N_LINES = 1000

# Read Vectors
v1 = np.loadtxt("vecs1.tsv")
v2 = np.loadtxt("vecs2.tsv")

print(f"vecs1.tsv: {v1.shape}")
print(f"vecs2.tsv: {v2.shape}")

np.savetxt(f"vecs1_{N_LINES}.csv", v1[:N_LINES], delimiter=",")
np.savetxt(f"vecs2_{N_LINES}.csv", v2[:N_LINES], delimiter=",")

# Read Metadata
# df1 = pd.read_csv("meta_lab1.tsv", sep='\t')
# df2 = pd.read_csv("meta_lab2.tsv", sep='\t')

df1 = pd.read_excel("meta_lab1.xlsx", header=1)
df2 = pd.read_excel("meta_lab2.xlsx", header=1)

df1.head(1000).to_csv(f"meta_lab1_{N_LINES}.csv", index=False)
df2.head(1000).to_csv(f"meta_lab2_{N_LINES}.csv", index=False)
