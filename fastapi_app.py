from fastapi import FastAPI, Form, HTTPException, Response
import requests
from fastapi.responses import RedirectResponse
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

app = FastAPI()
templates = Jinja2Templates(directory="E:\codes\python\dj-fsk-fapi\myproject\myapp\templates")



@app.post("/signup/")
async def signup(username: str = Form(...), email: str = Form(...), password: str = Form(...)):
    # 將數據轉發到 Flask 後端
    payload = {
        "username": username,
        "email": email,
        "password": password
    }
    print(payload)
    try:
        response = requests.post("http://127.0.0.1:5000/signup", json=payload, allow_redirects=False)
        response.raise_for_status()  # 檢查是否有 HTTP 錯誤

        if response.status_code == 302:
            return Response(status_code=302, headers={"Location": response.headers["Location"]})

        elif response.status_code == 400:
            # return {"error": response.json().get("error")}
            return RedirectResponse(url="http://127.0.0.1:8000/signup_failed/")
        
    except requests.exceptions.RequestException as e:
        # 捕捉 HTTP 請求錯誤並返回 500 狀態碼和錯誤信息
        raise HTTPException(status_code=500, detail=str(e))
    
    return {"message": "Sign up successful"}


@app.post("/signin/")
async def signup(username: str = Form(...),  password: str = Form(...)):
    # 將數據轉發到 Flask 後端
    payload = {
        "username": username,
        "password": password
    }
    print(payload)
    try:
        response = requests.post("http://127.0.0.1:5000/signin", json=payload, allow_redirects=False)
        response.raise_for_status()  # 檢查是否有 HTTP 錯誤

        if response.status_code == 302:
            return Response(status_code=302, headers={"Location": response.headers["Location"]})

        elif response.status_code == 400:
            # return {"error": response.json().get("error")}
            return RedirectResponse(url="http://127.0.0.1:8000/signup_failed/")
        
    except requests.exceptions.RequestException as e:
        # 捕捉 HTTP 請求錯誤並返回 500 狀態碼和錯誤信息
        raise HTTPException(status_code=500, detail=str(e))
    
    return {"message": "Sign in successful"}

# 定义API的URL

# 发送GET请求获取数据并处理
def fetch_data_and_plot():
    url = 'https://openapi.twse.com.tw/v1/exchangeReport/STOCK_DAY_ALL'
    res = requests.get(url)
    jsondata = res.json()
    df = pd.DataFrame(jsondata)
    df.set_index("Code", inplace=True)
    df.replace('', '0', inplace=True)
    df[df.columns.difference(['Name'])] = df[df.columns.difference(['Name'])].astype(float)
    top10_closing = df.nlargest(10, 'ClosingPrice')

    plt.figure(figsize=(15, 6))
    bars = plt.bar(top10_closing['Name'], top10_closing['ClosingPrice'], color='skyblue')
    plt.title('Top 10 Closing Prices', fontsize=20)
    plt.xlabel('Stock Name', fontsize=20)
    plt.ylabel('Closing Price', fontsize=20)
    plt.xticks(fontsize=12, rotation=45)
    plt.tight_layout()

    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval, round(yval, 2), ha='center', va='bottom', fontsize=12)

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plot_data = base64.b64encode(buffer.read()).decode()
    plt.close()

    return plot_data

# 首页路由
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# 登录成功页面路由
@app.post("/signin_success/", response_class=HTMLResponse)
async def signin_success(request: Request, username: str = Form(...), password: str = Form(...)):
    # plot_data = fetch_data_and_plot()
    return templates.TemplateResponse("signin_success.html", {"request": request, "username": username, "plot_data": plot_data})