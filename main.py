from fastapi import FastAPI, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel, Field, Session, create_engine, select, col, Relationship
from typing import  Annotated
from sqlalchemy.orm import selectinload
import os
from dotenv import load_dotenv
load_dotenv()
db_url = os.getenv("DATABASE_URL")

app = FastAPI()
origins=['http://localhost:8501','https://mobilerechargeplanfinder.onrender.com/']
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
        if benefit.benefitname not in ('id', 'uid', 'dfid','category', 'price'):
            grouped.setdefault(benefit.id, []).append({
                benefit.benefitname:benefit.benefitvalue
            }
            )

    resultids = []
    for plan in plans:
        resultids.append({
            "benefits": grouped.get(plan.id, [])
        })
    return resultids

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
def main():
    print("Hello from bestrechargeplanfinder!")


if __name__ == "__main__":
    main()