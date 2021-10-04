import numpy as np
import pandas as pd


def read_csv(filename):
    names ='no title url'.split()
    df = pd.read_csv(filename, names=names, na_filter=False)
    return df
