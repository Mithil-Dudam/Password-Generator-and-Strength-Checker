# Password Generator and Strength Checker

from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random
import string

app=FastAPI()

origins = ['http://localhost:5173']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Choice(BaseModel):
    length:int
    upper:bool
    number:bool
    symbol:bool

class Password(BaseModel):
    password:str

@app.post("/generate",status_code=status.HTTP_200_OK)
async def generate(user:Choice):
    possiblelist=list(string.ascii_lowercase)
    if user.upper == True:
        possiblelist+=list(string.ascii_uppercase)
    if user.number == True:
        possiblelist+=list("0123456789")
    if user.symbol == True:
        possiblelist+=list(string.punctuation)
    password = "".join(random.choice(possiblelist) for _ in range(user.length))
    return {"password":password}

@app.post("/check",status_code=status.HTTP_200_OK)
async def check(user:Password):
    lowletters=0
    upletters=0
    nums=0
    syms=0
    password = user.password.strip()
    for i in password:
        if i == " ":
            pass
        elif i in list(string.ascii_lowercase):
            lowletters+=1
        elif i in list(string.ascii_uppercase):
            upletters+=1
        elif i in list(string.punctuation):
            syms+=1
        else:
            nums+=1
    if(len(password)<6):
        return {"result":"Weak (Short Length)","lowercase":lowletters,"uppercase":upletters,"numbers":nums,"symbols":syms}
    elif(nums==0 and syms==0):
        return {"result":"Weak (Only Letters)","lowercase":lowletters,"uppercase":upletters,"numbers":nums,"symbols":syms}
    elif(syms==0 and (lowletters==0 and nums !=0))or(syms==0 and (upletters==0 and nums !=0)or(syms==0 and nums!=0)):
        return {"result":"Medium (No Symbols)","lowercase":lowletters,"uppercase":upletters,"numbers":nums,"symbols":syms}
    elif(nums==0 and (lowletters!=0 and syms!=0))or(nums==0 and (upletters!=0 and syms!=0))or(nums==0 and syms!=0):
        return {"result":"Medium (No Numbers)","lowercase":lowletters,"uppercase":upletters,"numbers":nums,"symbols":syms}
    elif(lowletters !=0 or upletters !=0) and (nums !=0 and syms !=0):
        return {"result":"Strong (Includes letters, numbers and special characters)","lowercase":lowletters,"uppercase":upletters,"numbers":nums,"symbols":syms}
