import sqlite3
# Queries
GET_ALL_WAREHOUSES = '''select * from warehouse'''
GET_ALL_PRODUCTS = '''select * from product'''
GET_ALL_PARTS = '''select * from part'''
GET_ALL_EMPLOYEES = '''select * from employee'''
GET_EMPLOYEES_WITH_GREATER_AVG_SALARY = '''select * from employee where salary > 
                                            (select avg(salary) from employee)'''

# TODO: Query that shows products that are being handled by a particular employee
# TODO: Code cleanup, make print table more readable
# TODO: Add product insertion and more queries

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
    
    while True:

        print("Welcome to the inventory system.")
        print("1. Add a product")
        print("2. View all products")
        print("3. View Employees")
        print("4. Special Queries")
        print("5. Quit\n")
        command = input("Enter your choice (1-5): ")
        
        if command.lower() == '1':
            # Add item to the inventory with insert into cmd,
            # item must have name, cost, quantity, warehouse, and parts
            print("Please enter the product details:")
            # Get attrs for product
            name = input("Name: ")

            try:
                cost = float(input("Cost: "))
            except ValueError:
                print("Invalid value, must be a decimal number.")
                continue
                
            try:
                quantity = int(input("Quantity: ")) 
            except ValueError:
                print("Invalid value, must be an integer.")
                continue
                
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
            res = cur.execute(GET_ALL_PRODUCTS)
            print_table(res.fetchall(), get_attr_names(cur))

            chosen_product = input("Select a product by id to view its details: ")
            print("1. View parts associated with this product")
            print("2. View warehouse associated with this product")
            choice = input("Enter your choice (1-2): ")
            # Selecting parts
            if choice == '1':
                res = cur.execute(f"select * from part where part_id in (select part_id from parts_in_product where product_id = {chosen_product})")
                print_table(res.fetchall(), get_attr_names(cur))

            # Selecting warehouse details
            elif choice == '2':
                res = cur.execute(f"select * from warehouse where warehouse_id in (select warehouse_id from product where product_id = {chosen_product})")
                print_table(res.fetchall(), get_attr_names(cur))


        elif command.lower() == '3':
            # View employee information
            # you can then select an employee to view
            res = cur.execute(GET_ALL_EMPLOYEES)
            print_table(res.fetchall(), get_attr_names(cur))

            pass

        elif command.lower() == '4':
            # Special Queries
            print("Special Queries:")
            print("1. View employees with salary greater than average")

            special_query = input("Enter your choice (1-3): ")

            if special_query == '1':
                res = cur.execute(GET_EMPLOYEES_WITH_GREATER_AVG_SALARY)
                print_table(res.fetchall(), get_attr_names(cur))
            
            

        elif command.lower() == '5':
            print("Exiting the inventory system.")
            break

interface()