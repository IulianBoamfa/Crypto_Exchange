from socket import *
import random
from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
from tkinter import ttk
import threading
import time
from datetime import datetime
import pickle


def request_gain_loss(ID):
    send_info('gain_loss', ID)
    gain_loss = socket.recv(BUFSIZE).decode()
    return gain_loss


def request_amount_owned(ID, name):
    info = [ID, name]
    send_info('request_amount', info)
    amount_owned = socket.recv(BUFSIZE).decode()
    return amount_owned


def deposit_withdraw_click(ID, balance):
    def deposit_click(ID, amount):
        # Check if amount is provided
        if not amount:
            messagebox.showerror('Error', 'Please enter an amount.')
            return

        balance = request_balance(ID)
        new_balance = eval(balance) + eval(amount)
        info = [ID, round(new_balance, 2)]
        send_info('update_balance', info)

        # Update the balance label
        balance_label.config(text=f'Current balance: ${round(new_balance, 2)}')

        # Clear the amount entry
        amount_entry.delete(0, END)

    def withdraw_click(ID, amount):
        balance = request_balance(ID)

        # Check if amount is provided
        if not amount:
            messagebox.showerror('Error', 'Please enter an amount.')
            return

        # Check if balance is sufficient
        if eval(amount) > eval(balance):
            messagebox.showerror('Error', 'Insufficient balance.')
            return

        new_balance = eval(balance) - eval(amount)
        info = [ID, round(new_balance, 2)]
        send_info('update_balance', info)

        # Update the balance label
        balance_label.config(text=f'Current balance: ${round(new_balance, 2)}')

        # Clear the amount entry
        amount_entry.delete(0, END)

    def cancel_click():
        deposit_window.destroy()

    deposit_window = Toplevel(root)
    deposit_window.title('Deposit/Withdraw')

    # Set the width and height of the invest window
    width = 450
    height = 300

    # Calculate the x-coordinate and y-coordinate of the invest window
    x = root.winfo_x() + (root.winfo_width() - width) // 2
    y = root.winfo_y() + (root.winfo_height() - height) // 2

    # Set the geometry of the invest window
    deposit_window.geometry("%dx%d+%d+%d" % (width, height, x, y))

    balance = float(balance)
    balance_label = Label(deposit_window, text=f'Current balance: ${balance:.2f}', font=('Arial', 18))
    balance_label.grid(row=0, column=0, padx=20, pady=20, sticky='w', columnspan=3)

    amount_label = Label(deposit_window, text='Amount: ', font=('Arial', 18))
    amount_label.grid(row=1, column=0, padx=20, pady=20, sticky='w')

    amount_entry = Entry(deposit_window, width=40)
    amount_entry.grid(row=1, column=1, padx=20, pady=10, sticky='w', columnspan=2)

    # Add the deposit button
    deposit_button = Button(deposit_window, text='Deposit', command=lambda: deposit_click(ID, amount_entry.get()),
                            font=('Arial', 18))
    deposit_button.grid(row=2, column=0, padx=20, pady=(50, 20), sticky='nsew')

    # Add the withdraw button
    withdraw_button = Button(deposit_window, text='Withdraw', command=lambda: withdraw_click(ID, amount_entry.get()),
                             font=('Arial', 18))
    withdraw_button.grid(row=2, column=1, padx=20, pady=(50, 20), sticky='nsew')

    # Add the cancel button
    cancel_button = Button(deposit_window, text='Cancel', command=cancel_click, font=('Arial', 18))
    cancel_button.grid(row=2, column=2, padx=20, pady=(50, 20), sticky='nsew')


def request_owned(ID):
    send_info('request_owned', ID)
    owned = pickle.loads(socket.recv(BUFSIZE))
    return owned


def request_portofolio(ID):
    send_info('request_portofolio', ID)
    portofolio = pickle.loads(socket.recv(BUFSIZE))
    return portofolio


