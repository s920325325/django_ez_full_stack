# 引入requests庫
import requests  
import matplotlib as plt
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] # 修改中文字體
plt.rcParams['axes.unicode_minus'] = False # 顯示負號

# 定義API的URL
url = 'https://openapi.twse.com.tw/v1/exchangeReport/STOCK_DAY_ALL'  
# 發送GET請求
res = requests.get(url)  
# res


import json

jsondata = json.loads(res.text)
# jsondata


# 引入pandas庫
import pandas as pd  
# 將JSON數據轉換為DataFrame
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
print(top10_closing)
# 視覺化
# plt.figure(figsize=(15, 6))
# bars = plt.bar(top10_closing['Name'], top10_closing['ClosingPrice'], color='skyblue')
# plt.title('Top 10 Closing Prices',fontsize=20)
# plt.xlabel('Stock Name',fontsize=20)
# plt.ylabel('Closing Price',fontsize=20)
# plt.xticks(fontsize=20)
# # 在每個條形圖上顯示對應的股價
# for bar in bars:
#     yval = bar.get_height()
#     plt.text(bar.get_x() + bar.get_width()/2, yval, round(yval, 2), ha='center', va='bottom', fontsize=12)

# plt.show()
