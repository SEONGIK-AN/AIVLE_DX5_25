import pandas as pd
import joblib

class Predict:
    def __init__(self) -> None:
        self.models = joblib.load('./src/model_data/models.pkl')
        self.data = pd.read_csv('./src/data/표층수온_표층염도_예측치.csv')
        self.date_col = '기간'
        self.preprocessing()

    def preprocessing(self) -> None:
        self.data['기간'] = pd.to_datetime(self.data['기간'])
        self.data['월'] = self.data['기간'].dt.month
        
    def predict(self, fish_kind: str, date: str) -> pd.DataFrame:
        X = self.data[self.data['기간']==date].drop(columns='기간')
        X['개체수'] = self.models[fish_kind].predict(X)
        return X
    
    def feature_importances(self, fish_kind: str) -> pd.Series:
        return pd.Series(dict(zip(self.data.drop(columns='기간').columns, self.models[fish_kind].feature_importances_)))
    
    def get_trend(self, fish_kind: str) -> pd.Series:
        data = dict()
        for date in self.data['기간'].unique():
            data[date] = self.models[fish_kind].predict(self.data[self.data['기간']==date].drop(columns='기간')).mean()
        return pd.Series(data)
    
    def get_optimal_value(self, predicted_df: pd.DataFrame, digit: int) -> pd.DataFrame:
        def get_range(col: str) -> str:
            upper = '+' + (predicted_df[col+'u']-predicted_df[col]).round(digit).astype(str).values[0]
            lower = '-' + (predicted_df[col]-predicted_df[col+'l']).round(digit).astype(str).values[0]
            return upper + ' / ' + lower

        predicted_df = predicted_df[predicted_df['개체수']==predicted_df['개체수'].max()]\
            .drop(columns='월').reset_index(drop=True)
        predicted_df = predicted_df.groupby(by='개체수', as_index=False).agg(
            위도=('위도', 'mean'),
            위도u=('위도', 'max'),
            위도l=('위도', 'min'),

            경도=('경도', 'mean'),
            경도u=('경도', 'max'),
            경도l=('경도', 'min'),
            
            표층수온=('표층수온', 'mean'),
            표층수온u=('표층수온', 'max'),
            표층수온l=('표층수온', 'min'),
            
            표층염분=('표층염분', 'mean'),
            표층염분u=('표층염분', 'max'),
            표층염분l=('표층염분', 'min'),
        ).apply(lambda x: x.round(digit))

        
        predicted_df['위도 (+/-)'] = get_range('위도')
        predicted_df['경도 (+/-)'] = get_range('경도')
        predicted_df['표층수온 (+/-)'] = get_range('표층수온')
        predicted_df['표층염분 (+/-)'] = get_range('표층염분')
        return predicted_df[['위도', '위도 (+/-)', '경도', '경도 (+/-)', '표층수온', '표층수온 (+/-)', '표층염분', '표층염분 (+/-)']].T