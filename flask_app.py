from flask import Flask, request, redirect, jsonify
import pyodbc

app = Flask(__name__)

conn_str = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost,1433;"
    "DATABASE=userDB;"
    "UID=sa;"
    "PWD=Test@123"
)

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data['username']
    email = data['email']
    password = data['password']

    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Users WHERE Username = ? OR Email = ?", (username, email))
    existing_user = cursor.fetchone()

    if existing_user:
        conn.close()
        return redirect("http://127.0.0.1:8000/signup_failed/")
        # return jsonify({"error": "Username or email already exists"}), 400

    cursor.execute("""
        INSERT INTO Users (Username, Email, Password)
        VALUES (?, ?, ?)
    """, (username, email, password))
    conn.commit()
    conn.close()

    # print("Data successfully inserted into DB!")

    return redirect("http://127.0.0.1:8000/signup_success/")

@app.route('/signin', methods=['POST'])
def signin():
    data = request.get_json()
    username = data['username']
    password = data['password']

    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Users WHERE Username = ? AND Password = ?", (username, password))
    existing_user = cursor.fetchone()

    if existing_user:
        user_data = {
            "username": existing_user[1],  # 假設資料庫中的用戶名在第二列
            "email": existing_user[2],     # 假設資料庫中的郵箱在第三列
            # 可以根據實際情況添加更多的資料項目
        }        
        conn.close()
        return redirect(f"http://127.0.0.1:8000/signin_success/?username={username}&email={user_data['email']}")
    
        # return jsonify({"error": "Username or email already exists"}), 400
    else:
        conn.close()
        return redirect("http://127.0.0.1:8000/signup_failed/")
    conn.commit()
    conn.close()

    # print("Data successfully inserted into DB!")

    return redirect("http://127.0.0.1:8000/signup_success/")



if __name__ == '__main__':
    app.run(port=5000)
