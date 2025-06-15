import pandas as pd

def replace_komma_and_cast_to_float(x):
    if isinstance(x, str):
        try:
            x = float(x.replace(",", "."))
        except: 
            pass
    return x

def read_data(file_name):
    df = pd.read_csv(file_name, sep=";")
    return df


def cast_data(df):
    return df.map(replace_komma_and_cast_to_float)