def portofolio_click(ID):
    portofolio_window = Toplevel(root)
    portofolio_window.title('Portfolio Viewing')

    # Set the width and height of the portfolio window
    width = 1200
    height = 600

    # Calculate the x-coordinate and y-coordinate of the portfolio window
    x = root.winfo_x() + (root.winfo_width() - width) // 2
    y = root.winfo_y() + (root.winfo_height() - height) // 2

    # Set the geometry of the portfolio window
    portofolio_window.geometry("%dx%d+%d+%d" % (width, height, x, y))

    # Define the columns for the Treeview
    columns = ["UserID", "Asset_Name", "Date", "Transaction_Type", "Quantity", "Transaction_Value"]

    # Create the Treeview widget for the transactions table
    tree_transactions = ttk.Treeview(portofolio_window, columns=columns, show="headings")

    # Set the headings for the Treeview columns
    for col in columns:
        tree_transactions.heading(col, text=col)

    # Add the transaction data to the Treeview
    transactions = request_portofolio(ID)
    for trans in transactions:
        tree_transactions.insert("", "end", values=trans)

    # Create the Treeview widget for the owned assets table
    columns_owned = ["UserID", "Asset_Name", "Amount", "VALUE_CASH"]
    tree_owned = ttk.Treeview(portofolio_window, columns=columns_owned, show="headings")

    # Set the headings for the Treeview columns
    for col in columns_owned:
        tree_owned.heading(col, text=col)

    # Add the owned data to the Treeview
    owned = request_owned(ID)
    for asset in owned:
        tree_owned.insert("", "end", values=asset)

    # Add the Treeviews to the window
    tree_transactions.pack(side=TOP, padx=10, pady=10)
    tree_owned.pack(side=TOP, padx=10, pady=10)

    balance = request_balance(ID)
    # Add the 'Go to buy/sell' button
    button_invest = ttk.Button(portofolio_window, text="Go to buy/sell",
                               command=lambda: (portofolio_window.destroy(), invest_click(balance, ID)))
    button_invest.pack(side=BOTTOM, padx=10, pady=10)


def request_balance(ID):
    send_info('request_balance', ID)
    balance = socket.recv(BUFSIZE).decode()
    return balance


def request_investment(ID):
    send_info('request_investment', ID)
    investment = socket.recv(BUFSIZE).decode()
    return investment


