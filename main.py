from fastapi import FastAPI, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel, Field, Session, create_engine, select, Column, col
from typing import Optional, Any, Annotated
from CreatingTable import final_dict
import os
from dotenv import load_dotenv
load_dotenv()
db_url = os.getenv("DATABASE_URL")
app = FastAPI()
origins=['http://localhost:8501']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['GET'],
    allow_headers=["*"],
)
engine = create_engine(db_url,echo=True)
SQLModel.metadata.create_all(engine)
class Jioplansprices(SQLModel, table=True):
    __tablename__="jioplansprices"
    id :int = Field(default=None, primary_key=True)
    price: int
    category: str

class jioplansbenefits(SQLModel, table=True):
    __tablename__="jioplansbenefits"

    dfid : int =Field(default=None,primary_key=True)
    id: int = Field(default=None, foreign_key="jioplansprices.id")
    benefitname:str
    benefitvalue: str

def get_session():
    with Session(engine) as session:
        yield session

# def flatten(lst):
#     resultids = []
#     for item in lst:
#         if isinstance(item, list):
#             resultids.extend(flatten(item))
#         else:
#             resultids.append(item)
#     return resultids

@app.get("/jioplansprices/",summary="Find prices",description="Get a list of Jio data plans prices")
def get_jio_plans_prices(session: Session = Depends(get_session)):
    return session.exec(select(Jioplansprices)).all()

@app.get("/jioplansbenefits/", summary="Find Plans", description="Get a list of available Jio data plans details")
def get_jio_plans(session: Session = Depends(get_session)):
    return session.exec(select(jioplansbenefits)).all()

@app.get("/allJioplans/")
def get_plans_with_benefits(session: Session = Depends(get_session)):
    plans = session.exec(select(Jioplansprices)).all()
    benefits = session.exec(select(jioplansbenefits)).all()

    grouped = {}
    for benefit in benefits:
        grouped.setdefault(benefit.id, []).append({
            # "benefitname": benefit.benefitname,
            # "benefitvalue": benefit.benefitvalue
            benefit.benefitname:benefit.benefitvalue
        })

    resultids = []
    for plan in plans:
        resultids.append({
            "id": plan.id,
            "price": plan.price,
            "category": plan.category,
            "benefits": grouped.get(plan.id, [])
        })
    return resultids

@app.get("/filter-plans-by-subscriptions")
def get_plans_with_subscriptions(q: Annotated[list[str] , Query()]=[], session: Session =Depends(get_session)):#to work on 5 april
    resultfinal={}
    for query in q:
        selectids=select(jioplansbenefits.id).where(col(jioplansbenefits.benefitvalue).ilike(f'%{query}%'))
        resultids=session.exec(selectids).all()
        subpack=[]
        for i in resultids:
            subpack.append(final_dict[i])
        resultfinal[query]=subpack
    return resultfinal
def main():
    print("Hello from bestrechargeplanfinder!")


if __name__ == "__main__":
    main()