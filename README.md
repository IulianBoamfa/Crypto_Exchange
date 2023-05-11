# Crypto_Exchange
This is a project designed using GUI, illustrating a Crypto Exchange.

All the data is stored into the MySQL database directly from Python, the prices are scarpped in real time from the websites specified under this line
and updated every 10 seconds so the GUI will display the real prices and the real value of the portofolio in real time.
The project design is described in the UML Diagram file where I made a diagram illustrating the logic of this project using UML Diagram program.

Task description:
The “Investment Trading Platform” contains the following:

a) Open an account.
b) Invest
c) Portfolio Viewing
d) Deposit/Withdraw

Server:
a) user account information
b) user portfolio information
c) price information
(Web scaped current prices of:
Crypto: https://coinranking.com/,
gold: https://finance.yahoo.com/quote/GC%3DF?p=GC%3DF, and
silver: https://finance.yahoo.com/quote/SI%3DF?p=SI%3DF)

Description of each client functionalities:
a) The ‘Open account’ option should allow the user to:
Create simple log in system with username and password. All the details are stored into the MySQL database.
Add ‘cash to invest’ option where user can enter the initial value of money they will add into
the account.
Return client ID number (store the user account details)
Then welcome window/message specifying client ID, total investment value, total cash to
invest, total gain/loss and three options to choose from:
a. Investment now.
b. Portfolio Viewing
c. Pay in /withdraw.
b) The ‘Invest now’ option allow the user to:
- view list of Investment types (names and prices information)
- choose one, based on amount of money to invest or quantity of the specific investment.
a. Enter the value and calculate accordingly.
Choose between buy or sell.
b. When buying check for sufficient amount of money and if the total cash will allow
proceed in creating the buy transaction:
c. When selling the system should check the current investment for availability and if
allow proceed in creating the sell transaction
d. Both options will generate transaction:
i. The transaction should allow the user to cancel, edit or confirm and pay.
1. cancel – will ask for confirmation and return into the welcome window
2. confirm and pay – will display the:
   Name of the cryptocurrencies, Date, Buy/sell option, Quantity, Cost.

Transaction should be update in portfolio accordingly (store user portfolio information).
c) The ‘Portfolio Viewing’ option will display list of all transaction. Where each transaction will
contain:
a. Name of the cryptocurrencies,
b. Date of purchasing:
c. Buy/sell option:
d. Quantity:
e. Cost:

Description of server data storage:
a) user account information will be updated after user will be created.
b) user portfolio information will be update after each transaction as well as all trades will be
retrieved and display on ‘Portfolio Viewing’ option.
c) price information will be retrieving each time user open invest now option.
