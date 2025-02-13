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








# print("Password Generator & Strength Checker!\n")

# def inp():
#     choice = input("Enter Choice: ")
#     if(choice.isdigit()):
#         choice=int(choice)
#         if(1<=choice<=6):
#             return choice
#         else:
#             print("Invalid Input, Number must be from 1 to 3.\n")
#             return inp()
#     else:
#         print("Invalid Input, Please choose a number.\n")
#         return inp()

# def uppercase():
#     upper = input("Include uppercase letters ? (y/n): ").strip().lower()
#     if upper != "y" and upper != "n":
#         print("Invalid Input. Enter 'y' for yes or 'n' for no.\n")
#         return uppercase()
#     return upper

# def numbers():
#     number = input("Include numbers ? (y/n): ").strip().lower()
#     if number != "y" and number != "n":
#         print("Invalid Input. Enter 'y' for yes or 'n' for no.\n")
#         return numbers()
#     return number

# def symbols():
#     symbol = input("Include symbols ? (y/n): ").strip().lower()
#     if symbol != "y" and symbol != "n":
#         print("Invalid Input. Enter 'y' for yes or 'n' for no.\n")
#         return symbols()
#     return symbol

# def gen():
#     password=""
#     length = input("Enter length of password: ")
#     if(length.isdigit()):
#         length=int(length)
#         if(0<length<=50):
#             upper = uppercase()
#             number = numbers()
#             symbol = symbols()

#             possiblelist=list(string.ascii_lowercase)
#             if upper == "y":
#                 possiblelist+=list(string.ascii_uppercase)
#             if number == "y":
#                 possiblelist+=list("0123456789")
#             if symbol == "y":
#                 possiblelist+=list(string.punctuation)
#             password = "".join(random.choice(possiblelist) for _ in range(length))
#             return password

#         else:
#             print("Password Length must be atleast 1 and max 50 characters.\n")
#             return gen()
#     else:
#         print("Invalid Input! Please enter a Valid length.\n")
#         return gen()

# def check():
#     lowletters=0
#     upletters=0
#     nums=0
#     syms=0
#     password=input("Enter password: ").strip()
#     if not password:
#         print("Cant enter an empty password.\n")
#         return check()
#     for i in password:
#         if i in list(string.ascii_lowercase):
#             lowletters+=1
#         elif i in list(string.ascii_uppercase):
#             upletters+=1
#         elif i in list(string.punctuation):
#             syms+=1
#         elif(i==" "):
#             pass
#         else:
#             nums+=1
#     print(f"\nYour password contains:\n{lowletters} Lowercase letters")
#     print(f"{upletters} Uppercase letters")
#     print(f"{nums} Numbers")
#     print(f"{syms} Symbols\n")

#     if(len(password)<6):
#         print("Password Strength: Weak (Short Length)\n")
#     elif(nums==0 and syms==0):
#         print("Password Strength: Weak (Only Letters)\n")
#     elif(syms==0 and (lowletters==0 and nums !=0))or(syms==0 and (upletters==0 and nums !=0)or(syms==0 and nums!=0)):
#         print("Password Strength: Medium (No Symbols)\n")
#     elif(nums==0 and (lowletters!=0 and syms!=0))or(nums==0 and (upletters!=0 and syms!=0))or(nums==0 and syms!=0):
#         print("Password Strength: Medium (No Numbers)\n")
#     elif(lowletters !=0 or upletters !=0) and (nums !=0 and syms !=0):
#         print("Password Strength: Strong (Includes letters, numbers and special characters)\n")

# def leave():
#     print("Thank You!")
#     exit()

# while True:
#     print("1. Generate a Password")
#     print("2. Check Strength of Password")
#     print("3. Exit\n")
#     choice = inp()
#     if choice == 1:
#         password=gen()
#         print(f"\nGenerated Password: {password}\n")
#     elif choice == 2:
#         check()
#     else:
#         leave()