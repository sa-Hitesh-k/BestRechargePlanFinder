import pandas as pd
from sqlmodel import create_engine, SQLModel, Field, Session, select, Column, String
from typing import Optional, Any, List
from sqlalchemy import text
from sqlalchemy.dialects.postgresql import ARRAY
import json
from CreatingTable import df2, df_prices, dfott
import os
from dotenv import load_dotenv
load_dotenv()
db_url = os.getenv("DATABASE_URL")
# 1. Define your SQLModel table structure
class Jioplansprices(SQLModel, table=True):
    __tablename__="jioplansprices"
    id :int = Field(default=None, primary_key=True)
    price: int
    category: str

class Jioplansbenefits(SQLModel, table=True):
    __tablename__="jioplansbenefits"
    dfid : int =Field(default=None,primary_key=True)
    id: int= Field(default=None, foreign_key="jioplansprices.id")
    benefitname:str
    benefitvalue: str
    
class Jioplanssubscriptions(SQLModel, table=True):
    __tablename__="jiosubs"
    sub_id : int | None = Field(default=None, primary_key=True)
    subval :str


# 2. Create the engine
engine = create_engine(db_url)
with engine.begin() as conn:
    conn.execute(text("DROP TABLE IF EXISTS jioplansprices CASCADE;"))
    conn.execute(text("DROP TABLE IF EXISTS jioplansbenefits CASCADE;"))
    conn.execute(text("DROP TABLE IF EXISTS jiosubs CASCADE;"))

# Create the table in the database (if it doesn't exist)
SQLModel.metadata.create_all(engine)

# df2['benefitvalue'] = df2['benefitvalue'].apply(json.dumps)
# 3. Create a sample pandas DataFrame
try:
    df_prices.to_sql('jioplansprices', con=engine, if_exists='append', index=False)
    print("DataFrame jio_plans_prices successfully uploaded to the database.")
except ValueError as e:
    print(f"Error uploading DataFrame: {e}")
try:
    df2.to_sql('jioplansbenefits', con=engine, if_exists='append', index=False)
    print("DataFrame jio_data_plans(details) successfully uploaded to the database.")
except ValueError as e:
    print(f"Error uploading DataFrame: {e}")
try:
    dfott.to_sql('jiosubs', con=engine, if_exists='append', index=False)
    print("DataFrame jio_plans_subscriptions(details) successfully uploaded to the database.")
except ValueError as e:
    print(f"Error uploading DataFrame: {e}")
