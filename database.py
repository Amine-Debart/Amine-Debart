import sqlite3
from typing import List



class database:
    """
    This class manages the database, and controls the SQL requests that executed.
    
    Attributes:
        connection: stores the connection request to the database using sqlite3

    Methods:
        __init__: Initializes the database class
        create_tables: Creates both the stockItems and sales tables if they do not already exist
        create_update_stock: Uses the values passed in to create a new product record, or update an existing record
        update_stock_quantity: Updates the products quantity by either adding or subtracting a sales records quantity
        delete_stock: deletes specified product from stockItems table
        create_sale: Uses the values passed in to create a new sales record
        delete_sale: deletes specified sale from stockItems table
        retrieve_inventory: retrieves all records in the stockItems table
        retrieve_quantity: retrieves the quantity for a specific product
        retrieve_sales: retrieves all records in the sales table
        retrieve_total_payments: calculates both the net and gross totals owed to the current days band
    """

    def __init__(self) -> None:
        """Initializes the database class"""
        self.connection = sqlite3.connect("StockSales.db")

    
    def create_tables(self) -> None:
        """Executes SQL command to create both stockItems table and sales table, if they do not exist"""
        cursor = self.connection.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS stockItems (
                       name TEXT PRIMARY KEY,
                       band TEXT,
                       quantity INTEGER,
                       price REAL,
                       timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP)""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS sales (
                       id INTEGER PRIMARY KEY,
                       stockItemID TEXT,
                       quantity INTEGER,
                       timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                       price REAL,
                       FOREIGN KEY (stockItemID) REFERENCES StockItems(name))""")

    
    def create_update_stock(self, values: List) -> None:

        cursor = self.connection.cursor()
        cursor.execute("""INSERT OR REPLACE INTO stockItems (name, band, quantity, price) VALUES (?,?,?,?)""", (values[0], values[1], values[2], values[3]))
        self.connection.commit()

    
    def update_stock_quantity(self, name: str, quantity: int) -> None:

        cursor = self.connection.cursor()
        oldquantity: int = cursor.execute("""SELECT quantity FROM stockItems WHERE name=?""", (name, )).fetchone()
        newquantity: int = oldquantity[0] - quantity
        cursor.execute("""UPDATE stockItems SET quantity=? WHERE name=?""", (newquantity, name, ))
        self.connection.commit()

    
    def delete_stock(self, name: str) -> None:

        cursor = self.connection.cursor()
        cursor.execute("""DELETE FROM stockItems WHERE name=?""", (name, ))
        self.connection.commit()

    
    def create_sale(self, values: List) -> None:

        cursor = self.connection.cursor()
        price: float = cursor.execute("""SELECT price FROM stockItems WHERE name=?""", (values[0], )).fetchone()[0]
        cursor.execute("""INSERT INTO sales (stockItemID, quantity, price) VALUES (?,?,?)""", (values[0], values[1], price))
        self.connection.commit()

    
    def delete_sale(self, id: int) -> None:

        cursor = self.connection.cursor()
        cursor.execute("""DELETE FROM sales WHERE id=?""", (id, ))
        self.connection.commit()

    
    def retrieve_inventory(self) -> List:

        cursor = self.connection.cursor()
        inventory: List = cursor.execute("""SELECT name, band, quantity, price, timestamp FROM stockItems WHERE quantity > 0 AND DATE(timestamp)=DATE('now') ORDER BY name""").fetchall()
        return inventory

    def retrieve_quantity(self, name: str) -> int:

        cursor = self.connection.cursor()
        quantity: int = cursor.execute("""SELECT quantity FROM stockItems WHERE name=?""", (name, )).fetchone()
        return quantity

    
    def retrieve_sales(self) -> List:

        cursor = self.connection.cursor()
        sales: List = cursor.execute("""SELECT sales.id, stockItems.name, stockItems.band, sales.quantity, sales.timestamp, sales.price FROM sales JOIN stockItems ON sales.stockItemID = stockItems.name WHERE DATE(sales.timestamp)=DATE('now')""").fetchall()
        return sales

    
    def retrieve_total_payments(self) -> List:
        
        sales: List = self.retrieve_sales()
        gross: float = 0
        net: float = 0
        for sale in sales:
            quantity: int = sale[3]
            price: float = sale[5]
            gross += price*quantity
            net = gross * 0.75
        try:
            band: str = sales[0][2]
        except:
            band: str = None  
        return gross, net, band

    
    def close_db(self) -> None:
        self.connection.close()
        print("Database Closed")