def invest_click(balance, ID):
    invest_window = Toplevel(root)
    invest_window.title('Invest')

    # Set the width and height of the invest window
    width = 1000
    height = 600

    # Calculate the x-coordinate and y-coordinate of the invest window
    x = root.winfo_x() + (root.winfo_width() - width) // 2
    y = root.winfo_y() + (root.winfo_height() - height) // 2

    # Set the geometry of the invest window
    invest_window.geometry("%dx%d+%d+%d" % (width, height, x, y))

    columns = ('Name', 'Price')
    table = ttk.Treeview(invest_window, columns=columns, show='headings', selectmode='browse')

    table.column('Name', width=400)
    table.column('Price', width=200)
    table.heading('Name', text='Name')
    table.heading('Price', text='Price')
    table.pack()

    def update_prices():
        def update():
            # Request prices from the server
            table_name = 'Price'
            send_info('request_prices', table_name)
            prices = socket.recv(BUFSIZE).decode()
            prices_dict = eval(prices)

            # Clear the table
            for item in table.get_children():
                table.delete(item)

            # Add the prices to the table
            for name, price in prices_dict.items():
                table.insert('', 'end', values=(name, price))

            # Schedule the next update
            invest_window.after(10000, update)

        # Start updating the prices in a separate thread
        thread = threading.Thread(target=update)
        thread.daemon = True
        thread.start()

    # Start updating the prices
    update_prices()

    balance = float(balance)
    balance_label = Label(invest_window, text=f'Balance: ${balance:.2f}', font=('Arial', 18))
    balance_label.place(x=20, y=250)

    name_label = Label(invest_window, text='Select your investment inside the table.', font=('Arial', 18))
    name_label.place(x=20, y=300)

    # Get the list of names from the table
    names = [table.item(child)['values'][0] for child in table.get_children()]

    # Set the default value of the name
    name = names[0] if names else None

    # Create a label for the name
    name_value_label = Label(invest_window, text=name, font=('Arial', 18))
    name_value_label.place(x=300, y=305)

    # Create a label and entry for the amount of shares
    amount_label = Label(invest_window, text='Insert amount:', font=('Arial', 18))
    amount_label.place(x=20, y=400)

    amount_entry = Entry(invest_window, font=('Arial', 18))
    amount_entry.place(x=300, y=405)

    # Create a button to calculate the transaction

    def buy_transaction(ID):
        try:
            selected_item = table.selection()[0]  # get iid of selected item
        except IndexError:
            messagebox.showerror('Error', 'Please select an investment.')
            return

        if not selected_item:
            messagebox.showerror('Error', 'Please select an investment.')
            return
        name = table.item(selected_item)['values'][0]  # get name of selected investment
        price_str = table.item(selected_item)['values'][1]  # pass iid to retrieve values
        price = float(price_str.replace(',', ''))
        amount = amount_entry.get()

        if not amount:
            messagebox.showerror('Error', 'Please enter an amount.')
            return
        else:
            amount = float(amount)

        total_cost = round((price * amount), 2)
        balance = float(request_balance(ID))

        if not amount:
            messagebox.showerror('Error', 'Please enter an amount.')
            return

        if balance >= total_cost:
            confirmation = messagebox.askyesno('Confirm Transaction',
                                               f'Are you sure you want to invest ${total_cost} in {name}?')
            if confirmation:
                # Subtract the total cost from the balance
                balance -= total_cost
                info = [ID, round(balance, 2)]
                send_info('update_balance', info)

                # Update the balance label
                balance_label.config(text=f'Balance: ${balance:.2f}')

                current_time = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

                # Clear the amount entry
                amount_entry.delete(0, END)

                tran_inf = [ID, name, current_time, 'Buy', str(amount), str(total_cost)]
                send_info('insert_transaction', tran_inf)

                # Display transaction details in a messagebox
                tran_details = f'Stock: {name}\nDate: {current_time}\nType: Buy\nQuantity: {amount}\nCost: {total_cost:.2f}'
                messagebox.showinfo('Transaction Details', tran_details)

                asset_bought = [ID, name, str(amount)]
                send_info('asset_bought', asset_bought)

                add_investment = [ID, str(total_cost)]
                send_info('add_investment', add_investment)

            else:
                # User clicked "Cancel"
                return
        else:
            # Show an error message if the balance is not enough
            messagebox.showerror('Error', 'You do not have enough balance for this transaction.')

    def sell_transaction(ID):
        try:
            selected_item = table.selection()[0]  # get iid of selected item
        except IndexError:
            messagebox.showerror('Error', 'Please select an investment.')
            return

        if not selected_item:
            messagebox.showerror('Error', 'Please select an investment.')
            return
        name = table.item(selected_item)['values'][0]  # get name of selected investment
        price_str = table.item(selected_item)['values'][1]  # pass iid to retrieve values
        price = float(price_str.replace(',', ''))
        amount = amount_entry.get()

        if not amount:
            messagebox.showerror('Error', 'Please enter an amount.')
            return
        else:
            amount = float(amount)

        total_cost = round((price * amount), 2)
        balance = float(request_balance(ID))

        if not amount:
            messagebox.showerror('Error', 'Please enter an amount.')
            return

        amount_owned = float(request_amount_owned(ID, name))

        if not amount_owned:
            messagebox.showerror('Error', 'The amount selected is bigger than the amount you actually own.')

        if amount_owned >= amount:
            confirmation = messagebox.askyesno('Confirm Transaction',
                                               f'Are you sure you want to sell {amount}  {name}?')
            if confirmation:
                # Add the total cost from the balance
                balance += total_cost
                balance = round(balance, 2)
                info = [ID, balance]
                send_info('update_balance', info)

                # Update the balance label
                balance_label.config(text=f'Balance: ${balance}')

                current_time = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

                # Clear the amount entry
                amount_entry.delete(0, END)

                tran_inf = [ID, name, current_time, 'Sell', str(amount), str(total_cost)]
                send_info('insert_transaction', tran_inf)

                # Display transaction details in a messagebox
                tran_details = f'Stock: {name}\nDate: {current_time}\nType: Sell\nQuantity: {amount}\nCost: {total_cost}'
                messagebox.showinfo('Transaction Details', tran_details)

                asset_sold = [ID, name, str(amount)]
                send_info('asset_sold', asset_sold)

                sub_investment = [ID, str(total_cost)]
                send_info('sub_investment', sub_investment)

            else:
                # User clicked "Cancel"
                return
        else:
            # Show an error message if the balance is not enough
            messagebox.showerror('Error', 'You do not have enough balance for this transaction.')

    sell_button = Button(invest_window, text='Sell', font=('Arial', 18),
                         command=lambda: sell_transaction(ID))
    sell_button.place(x=90, y=500)

    buy_button = Button(invest_window, text='Buy', font=('Arial', 18),
                        command=lambda: buy_transaction(ID))
    buy_button.place(x=20, y=500)

    cancel_button = Button(invest_window, text='Cancel', font=('Arial', 18),
                           command=invest_window.destroy)
    cancel_button.place(x=160, y=500)


