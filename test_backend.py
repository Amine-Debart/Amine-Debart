import sys
import os
import pytest
root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, root)
from database import database


# Define a fixture to create a database connection and initialize tables
@pytest.fixture
def db():
    # Create a new database instance
    db = database()
    # Create necessary tables
    db.create_tables()
    # Provides the database instance for testing
    yield db
    # Close the database connection after the test
    db.close_db()


# Test case for create_tables method
def test_create_tables(db):
    # Check if the tables have been created by trying to select data from them
    cursor = db.connection.cursor()
    cursor.execute("SELECT * FROM stockItems")
    assert cursor.fetchall() is not None
    cursor.execute("SELECT * FROM sales")
    assert cursor.fetchall() is not None


# Test case for create_update_stock method
def test_create_update_stock(db):
    # Insert a new stock item
    db.create_update_stock(["Hoodie", "One Direction", 20, 5.0])
    # Retrieve the inserted item
    cursor = db.connection.cursor()
    cursor.execute("SELECT * FROM stockItems WHERE name=?", ("Hoodie", ))
    result = cursor.fetchone()
    assert result is not None
    assert result[:-1] == ("Hoodie", "One Direction", 20, 5.0)


# Test case for update_stock_quantity method
def test_update_stock_quantity(db):
    # Update the quantity of an existing stock item
    db.update_stock_quantity("Hoodie", 5)
    # Retrieve the updated quantity
    cursor = db.connection.cursor()
    query = "SELECT quantity FROM stockItems WHERE name=?"
    cursor.execute(query, ("Hoodie", ))
    result = cursor.fetchone()
    db.update_stock_quantity("Hoodie", -5)
    cursor = db.connection.cursor()
    cursor.execute(query, ("Hoodie", ))
    result1 = cursor.fetchone()
    assert result is not None
    assert result[0] == 15
    assert result1[0] == 20


# Test case for create_sale method
def test_create_sale(db):
    # Insert a new sale record
    db.create_sale(["Hoodie", 5])
    # Retrieve the inserted sale record
    cursor = db.connection.cursor()
    cursor.execute("SELECT * FROM sales WHERE stockItemID=?", ("Hoodie", ))
    result = cursor.fetchone()
    assert result is not None
    assert (result[1], result[-1]) == ("Hoodie", 5)


# Test case for delete_sale method
def test_delete_sale(db):
    # Delete an existing sale item
    db.delete_sale(1)
    # Try to retrieve the deleted item
    cursor = db.connection.cursor()
    cursor.execute("SELECT * FROM sales WHERE id=?", (1, ))
    result = cursor.fetchone()
    assert result is None


# Test case for delete_stock method
def test_delete_stock(db):
    # Delete an existing stock item
    db.delete_stock("Hoodie")
    # Try to retrieve the deleted item
    cursor = db.connection.cursor()
    cursor.execute("SELECT * FROM stockItems WHERE name=?", ("Hoodie", ))
    result = cursor.fetchone()
    assert result is None


# Test case for retrieve_inventory method
def test_retrieve_inventory(db):
    # Ensure the inventory is retrieved correctly
    inventory = db.retrieve_inventory()
    assert isinstance(inventory, list)


# Test case for retrieve_quantity method
def test_retrieve_quantity(db):
    # Insert a new stock item
    db.create_update_stock(["Hoodie", "One Direction", 20, 10.0])
    # Retrieve the quantity of the inserted item
    quantity = db.retrieve_quantity("Hoodie")
    assert quantity[0] == 20


# Test case for retrieve_sales method
def test_retrieve_sales(db):
    # Ensure sales records are retrieved correctly
    sales = db.retrieve_sales()
    assert isinstance(sales, list)


# Test case for retrieve_total_payments method
def test_retrieve_total_payments(db):
    # Ensure total payments are calculated correctly
    gross, net, band = db.retrieve_total_payments()
    assert gross == 4/3 * net
    assert net == 3/4 * gross
    assert band is not None
