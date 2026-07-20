import sqlite3
# Queries
GET_ALL_WAREHOUSES = '''select * from warehouse'''
GET_ALL_PRODUCTS = '''select * from product'''
GET_ALL_PARTS = '''select * from part'''
GET_ALL_EMPLOYEES = '''select * from employee'''


# Create connection to db
connection = sqlite3.connect('inventory.db')
cur = connection.cursor()


# Helper
def print_table(data, attr_names):
    if not data:
        print("Empty table - error.")
    # Headers
    for attr in attr_names:
        print(attr, end='    ')

    print('\n')
    # Columns
    for row in data:
        for value in row:
            print(value, end='  |  ')
        print('\n')

def get_attr_names(cursor):
    return [description[0] for description in cursor.description]

# Interface
def interface():
    print("Welcome to the inventory system.")
    print("1. Add a product")
    print("2. View all products")
    print("3. View Employees")
    print("4. Quit")

    while True:
        command = input("Enter your choice (1-4): ")
        
        if command.lower() == '1':
            # Add item to the inventory with insert into cmd,
            # item must have name, cost, quantity, warehouse, and parts
            print("Please enter the product details:")
            # Get attrs for product
            name = input("Name: ")
            cost = float(input("Cost: "))
            quantity = int(input("Quantity: "))
            print("Select a warehouse from the list below:")

            # Printing out warehouses to get foreign key for product
            res = cur.execute(GET_ALL_WAREHOUSES)
            print_table(res.fetchall(), get_attr_names(cur))
            
            warehouse = input("Warehouse id: ")

            # Printing out parts because each product must have parts, 
            # this relationship will be inserted into product/part rel table
            print("Below is a list of parts, select parts by id associated with the product:")
            res = cur.execute(GET_ALL_PARTS)
            print_table(res.fetchall(), get_attr_names(cur))

            pass

        elif command.lower() == '2':
            # View all products in the inventory, 
            # this will next prompt user to view parts or warehouse of chosen product
            pass

        elif command.lower() == '3':
            # View employee information
            # you can then select an employee to view
            pass

        elif command.lower() == '4':
            print("Exiting the inventory system.")
            break

interface()