import pandas as pd

def getSpeciesList():
    df = pd.read_csv('assets/arbres-publics.csv')
    return list(pd.unique(df['Essence_fr']))