import tkinter as tk
from tkinter import *
from database import database


class ShopManager(tk.Tk):
    """
    This class manages the frames and navigation of the Shop Manager application.
    
    Attributes:
            frames (dict): A dictionary to store instances of different frames.
                Key: Class representing a frame.
                Value: Instance of the frame.

    Methods:
        __init__: Initializes the ShopManager class.
        show_frame: Displays a specified frame.
    """

    def __init__(self, *args, **kwargs):
        """Inializes the ShopManager class"""
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Shop Manager")
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for page in (homePage, manageStock, manageSales, calculateTotal):
            frame = page(container, self)
            self.frames[page]=frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(homePage)
    
    def show_frame(self, page):
        """Displays the selected frame"""
        frame = self.frames[page]
        frame.tkraise()


class homePage(tk.Frame):
    """
     This class manages the applications menu, and displays all available pages.

     Attributes:
        manageStockPage (tk.Button): Displays the ManageStock frame
        manageSalesPage (tk.Button): Displays the ManageSales frame
        calculateTotalPage (tk.Button): Displays the calculateTotal frame

    Methods:
        __init__: Initializes the HomePage class
    """
    def __init__(self, parent, controller):
        """Initializes the homePage class"""
        tk.Frame.__init__(self, parent, width=500, height=500) 
        self.pack_propagate(False)
        manageStockPage = tk.Button(self, text="Manage Inventory", command=lambda: controller.show_frame(manageStock))
        manageSalesPage = tk.Button(self, text="Manage Sales", command=lambda: controller.show_frame(manageSales))
        calculateTotalPage = tk.Button(self, text="Calculate Totals", command=lambda: controller.show_frame(calculateTotal))
        manageStockPage.pack(fill="both", expand=True)  
        manageSalesPage.pack(fill="both", expand=True)
        calculateTotalPage.pack(fill="both", expand=True)


