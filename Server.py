import threading
import time
from socket import *
from DB_Admin import *
import pickle

HOST = "127.0.0.1"
PORT = 4455
ADDRESS = (HOST, PORT)
BUFSIZE = 1024

socket = socket(AF_INET, SOCK_STREAM)
socket.bind(ADDRESS)
socket.listen(5)

db = Database("127.0.0.1", "root", "1234", "Exchange_DB")
db.connect()


def gain_loss(client, info):
    ID = info['gain_loss']
    query = f"SELECT SUM(VALUE_CASH) FROM Assets_portofolio WHERE UserID='{ID}';"
    current_value = db.execute(query)
    query2 = f"SELECT Total_Investment FROM user_info WHERE UserID='{ID}';"
    total_investment = db.execute(query2)

    if current_value[0][0] is not None:
        total_investment = float(total_investment[0][0])
        current_value = float(current_value[0][0])
        gain_loss = current_value - total_investment
        gain_loss = round(gain_loss, 2)
        client.send(str(gain_loss).encode())
    else:
        gain_loss = 0
        client.send(str(gain_loss).encode())


def request_amount(client, info):
    info = info['request_amount']
    ID = info[0]
    name = info[1]
    query = f"SELECT Amount FROM Assets_portofolio WHERE UserID='{ID}' AND Asset_Name='{name}';"
    result = db.execute(query)
    db.commit()
    amount_owned = result[0][0] if result else None
    amount_owned = str(amount_owned)
    client.send(amount_owned.encode())


def add_investment(info):
    info = info['add_investment']
    ID = info[0]
    cost = info[1]
    query = f"UPDATE user_info SET Total_Investment = Total_Investment + {cost} WHERE UserID='{ID}';"
    db.execute(query)
    db.commit()


def sub_investment(info):
    info = info['sub_investment']
    ID = info[0]
    cost = info[1]
    query = f"UPDATE user_info SET Total_Investment = Total_Investment - {cost} WHERE UserID='{ID}';"
    db.execute(query)
    db.commit()


def update_portfolio_value():
    while True:
        query = "SELECT UserID, Asset_Name, Amount FROM Assets_portofolio;"
        result = db.execute(query)
        db.commit()
        for row in result:
            user_id = row[0]
            asset_name = row[1]
            amount = row[2]
            query = f"SELECT Price FROM Price WHERE Asset_Name='{asset_name}';"
            result = db.execute(query)
            db.commit()
            price_str = result[0][0] if result else None
            price = float(price_str.replace(',', ''))
            value = round((float(price) * float(amount)), 2)
            query = f"UPDATE Assets_portofolio SET VALUE_CASH={value} WHERE UserID='{user_id}' AND Asset_Name='{asset_name}';"
            db.execute(query)
        db.commit()
        time.sleep(10)


thread2 = threading.Thread(target=update_portfolio_value)
thread2.start()


def request_owned(client, ID):
    ID = info['request_owned']
    query = f"SELECT * FROM Assets_portofolio WHERE UserID='{ID}';"
    owned = db.execute(query)
    db.commit()
    client.send(pickle.dumps(owned))


def request_portofolio(client, info):
    ID = info['request_portofolio']
    query = f"SELECT * FROM transactions WHERE UserID='{ID}';"
    trans = db.execute(query)
    db.commit()
    client.send(pickle.dumps(trans))


def add_asset(info):
    info = info['asset_bought']
    ID = info[0]
    asset_name = info[1]
    amount = info[2]
    query = f"SELECT * FROM Assets_portofolio WHERE UserID='{ID}' AND Asset_Name='{asset_name}';"
    result = db.execute(query)
    if result:
        old_amount = result[0][2]
        new_amount = float(old_amount) + float(amount)
        query = f"UPDATE Assets_portofolio SET Amount={new_amount} WHERE UserID='{ID}' AND Asset_Name='{asset_name}';"
    else:
        query = f"INSERT INTO Assets_portofolio (UserID, Asset_Name, Amount) VALUES ('{ID}', '{asset_name}', '{amount}')"
    db.execute(query)


