import pandas as pd

class Data:
    def __init__(self) -> None:
        self.data = pd.read_csv('./src/data/수질지수.csv')
        self.date_col = '조사일자'
        self.preprocessing()

    def preprocessing(self) -> None:
        self.data[self.date_col] = pd.to_datetime(self.data[self.date_col])