def main_menu_window(id):
    main_menu = Toplevel(root)
    main_menu.title('Main Menu')

    # Set the width and height of the main menu window
    width = 1000
    height = 500

    # Calculate the x-coordinate and y-coordinate of the main menu window
    x = root.winfo_x() + (root.winfo_width() - width) // 2
    y = root.winfo_y() + (root.winfo_height() - height) // 2

    # Set the geometry of the main menu window
    main_menu.geometry("%dx%d+%d+%d" % (width, height, x, y))

    main_menu.columnconfigure(0, weight=1)
    main_menu.columnconfigure(1, weight=1)
    main_menu.columnconfigure(2, weight=1)

    ID = id.upper()

    ID_label = Label(main_menu, text=f'Welcome, {ID}!', font=('Arial', 18))
    ID_label.grid(row=0, column=0, columnspan=3, padx=20, pady=20, sticky='we')

    balance = float(request_balance(ID))

    balance_label = Label(main_menu, text=f'Balance: ${balance:.2f}', font=('Arial', 17))
    balance_label.grid(row=1, column=0, padx=20, pady=20, sticky='w')

    # Function to update the balance label every 2 seconds
    def update_balance():
        nonlocal balance_label
        nonlocal balance
        balance = request_balance(ID)
        balance_label.configure(text=f'Balance: ${balance}')
        main_menu.after(1100, update_balance)

    # Start the update balance loop
    update_balance()

    send_info('request_investment', ID)
    investment = socket.recv(BUFSIZE).decode()

    if investment == 'None':
        investment = 0
    else:
        investment = float(investment)

    investment_label = Label(main_menu, text=f'Total investment: ${investment:.2f}', font=('Arial', 17))
    investment_label.grid(row=1, column=1, padx=20, pady=20, sticky='e')

    def update_investment():
        nonlocal investment_label
        nonlocal investment
        investment = request_investment(ID)

        if investment == 'None':
            investment = 0
        else:
            investment = float(investment)
        investment_label.configure(text=f'Total investment: ${investment:.2f}')
        main_menu.after(1200, update_investment)

    update_investment()

    gain_loss = request_gain_loss(ID)
    gain_loss_label = Label(main_menu, text=f'Gain/Loss: ${gain_loss}', font=('Arial', 17))
    gain_loss_label.grid(row=1, column=2, padx=20, pady=20, sticky='e')

    def update_gain_loss():
        nonlocal gain_loss_label
        nonlocal gain_loss
        gain_loss = request_gain_loss(ID)
        gain_loss = float(gain_loss)
        gain_loss_label.configure(text=f'Gain/Loss: ${gain_loss:.2f}')
        main_menu.after(1300, update_gain_loss)

    update_gain_loss()

    # Create a new row for the buttons
    buttons_row = 3

    # Add the Invest button
    invest_button = Button(main_menu, text='Invest', command=lambda: invest_click(balance, ID), font=('Arial', 18))
    invest_button.grid(row=buttons_row, column=1, padx=20, pady=20, sticky='nsew')

    # Add the View Portfolio button
    portfolio_button = Button(main_menu, text='View Portfolio', command=lambda: portofolio_click(ID),
                              font=('Arial', 18))
    portfolio_button.grid(row=buttons_row + 1, column=1, padx=20, pady=20, sticky='nsew')

    # Add the Deposit/Withdraw button
    deposit_withdraw_button = Button(main_menu, text='Deposit/Withdraw',
                                     command=lambda: deposit_withdraw_click(ID, balance), font=('Arial', 18))
    deposit_withdraw_button.grid(row=buttons_row + 2, column=1, padx=20, pady=20, sticky='nsew')


