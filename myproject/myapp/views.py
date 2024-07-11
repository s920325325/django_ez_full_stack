from django.shortcuts import render
from django.http import HttpResponseRedirect
import requests
import json
import pandas as pd
def index(request):
    return render(request, 'index.html')

def login(request):  # 添加這個視圖
    return render(request, 'login.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # 将数据发送到 FastAPI
        payload = {
            "username": username,
            "email": email,
            "password": password
        }
        response = requests.post("http://127.0.0.1:8001/signup/", data=payload)

        if response.status_code == 200:
            return HttpResponseRedirect('/signup_success/')
    return render(request, 'signup.html')

def signup_success(request):
    return render(request, 'signup_success.html')

def signup_failed(request):
    return render(request, 'signup_failed.html')


def signin_success(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # 将数据发送到 FastAPI
        payload = {
            "username": username,
            "password": password
        }
        response = requests.post("http://127.0.0.1:8001/signin/", data=payload)

        if response.status_code == 200:
            return HttpResponseRedirect('/signin_success/')
    return render(request, 'signin_success.html')

def display_stock_data(request):
    url = 'https://openapi.twse.com.tw/v1/exchangeReport/STOCK_DAY_ALL'
    try:
        res = requests.get(url)  
        # res

        jsondata = json.loads(res.text)
        df = pd.DataFrame(jsondata)
        # 將"Code"列設置為索引
        df.set_index("Code", inplace=True)
        # 將空字符串替換為'0'
        df.replace('', '0', inplace=True)
        # 將除了"Name"列以外的所有列轉換為浮點數
        df[df.columns.difference(['Name'])] = df[df.columns.difference(['Name'])].astype(float)
        # 顯示DataFrame

        # 按收盤價排序並選取前10大收盤價的股票
        top10_closing = df.nlargest(10, 'ClosingPrice')
        table_html = top10_closing.to_html(classes='table table-striped')
        return render(request, 'stock_data.html', {'table_html': table_html})
    
    except Exception as e:
        error_message = f"Error fetching data: {e}"
        print(error_message)  # 添加調試語句
        return render(request, 'error.html', {'error_message': error_message})
        # print(top10_closing)