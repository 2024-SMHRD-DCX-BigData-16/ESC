import pandas as pd
import pymysql
from sqlalchemy import create_engine

# CSV 로드
df = pd.read_csv("C:/Users/smhrd/Desktop/공공데이터/csv/test.csv", encoding='utf-8')
df = df[['징수요청연도', '위반법령', '위반법조항', '건수']]
df.columns = ['year', 'law_name', 'law_article', 'count']
df = df.dropna()

# MySQL 연결
engine = create_engine("mysql+pymysql://user:password@localhost:3306/your_db")
df.to_sql("penalty_stats", con=engine, if_exists='replace', index=False)