def login_button(id, password, login_window, root):
    ID = id.upper()
    PW = password
    login = [ID, PW]

    send_info('login', login)

    confirmation = socket.recv(BUFSIZE).decode()
    if confirmation == 'Login successful':
        login_window.withdraw()
        time.sleep(1)
        root.withdraw()
        main_menu_window(id)
    else:
        messagebox.showerror("Error", "Invalid ID or password")


def send_info(info_type, info):
    info_dict = {}
    info_dict[info_type] = info
    socket.send(pickle.dumps(info_dict))


def login_wind():
    login_window = Toplevel(root)
    login_window.title('Log In')

    # Set the width and height of the create account window
    width = 400
    height = 250

    # Calculate the x-coordinate and y-coordinate of the create account window
    x = root.winfo_x() + (root.winfo_width() - width) // 2
    y = root.winfo_y() + (root.winfo_height() - height) // 2

    # Set the geometry of the create account window
    login_window.geometry("%dx%d+%d+%d" % (width, height, x, y))

    text_label = Label(login_window, text="Insert your UserID and Password", font=("Arial", 18))
    text_label.pack(side=TOP, pady=40)

    userid = StringVar()
    pasw = StringVar()

    user_id = Label(login_window, text="Enter your UserID:", font=('Arial', 14))
    password = Label(login_window, text="Enter your password:", font=('Arial', 14))
    e_userid = Entry(login_window, textvariable=userid)
    e_password = Entry(login_window, textvariable=pasw, show='*')

    user_id.place(x=30, y=93)
    password.place(x=30, y=143)
    e_userid.place(x=230, y=100)
    e_password.place(x=230, y=150)
    login_b = Button(login_window, text="Log In", bg='light gray', relief=RAISED,
                     command=lambda: login_button(e_userid.get(), e_password.get(), login_window, root),
                     font=("Arial", 14))
    login_b.pack(side=BOTTOM, padx=10, pady=20)


def register(f_name, l_name, password, deposit, cr_acc_window):
    global datatype
    rand_num = random.randint(100, 1000)
    l_name = l_name.capitalize()
    f_name = f_name.capitalize()
    user_ID = f_name[0] + l_name[0] + str(rand_num)

    # Hide the cr_acc_window
    cr_acc_window.withdraw()

    # Create a new window
    confirm_window = Toplevel(root)
    confirm_window.title('Confirmation')

    # Set the width and height of the confirmation window
    width = 400
    height = 300

    # Calculate the x-coordinate and y-coordinate of the confirmation window
    x = root.winfo_x() + (root.winfo_width() - width) // 2
    y = root.winfo_y() + (root.winfo_height() - height) // 2

    # Set the geometry of the confirmation window
    confirm_window.geometry("%dx%d+%d+%d" % (width, height, x, y))

    # Create a Label widget to display the user ID
    id_label = Label(confirm_window, text="Your user ID is: " + user_ID, font=("Arial", 18))
    instr_label = Label(confirm_window, text="Please return to the main window and Log In.", font=("Arial", 14))
    id_label.pack(side=TOP, pady=20)
    instr_label.pack(side=TOP, pady=40)

    # Create a Button widget to close the confirmation window
    close_button = Button(confirm_window, text="Close", bg='light gray', relief=RAISED, command=confirm_window.destroy,
                          font=("Arial", 18), height=2)
    close_button.pack(side=BOTTOM, padx=10, pady=20)

    # Send the user information to the server
    values = f"'{user_ID}', '{f_name}', '{l_name}', '{password}', '{deposit}', '0'"

    send_info('user_information', values)