class manageStock(tk.Frame):
    """
     This class manages the shops inventory, and displays a row for each product.

     Attributes:
        controller: Handles requests and manages which frame should be displayed
        db: Creates an instance of the database class
        
    Methods:
        __init__: Initializes the HomePage class
        stockManager: Displays all records in the stockItems table, with options to update or delete row
        addStockPage: Page which allows user to add a products and its details
        updateStockPage: Page which allows user to update the quantity or price of a product
        addUpdateStock: This is used to send a request to the backend to create or update an existing products details
        deleteStock: Sends a request to the backend to delete a product from the stockItems table
    """

    def __init__(self, parent, controller):
        """Initializes the Homepage class"""
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.db = database()
        self.db.create_tables()
        self.stockManager()

    
    def stockManager(self):
        """
        Displays all the records in the database. 
        
        Add, update and delete buttons are available to manipulate the data
        """
        for widget in self.winfo_children():
            widget.destroy()
        stockitems = self.db.retrieve_inventory()
        title = tk.Label(self,text="Stock Items")
        home = tk.Button(self,text="Home", command=lambda: self.controller.show_frame(homePage))
        add = tk.Button(self,text="Add Item",command=lambda: self.addStockPage())
        title.grid(row=0, column=0, pady=5,columnspan=5,sticky="EW")
        home.grid(row=1, column=1, sticky="EW")
        add.grid(row=1, column=2, sticky="EW")
        row_position = 2
        for item in stockitems:
            name = tk.Label(self, text=item[0])
            band = tk.Label(self, text=item[1])
            quantity = tk.Label(self, text=item[2])
            price = tk.Label(self, text=item[3])
            name.grid(row=row_position, column=0, pady=5, sticky="NSEW")
            band.grid(row=row_position, column=1, pady=5, sticky="NSEW")
            quantity.grid(row=row_position, column=2, pady=5, sticky="NSEW")
            price.grid(row=row_position, column=3, pady=5, sticky="NSEW")
            edit = tk.Button(self, text="Update", command= lambda item=item:  self.updateStockPage(item))
            delete = tk.Button(self, text="delete", command= lambda name=item[0]:  self.deleteStock(name))
            edit.grid(row=row_position, column=4, pady=5, sticky="NSEW")
            delete.grid(row=row_position, column=5, pady=5, sticky="NSEW")
            row_position += 1
        for i in range(6):
            self.grid_columnconfigure(i, weight=1)
        
    
    def addStockPage(self):
        """
        Page displayed when add button clicked. 
        User can input name, brand, price and quantity data when creating a product.
        """
        for widget in self.winfo_children():
            widget.destroy()
        title = tk.Label(self, text="Add Stock")
        nameLabel = tk.Label(self, text="Name")
        bandLabel = tk.Label(self, text="Touring Band")
        quantityLabel = tk.Label(self, text="Quantity")
        priceLabel = tk.Label(self, text="Price")
        name_var = tk.StringVar()
        band_var = tk.StringVar()
        quantity_var = tk.IntVar()
        price_var = tk.DoubleVar()
        name = tk.Entry(self, textvariable=name_var)
        band = tk.Entry(self, textvariable=band_var)
        quantity = tk.Entry(self, textvariable=quantity_var)
        price = tk.Entry(self, textvariable=price_var)
        title.grid(row=0, column=0, pady=5, columnspan=5, sticky="NSEW")
        nameLabel.grid(row=2, column=2, pady=5, sticky="NSEW")
        bandLabel.grid(row=4, column=2, pady=5, sticky="NSEW")
        quantityLabel.grid(row=6, column=2, pady=5, sticky="NSEW")
        priceLabel.grid(row=8, column=2, pady=5, sticky="NSEW")
        name.grid(row=3, column=2, pady=5, sticky="NSEW")
        band.grid(row=5, column=2, pady=5, sticky="NSEW")
        quantity.grid(row=7, column=2, pady=5, sticky="NSEW")
        price.grid(row=9, column=2, pady=5, sticky="NSEW")
        back = tk.Button(self,text="Back", command=lambda: self.stockManager())
        add = tk.Button(self,text="Add",command=lambda: self.addUpdateStock(name_var.get(), band_var.get(),  quantity_var.get(), price_var.get()))
        add.config(state="disabled")
        back.grid(row=11, column=2, sticky="NSEW")
        add.grid(row=10, column=2, sticky="NSEW")


        def validate_entries(*args):
            """
            The input values are checked to ensure they are the right data type. 
            Once they are valid, the add button is enabled
            """
            try:
                if quantity_var.get() > 0 and name_var.get() is not None and band_var.get() is not None and price_var.get() > 0:
                    add.config(state="normal")
                else:
                    add.config(state="disabled")
            except:
                add.config(state="disabled")     
        name_var.trace_add("write", validate_entries)
        band_var.trace_add("write", validate_entries)
        quantity_var.trace_add("write", validate_entries)
        price_var.trace_add("write", validate_entries)


    def updateStockPage(self,item):
        """
        Displays page where user can update a specific products price or quantity
        """
        for widget in self.winfo_children():
            widget.destroy()
        title = tk.Label(self, text="Update Stock")
        nameLabel = tk.Label(self, text=item[0])
        bandLabel = tk.Label(self, text=item[1])
        quantity_var = tk.IntVar()
        price_var = tk.DoubleVar()
        quantity_var.set(item[2])
        price_var.set(item[3])
        quantity = tk.Entry(self, textvariable=quantity_var)
        price = tk.Entry(self, textvariable=price_var)
        title.grid(row=0,column=0, pady=5, columnspan=5, sticky="NSEW")
        nameLabel.grid(row=3, column=0, pady=5, sticky="NSEW")
        bandLabel.grid(row=3, column=2, pady=5, sticky="NSEW")
        quantity.grid(row=3, column=4, pady=5, sticky="NSEW")
        price.grid(row=3, column=6, pady=5, sticky="NSEW")
        back = tk.Button(self, text="Back", command=lambda: self.stockManager())
        update = tk.Button(self, text="Update", command=lambda: self.addUpdateStock(item[0], item[1], quantity_var.get(), price_var.get()))
        update.config(state="disabled")


        def validate_entries(*args):
            """
            The input values are checked to ensure they are the right data type. 
            Once they are valid, the add button is enabled
            """
            try:
                if quantity_var.get() > 0 and price_var.get() > 0:
                    update.config(state="normal")
                else:
                    update.config(state="disabled")
            except:
                update.config(state="disabled")

        quantity_var.trace_add("write", validate_entries)
        price_var.trace_add("write", validate_entries)
        back.grid(row=5, column=1, sticky="NSEW")
        update.grid(row=5, column=2, sticky="NSEW")
        
    
    def addUpdateStock(self, name, band, quantity, price):
        """A request is sent to the backend to create or update a product details using user entries"""
        self.db.create_update_stock([name, band, quantity, price])
        self.stockManager()
    

    def deleteStock(self, name):
        """A request is sent to the backend to delete a products record from the database """
        self.db.delete_stock(name)
        self.stockManager()