def sell_asset(info):
    info = info['asset_sold']
    ID = info[0]
    asset_name = info[1]
    amount = info[2]
    query = f"SELECT * FROM Assets_portofolio WHERE UserID='{ID}' AND Asset_Name='{asset_name}';"
    result = db.execute(query)
    if result:
        old_amount = result[0][2]
        new_amount = float(old_amount) - float(amount)
        query = f"UPDATE Assets_portofolio SET Amount={new_amount} WHERE UserID='{ID}' AND Asset_Name='{asset_name}';"
        db.execute(query)


def insert_transaction(info):
    info = info['insert_transaction']
    fields = 'UserID, Asset_Name, Tran_Date, Buy_Sell, Quantity, Tran_Value'
    values = f'"{info[0]}", "{info[1]}", "{info[2]}", "{info[3]}", {info[4]}, {info[5]}'
    query = f"INSERT INTO Transactions ({fields}) VALUES ({values})"
    return db.execute(query)


def update_balance(info):
    ID = info['update_balance'][0]
    new_balance = info['update_balance'][1]
    query = f"UPDATE user_info SET Balance={new_balance} WHERE UserID='{ID}';"
    db.execute(query)
    db.commit()


def request_prices(client, info):
    table_name = info['request_prices']
    query = f"SELECT Asset_Name, Price FROM {table_name};"
    result = db.execute(query)
    db.commit()
    prices = {}
    for row in result:
        name = row[0]
        price = row[1]
        prices[name] = price
    client.send(str(prices).encode())


def request_investment(client, info):
    ID = info['request_investment']
    query = f"SELECT Total_Investment FROM user_info WHERE UserID='{ID}';"
    result = db.execute(query)
    db.commit()
    investment = result[0][0] if result else None
    investment = str(investment)
    client.send(investment.encode())


def request_balance(client, info):
    ID = info['request_balance']
    query = f"SELECT Balance FROM user_info WHERE UserID='{ID}';"
    result = db.execute(query)
    db.commit()
    balance = result[0][0] if result else None
    balance = str(balance)
    client.send(balance.encode())


def insert_acc_info(info):
    db.insert_into('user_info', 'UserID, First_Name, Last_Name, Password, Balance, Total_investment',
                   info['user_information'])
    db.commit()


def login_check(client, info):
    values_list = info['login']
    ID = values_list[0]
    PW = values_list[1]
    query = f"SELECT UserID, Password FROM user_info WHERE UserID='{ID}' AND Password='{PW}';"
    result = db.execute(query)
    if result:
        message = "Login successful"
    else:
        message = 'Denied'
    message = message.encode()
    client.send(message)


def update_price_table():
    while True:
        db.update_price()
        time.sleep(10)


thread1 = threading.Thread(target=update_price_table)
thread1.start()

while True:
    print("Waiting for connection...")
    (client, address) = socket.accept()
    print(f"...connected successfully from {address}")

    while True:
        received = client.recv(BUFSIZE)
        info = pickle.loads(received)
        if 'user_information' in info:
            insert_acc_info(info)
        elif 'login' in info:
            login_check(client, info)
        elif 'request_balance' in info:
            request_balance(client, info)
        elif 'request_investment' in info:
            request_investment(client, info)
        elif 'request_prices' in info:
            request_prices(client, info)
        elif 'update_balance' in info:
            update_balance(info)
        elif 'insert_transaction' in info:
            insert_transaction(info)
        elif 'request_portofolio' in info:
            request_portofolio(client, info)
        elif 'asset_bought' in info:
            add_asset(info)
        elif 'add_investment' in info:
            add_investment(info)
        elif 'request_amount' in info:
            request_amount(client, info)
        elif 'asset_sold' in info:
            sell_asset(info)
        elif 'sub_investment' in info:
            sub_investment(info)
        elif 'gain_loss' in info:
            gain_loss(client, info)
        elif 'request_owned' in info:
            request_owned(client, info)
        else:
            break

    client.close()
