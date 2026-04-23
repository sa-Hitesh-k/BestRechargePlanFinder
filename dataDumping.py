import pandas as pd
from sqlmodel import create_engine, SQLModel, Field, Session, select, Column, String, Relationship
from typing import Optional, Any, List
from sqlalchemy import text
from sqlalchemy.dialects.postgresql import ARRAY
import json
import os
from dotenv import load_dotenv
from CreatingTable import process_all_jio_data, get_ott_list
df_prices, df_benefits, dfott = process_all_jio_data()
uniqueott_df=get_ott_list()

load_dotenv()
db_url = os.getenv("DATABASE_URL")
# 1. Defining SQLModel table structure
class Jioplansprices(SQLModel, table=True):
    __tablename__="jioplansprices"
    id :int = Field(default=None, primary_key=True)
    uid: int
    price: int
    category: str
    plan : list["Jioplansbenefits"] =Relationship(back_populates="group")

class Jioplansbenefits(SQLModel, table=True):
    __tablename__="jioplansbenefits"
    dfid : int =Field(default=None,primary_key=True)
    id: int= Field(default=None, foreign_key="jioplansprices.id")
    uid : int 
    benefitname:str
    benefitvalue: str
    group: Jioplansprices | None = Relationship(back_populates="plan")

class Jioplanssubscriptions(SQLModel, table=True):
    __tablename__="jiosubs"
    sub_id : int | None = Field(default=None, primary_key=True)
    subval :str

class Uniqueotts(SQLModel, table=True):
    __tablename__="uniqueotts"
    ottid: int =Field(default=None, primary_key=True)
    otts: str 


# 2. Creating the engine
engine = create_engine(db_url)
with engine.begin() as conn:
    conn.execute(text("DROP TABLE IF EXISTS jioplansprices CASCADE;"))
    conn.execute(text("DROP TABLE IF EXISTS jioplansbenefits CASCADE;"))
    conn.execute(text("DROP TABLE IF EXISTS jiosubs CASCADE;"))
    conn.execute(text("DROP TABLE IF EXISTS uniqueotts CASCADE;"))

# Creating the table in the database (if it doesn't exist)
SQLModel.metadata.create_all(engine)

# df_benefits['benefitvalue'] = df_benefits['benefitvalue'].apply(json.dumps)
# 3. Creating a sample pandas DataFrame
try:
    df_prices.to_sql('jioplansprices', con=engine, if_exists='append', index=False)
    print("DataFrame jio_plans_prices successfully uploaded to the database.")
except ValueError as e:
    print(f"Error uploading DataFrame: {e}")
try:
    df_benefits.to_sql('jioplansbenefits', con=engine, if_exists='append', index=False)
    print("DataFrame jio_data_plans(details) successfully uploaded to the database.")
except ValueError as e:
    print(f"Error uploading DataFrame: {e}")
try:
    dfott.to_sql('jiosubs', con=engine, if_exists='append', index=False)
    print("DataFrame jio_plans_subscriptions(details) successfully uploaded to the database.")
except ValueError as e:
    print(f"Error uploading DataFrame: {e}")
try:
    uniqueott_df.to_sql('uniqueotts', con=engine, if_exists='append', index=False)
    print("DataFrame uniqueott_df successfully uploaded to the database.")
except ValueError as e:
    print(f"Error uploading DataFrame: {e}")
