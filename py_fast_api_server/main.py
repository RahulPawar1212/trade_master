from typing import Union
import requests
from fastapi import FastAPI
import json
import os
from dotenv import load_dotenv

app = FastAPI()

# Load environment variables from .env file
load_dotenv()

requestToken:str = "Not Found"
accessToken:str = "Not Found"
refreshToken:str = "Not Found"
status:str = "Failed!"
cookie = ""

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.get("/getrequesttoken/")
async def connection():
    url = "https://Openapi.5paisa.com/VendorsAPI/Service1.svc/TOTPLogin"
    headers = {"Content-Type": "application/json"}
    data =  {
    "head": {
        "Key": os.getenv('User_Key')
    },
    "body": {
        "Email_ID": os.getenv('Email_ID'),
        "TOTP": os.getenv('TOTP'),
        "PIN": os.getenv('PIN')
    }
    }
    try:
        response = requests.post(url, json=data, headers=headers).content
        return json.loads(response)
    except Exception as e:
        return e

@app.get("/getaccesstoken/")
def connection():
    requestTokenReqest = requests.get("http://127.0.0.1:8000/getrequesttoken/")
    requestTokenJson = json.loads(requestTokenReqest.content)
    global requestToken 
    requestToken = requestTokenJson["body"]["RequestToken"]
    print(requestToken)
    url = "https://Openapi.5paisa.com/VendorsAPI/Service1.svc/GetAccessToken"
    headers = {"Content-Type": "application/json"}
    data =  {
    "head": {
        "Key": os.getenv('User_Key')
    },
    "body": {
        "RequestToken":requestToken,
        "EncryKey": os.getenv('EncryKey'),
        "UserId": os.getenv('UserId')
    }
    }
    try:
        response = requests.post(url, json=data, headers=headers)
        global cookie
        cookie = response.cookies
        #print( "Cookie",response.cookies.get('NSC_JOh0em50e1pajl5b5jvyafempnkehc3'), response.cookies)
        return json.loads(response.content)
    except Exception as e:
        return e
    #return accessToken


@app.get("/login/")
def connection():
    try:
        accessTokenRequest = requests.get("http://127.0.0.1:8000/getaccesstoken/")
        accessTokenRequestJson = json.loads(accessTokenRequest.content)
        global accessToken,refreshToken,status
        #print(accessToken)
        accessToken = accessTokenRequestJson["body"]["AccessToken"]
        refreshToken = accessTokenRequestJson["body"]["RefreshToken"]
        status = accessTokenRequestJson["body"]["Message"]
        #print(accessToken)
        return accessToken,refreshToken,status
    except Exception as e:
        return e,accessToken,refreshToken,status
    

@app.get("/holdings/")
async def connection_new():
    global accessToken
    url = "https://Openapi.5paisa.com/VendorsAPI/Service1.svc/V3/Holding"
    token = "bearer " + accessToken
    headers = {"Authorization": token,
                "Content-Type": "application/json"
                }
    #print(headers)
    data =  {
    "head": {
        "Key": os.getenv('User_Key')
    },
    "body": {
        "ClientCode": os.getenv('ClientCode')
    }
    }
    try:

        response = requests.post(url, json=data, headers=headers,cookies=cookie)
        #print(cookie)
        return json.loads(response.content), response.cookies
    except Exception as e:
        return e
    
@app.get("/marketdept/")
async def connection_new():
    with open('../scriptmaster copy.json', 'r') as json_file:
        scripMasterData = json.load(json_file)
    global accessToken
    url = "https://Openapi.5paisa.com/VendorsAPI/Service1.svc/MarketDepth"
    token = "bearer " + accessToken
    headers = {"Authorization": token,
                "Content-Type": "application/json"
            }
    #print(headers)
    data =  {
    "head": {
        "key": os.getenv('User_Key')
    },
    "body": {
        "ClientCode": os.getenv('ClientCode'),
        "Count": "1",
        "Data": scripMasterData
            # [
            # {
            #     "Exchange": "N",
            #     "ExchangeType": "C",
            #     "ScripCode": "2885"
            # },
            # {
            #     "Exchange": "N",
            #     "ExchangeType": "C",
            #     "ScripCode": "15179"
            # }]
    }
}
    try:
        response = requests.post(url, json=data, headers=headers,cookies=cookie)
        print(data)
        print(cookie)
        return json.loads(response.content)
    except Exception as e:
        return e  







@app.get("/connect_2/")
async def connections():
    url = 'http://127.0.0.1:5500/test.xml'
    headers = {"Content-Type": "application/json"}
    data = {'somekey': 'somevalue'}

    # try:
    response = requests.get(url).content
    #     return response
    # except Exception as e:
    #     return e
    return {"data": response} 


    