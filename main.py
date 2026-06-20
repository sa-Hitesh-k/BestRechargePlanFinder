from fastapi import FastAPI, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel, Field, Session, create_engine, select, col, Relationship
from typing import  Annotated
from sqlalchemy.orm import selectinload
import os
from dotenv import load_dotenv
import re

def extract_numeric_value(value_string: str) -> float:
    """Extract numeric value from strings like '28 Days', '56 GB', etc."""
    match = re.search(r'\d+\.?\d*', str(value_string))
    return float(match.group()) if match else 0.0

load_dotenv()
db_url = os.getenv("DATABASE_URL")

app = FastAPI()
origins=['http://localhost:8501','https://mobilerechargeplanfinder.onrender.com/','https://shk-recharge-plan-finder.streamlit.app/']
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
    uid: int
    price: int
    category: str
    plan : list["jioplansbenefits"] =Relationship(back_populates="group")

class jioplansbenefits(SQLModel, table=True):
    __tablename__="jioplansbenefits"

    dfid : int =Field(default=None,primary_key=True)
    id: int = Field(default=None, foreign_key="jioplansprices.id")
    uid : int
    benefitname:str
    benefitvalue: str
    group: Jioplansprices | None = Relationship(back_populates="plan")

class Uniqueotts(SQLModel, table=True):
    __tablename__="uniqueotts"
    ottid: int =Field(default=None, primary_key=True)
    otts: str 

def get_session():
    with Session(engine) as session:
        yield session

@app.get("/jioplansprices/",summary="Find prices",description="Get a list of Jio plans prices")
def get_jio_plans_prices(session: Session = Depends(get_session)):
    return session.exec(select(Jioplansprices)).all()

@app.get("/jioplansbenefits/", summary="Find Plans", description="Get a list of available Jio plans details")
def get_jio_plans(session: Session = Depends(get_session)):
    return session.exec(select(jioplansbenefits)).all()

@app.get("/allJioplans/")
def get_plans_with_benefits(session: Session = Depends(get_session)):
    plans = session.exec(select(Jioplansprices)).all()
    benefits = session.exec(select(jioplansbenefits)).all()

    grouped = {}
    for benefit in benefits:
        if benefit.benefitname not in ('id', 'uid', 'dfid','category'):
            grouped.setdefault(benefit.id, []).append({
                benefit.benefitname:benefit.benefitvalue
            }
            )

    resultids, i = [], 0
    for plan in plans:
        resultids.append({
            f"benefits pack {i}": grouped.get(plan.id, [])
        })
        i+=1
    return resultids
    # return grouped

@app.get("/unique-subscriptions", summary="Get Unique OTTs", description="Returns a sorted list of all unique OTT platforms found in Jio plans")
def get_unique_subscriptions(session: Session = Depends(get_session)):
    statement=select(Uniqueotts.otts)
    return session.exec(statement).all()

@app.get("/filter-plans-by-OTTs")
def get_plans_with_subscriptions(q: Annotated[list[str] , Query()]=[], session: Session =Depends(get_session)):
    res={}
    for query in q:
        select_plans=(select(Jioplansprices).join(jioplansbenefits).where(col(jioplansbenefits.benefitvalue).ilike(f'%{query}%')).options(selectinload(Jioplansprices.plan)).distinct(Jioplansprices.uid))
        plans=session.exec(select_plans).all()
        res[query] = [
            {
                "details": [
                {benefit.benefitname: benefit.benefitvalue}
                for benefit in plan.plan
                    if benefit.benefitname not in ('id', 'uid', 'dfid','category') # The Gatekeeper
            ]
            }
            for plan in plans
        ]

    return res

@app.get("/filter-plans-by-prices")
def get_plans_in_price_range(q1:int, q2:int, session: Session= Depends(get_session)):
    
    
    res={}
    select_plans=(select(Jioplansprices).join(jioplansbenefits).where(col(Jioplansprices.price).between(q1,q2)).options(selectinload(Jioplansprices.plan)).distinct(Jioplansprices.uid))
    plans=session.exec(select_plans).all()
    res["prices"]=[
        {
            "plan":[
                {benefit.benefitname: benefit.benefitvalue}
                for benefit in plan.plan
                    if benefit.benefitname not in ('id', 'uid', 'dfid','category')
            ]

        }
        for plan in plans
    ]
    return res

@app.get("/filter-plans-by-validity")
def get_plans_by_validity_range(min_days: int, max_days: int, session: Session = Depends(get_session)):
    
    res = {}
    select_plans = (select(Jioplansprices)
                    .join(jioplansbenefits)
                    .where(col(jioplansbenefits.benefitname) == "Pack validity")
                    .options(selectinload(Jioplansprices.plan))
                    .distinct(Jioplansprices.uid))
    
    plans = session.exec(select_plans).all()
    
    filtered_plans = [
        plan for plan in plans
        if min_days <= extract_numeric_value([b.benefitvalue for b in plan.plan 
                                             if b.benefitname == "Pack validity"][0]) <= max_days
    ]
    
    res["validity"] = [
        {
            "plan": [
                {benefit.benefitname: benefit.benefitvalue}
                for benefit in plan.plan
                if benefit.benefitname not in ('id', 'uid', 'dfid', 'category')
            ]
        }
        for plan in filtered_plans
    ]
    return res


@app.get("/filter-plans-by-data")
def get_plans_by_data_range(min_gb: float, max_gb: float, session: Session = Depends(get_session)):
    
    res = {}
    select_plans = (select(Jioplansprices)
                    .join(jioplansbenefits)
                    .where(col(jioplansbenefits.benefitname) == "Total data")
                    .options(selectinload(Jioplansprices.plan))
                    .distinct(Jioplansprices.uid))
    
    plans = session.exec(select_plans).all()
    
    filtered_plans = [
        plan for plan in plans
        if min_gb <= extract_numeric_value([b.benefitvalue for b in plan.plan 
                                           if b.benefitname == "Total data"][0]) <= max_gb
    ]
    
    res["data"] = [
        {
            "plan": [
                {benefit.benefitname: benefit.benefitvalue}
                for benefit in plan.plan
                if benefit.benefitname not in ('id', 'uid', 'dfid', 'category')
            ]
        }
        for plan in filtered_plans
    ]
    return res

def main():
    print("Hello from bestrechargeplanfinder!")


if __name__ == "__main__":
    main()