def cr_acc():
    cr_acc_window = Toplevel(root)
    cr_acc_window.title('Create Account')

    # Set the width and height of the create account window
    width = 400
    height = 500

    # Calculate the x-coordinate and y-coordinate of the create account window
    x = root.winfo_x() + (root.winfo_width() - width) // 2
    y = root.winfo_y() + (root.winfo_height() - height) // 2

    # Set the geometry of the create account window
    cr_acc_window.geometry("%dx%d+%d+%d" % (width, height, x, y))

    text_label = Label(cr_acc_window, text="Create your account", font=("Arial", 18))
    text_label.pack(side=TOP, pady=40)

    fname = StringVar()
    lname = StringVar()
    pasw = StringVar()
    cash = StringVar()

    f_name = Label(cr_acc_window, text="Enter your first name:", font=('Arial', 14))
    l_name = Label(cr_acc_window, text="Enter your last name:", font=('Arial', 14))
    password = Label(cr_acc_window, text="Enter your password:", font=('Arial', 14))
    deposit = Label(cr_acc_window, text="Your first deposit:", font=('Arial', 14))
    e_f_name = Entry(cr_acc_window, textvariable=fname)
    e_l_name = Entry(cr_acc_window, textvariable=lname)
    e_password = Entry(cr_acc_window, textvariable=pasw, show='*')
    e_deposit = Entry(cr_acc_window, textvariable=cash)

    f_name.place(x=30, y=93)
    l_name.place(x=30, y=143)
    password.place(x=30, y=193)
    deposit.place(x=30, y=243)
    e_f_name.place(x=230, y=100)
    e_l_name.place(x=230, y=150)
    e_password.place(x=230, y=200)
    e_deposit.place(x=230, y=250)
    register_button = Button(cr_acc_window, text="Register", bg='light gray', relief=RAISED,
                             command=lambda: register(e_f_name.get(), e_l_name.get(), e_password.get(), e_deposit.get(),
                                                      cr_acc_window), font=("Arial", 18), height=2)
    register_button.pack(side=BOTTOM, padx=10, pady=20)


# Establishing connection
# >>>
HOST = "127.0.0.1"
PORT = 4455
ADDRESS = (HOST, PORT)
BUFSIZE = 1024
socket = socket(AF_INET, SOCK_STREAM)
socket.connect(ADDRESS)
# >>>


root = Tk()
root.title('InveStar')

width = root.winfo_screenwidth()
height = root.winfo_screenheight()
root.geometry("%dx%d" % (width, height))

frame = Frame(root)
frame.place(relx=0.5, rely=0.5, anchor=CENTER)

login_button_main = Button(frame, text="Log In", bg='light gray', relief=RAISED, command=login_wind, font=("Arial", 18),
                           height=2)
signup_button = Button(frame, text="Create Account", bg='light gray', relief=RAISED, command=cr_acc, font=("Arial", 18),
                       height=2)
login_button_main.pack(side=BOTTOM, padx=10, pady=10)
signup_button.pack(side=BOTTOM, padx=10, pady=10)

# Create a Label widget to display text and an image
text_label = Label(frame, text="Welcome to InveStar!", font=("Arial", 36))
text_label.pack(side=TOP, pady=50)

image = Image.open('logo.pgm')
my_img = image.resize((450, 350))

img = ImageTk.PhotoImage(my_img)
img_label = Label(frame, image=img)
img_label.pack(side=TOP)

root.mainloop()

# Client code
# >>>


received = socket.recv(BUFSIZE).decode()


# >>>

# Closing connection
# >>>
socket.close()
# >>>
