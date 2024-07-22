import pandas as pd

def convert_date(df: pd.DataFrame, convert_to: str, date_col: str, categorical_col: str, return_cols: list) -> pd.DataFrame:
    return_cols = [date_col, categorical_col] + return_cols
    df = df[return_cols]
    if convert_to.upper() == 'Y':
        df['temp'] = df[date_col].dt.strftime('%Y')
        df = df.groupby(by=['temp', categorical_col], as_index=False)[return_cols].median(numeric_only=True)
        df[date_col] = df['temp']
        return df.drop(columns='temp')
    elif convert_to.upper() == 'M':
        df['temp'] = df[date_col].dt.strftime('%Y-%m')
        df = df.groupby(by=['temp', categorical_col], as_index=False)[return_cols].median(numeric_only=True)
        df[date_col] = df['temp']
        return df.drop(columns='temp')
    elif convert_to.upper() == 'W':
        df['temp'] = df[date_col].dt.strftime('%Y-%m-%d')
        df = df.groupby(by=['temp', categorical_col], as_index=False)[return_cols].median(numeric_only=True)
        df[date_col] = df['temp']
        return df.drop(columns='temp')
    elif convert_to.upper() == 'D':
        return df
    else:
        raise ValueError