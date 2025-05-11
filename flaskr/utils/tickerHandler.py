import pandas as pd
from pathlib import Path
import os

filepath = os.path.join(Path(__file__).parent.parent, 'files', 'listedCompanies_en_US.xls')

def read_file(file_path: str) -> pd.DataFrame:
    return  pd.read_html(file_path) 

def ticker(df: pd.DataFrame) -> set:
    df = df[0]
    symbol = set(df.iloc[2:,0])
    symbol = {dt+'.bk' for dt in symbol}
    return symbol

def get_ticker():
    df = read_file(filepath)
    ticker_info = ticker(df)
    return ticker_info
    
if __name__ == "__main__":
    get_ticker()