class manageSales(tk.Frame):
    """
    This class manages the shops sales, and displays a row for each sale.

    Attributes:
        controller: Handles requests and manages which frame should be displayed
        db: Creates an instance of the database class
        
    Methods:
        __init__: Initializes the HomePage class
        salesManager: Displays all records in the sales table, with the option to delete a sale
        addSalePage: This page lets the user register a sale
        createSale: This sends a request to the backend to add the sales record to the sales table
        deleteSale: This sends a request to the backend to delete a specific sales record
    """


    def __init__(self, parent, controller):
        """Initializes the manageSales page"""
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.db = database()
        self.salesManager()


    def salesManager(self):
        """
        Displays all the sales records in the database

        An add button is available to allow user to register a sale

        A delete button is also provided next to each row to allow user to remove a sales record
        """
        for widget in self.winfo_children():
            widget.destroy()
        sales = self.db.retrieve_sales()
        title = tk.Label(self, text="Sales")
        home = tk.Button(self, text="Home", command=lambda: self.controller.show_frame(homePage))
        add = tk.Button(self, text="Add Sale", command=lambda: self.addSalePage())
        title.grid(row=0, column=0, pady=5, columnspan=5, sticky="EW")
        home.grid(row=1, column=1, sticky="EW")
        add.grid(row=1, column=2, sticky="EW")
        row_position = 2
        for sale in sales:
            id = tk.Label(self, text=sale[0]) 
            name = tk.Label(self, text=sale[1])
            quantity = tk.Label(self, text=sale[2])
            timestamp = tk.Label(self, text=sale[3])
            id.grid(row=row_position, column=0, pady=5, sticky="NSEW")
            name.grid(row=row_position, column=1, pady=5, sticky="NSEW")
            quantity.grid(row=row_position, column=2, pady=5, sticky="NSEW")
            timestamp.grid(row=row_position, column=3, pady=5, sticky="NSEW")
            delete = tk.Button(self, text="Delete", command= lambda sale=sale: self.deleteSale(sale))
            delete.grid(row=row_position, column=4, pady=5, sticky="NSEW")
            row_position += 1
        for i in range(5):
            self.grid_columnconfigure(i, weight=1)

    
    def addSalePage(self):
        """
        This page is displayed when user clicks the add button on the salesManager page

        The method checks if there are any existing products in the database.

        If there is, entry fields are displayed for user to input the sale's details.

        The add button is disabled until the entries are validated
        """
        for widget in self.winfo_children():
            widget.destroy()
        dropdown_options = []
        items = self.db.retrieve_inventory()
        title = tk.Label(self, text="Add Sale")
        title.grid(row=0, column=0, pady=5, columnspan=5, sticky="NSEW")
        back = tk.Button(self, text="Back", command=lambda: self.salesManager())
        back.grid(row=9, column=2, sticky="NSEW")
        
        if len(items) > 0:
            for item in items:
                dropdown_options.append(item[0])
            nameLabel = tk.Label(self, text="Name")
            quantityLabel = tk.Label(self, text="Select product to view quantity ")
            quantityLabel.grid(row=4, column=2, pady=5,sticky="NSEW")
            name_var = tk.StringVar()
            quantity_var = tk.IntVar()
            name_var.set(dropdown_options[0])
            name = tk.OptionMenu(self, name_var, *dropdown_options)
            quantity = tk.Entry(self, textvariable=quantity_var)  
            add = tk.Button(self, text="Add", command=lambda: self.createSale(name_var.get(), quantity_var.get(), ))
            add.config(state="disabled")
            
            def update_quantity_label(*args):
                """This detects a change in product selected and updates the quantity displayed"""
                available = self.db.retrieve_quantity(name_var.get())
                quantityLabel.config(text=f"Quantity Available: {available[0]}")
            
            def validate_quantity(*args):
                """
                This is used to validate the users entries to ensure the datatypes are correct

                The quantity is also checked to verify it is less than the available stock

                Once the entries have been validated, the add button is reenabled
                """
                available_quantity = self.db.retrieve_quantity(name_var.get())
                try:
                    if quantity_var.get() > 0 and quantity_var.get() <= available_quantity[0]:
                        add.config(state="normal")
                    else:
                        add.config(state="disabled")
                except:
                    add.config(state="disabled")  


            name_var.trace_add("write", update_quantity_label)
            quantity_var.trace_add("write", validate_quantity)
            nameLabel.grid(row=2, column=2, pady=5, sticky="NSEW")
            name.grid(row=3, column=2, pady=5, sticky="NSEW")
            quantity.grid(row=5, column=2, pady=5, sticky="NSEW")
            add.grid(row=8, column=2, sticky="NSEW")
        else:
            warning_text = tk.Label(self, text="Error: Please Create Products")
            warning_text.grid(row=2, olumn=2, pady=5, sticky="NSEW")

    
    def createSale(self, name, quantity):
        """
        A request is sent to the backend to update the sales records

        Another request is sent to the database to reflect the changes the sale has made to existing quantities and values.

        The manageStock frame is refreshed to show the new data

        User is rerouted back to the Stock Manager page

            Parameters:
                name (str): a string representing products name
                quantity (int): an integer representing quantity of a product
        """
        self.db.create_sale([name, quantity])
        self.db.update_stock_quantity(name, quantity)
        self.controller.frames[manageStock].stockManager()
        self.controller.frames[calculateTotal].calculator()
        self.salesManager()

    
    def deleteSale(self, sale):
        """
        A request is sent to the backend to remove sales record

        Another request is sent to the database to reverse the changes the sale has made to existing quantities and values.

        the manageStock frame is refreshed to display updated data

        User is rerouted back to the sales Manager page

            Parameters:
            sale (list): A list containing all the details of the sale
        """
        self.db.delete_sale(sale[0])
        self.db.update_stock_quantity(sale[1], -sale[3])
        self.controller.frames[manageStock].stockManager()
        self.controller.frames[calculateTotal].calculator()
        self.salesManager() 



