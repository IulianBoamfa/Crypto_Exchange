# Crypto Exchange

## Project Overview
Crypto Exchange is a sophisticated graphical user interface (GUI) project that emulates a real Crypto Exchange. It offers users a seamless experience of trading cryptocurrencies, gold, and silver in real-time. All data is efficiently managed, and prices are scraped from reputable sources, ensuring that users have access to up-to-date market information. The project's logic and architecture are meticulously represented in a UML diagram for clarity.

## Key Features

### Client-Side Functionalities
- **Open an Account**
  - Users can create an account with a simple username and password.
  - User account details are securely stored in a MySQL database.
  - Users can specify their initial investment amount, enhancing the trading experience.
  - User can perform Deposit/Withdrawal actions.  
  - Each user is assigned a unique client ID for identification.

- **Investment Options**
  - Users can explore a wide variety of investment options, including cryptocurrencies, gold, and silver, along with their current prices.
  - Investments can be based on the available funds or the desired quantity of the asset.
  - Buy or sell transactions can be executed.
  - The system ensures that there are sufficient funds for buying transactions and available assets for selling transactions.
  - Transactions can be canceled, edited, or confirmed with details such as asset name, date, buy/sell option, quantity, and cost.

- **Portfolio Viewing**
  - Users have access to a comprehensive portfolio that displays all their transactions.
  - Each transaction includes information about the asset name, purchase date, buy/sell option, quantity, and cost.

### Server-Side Functionalities
- **User Account Management**
  - User account information is updated upon account creation.
  - Secure storage of user account details in the MySQL database.

- **Portfolio Management**
  - User portfolio information is updated after each transaction.
  - All trades are retrieved and displayed in the 'Portfolio Viewing' option, providing users with a complete view of their investments.

- **Real-Time Data**
  - The system continuously scrapes real-time prices from reputable sources:
    - Cryptocurrencies: [coinranking.com](https://coinranking.com/)
    - Gold: [finance.yahoo.com](https://finance.yahoo.com/quote/GC%3DF?p=GC%3DF)
    - Silver: [finance.yahoo.com](https://finance.yahoo.com/quote/SI%3DF?p=SI%3DF)

## Technology Stack
- **GUI Design:** The project features a user-friendly GUI for intuitive navigation.
- **MySQL Database:** Securely stores user account and portfolio data.
- **Python:** Powers the core functionality of the project, including real-time data scraping and database integration.

## System Architecture
The project's logical architecture is elegantly represented in the UML diagram provided, offering a comprehensive view of the system's design and functionality.

## Getting Started
To get started with Crypto Exchange, ensure you have Python and MySQL set up on your system. Refer to the project's documentation for detailed installation and configuration instructions.