class calculateTotal(tk.Frame):
    """
    This class displays the gross and net revenue that is owed to the touring band

    Attributes:
        controller: Handles requests and manages which frame should be displayed
        db: Creates an instance of the database class

    Methods:
        __init__: Initializes the calculateTotal class
        calculator: displays the gross and net revenues
    
    """
    def __init__(self, parent, controller):
        """
        Initializes the calculateTotal class
        
        Args:
            parent: The parent widget
            controller: Instance of the controller managing frame navigation
        """
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.db = database()
        self.calculator()
    

    def calculator(self):
        """"
        Displays the current days touring bands gross and net revenues 

        Begins by refreshing the pages data by destroying all widgets

        A request is made to the backend to calculate totals

        The returned data is then formatted and displayed on this frame

        User has option to return to homepage by selecting home button
        """
        for widget in self.winfo_children():
            widget.destroy()
        total, net, band = self.db.retrieve_total_payments()
        title = tk.Label(self, text=f"Payment Owed To: {band}")
        home = tk.Button(self, text="Home", command=lambda: self.controller.show_frame(homePage))
        title.grid(row=0, column=0, pady=5, columnspan=5, sticky="EW")
        home.grid(row=7, column=1, sticky="EW")
        total = tk.Label(self, text=f"Total: £{total}")
        total.grid(row=5, column=0, pady=5, sticky="NSEW")
        net = tk.Label(self, text=f"Net: £{net}")
        net.grid(row=5, column=2, pady=5, sticky="NSEW")
        for i in range(3):
            self.grid_columnconfigure(i, weight=1)



app = ShopManager()
app.mainloop()
