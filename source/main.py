import sqlite3
from pathlib import Path
from tabulate import tabulate
# Static Queries
GET_ALL_WAREHOUSES = '''select * from warehouse'''
GET_ALL_PRODUCTS = '''select * from product'''
GET_ALL_PARTS = '''select * from part'''
GET_ALL_EMPLOYEES = '''select * from employee'''
GET_EMPLOYEES_WITH_GREATER_AVG_SALARY = '''select * from employee where salary > 
                                            (select avg(salary) from employee)'''

GET_EMPLOYEES_UNDER_100000_SAL_WITH_WAREHOUSE = """select e.employee_id, e.name as employee_name, 
                                                    w.name as warehouse_name, w.state, w.city 
                                                    from employee as e
                                                    inner join warehouse as w
                                                    on e.warehouse_id = w.warehouse_id
                                                    where e.salary < 100000;"""

GET_PRODUCTS_FROM_WAREHOUSE_WITH_MORE_THAN_ONE_PRODUCT = """select p.name as product_name, p.quantity, p.cost, w.name as warehouse_name, w.state, w.city
                                                            from product as p
                                                            inner join warehouse as w
                                                            on p.warehouse_id = w.warehouse_id
                                                            where p.warehouse_id in (select warehouse_id
                                                                                    from product
                                                                                    group by warehouse_id
                                                                                    having count(warehouse_id)>1)
                                                            order by w.name;"""

db_dir = str(Path(__file__).resolve().parent.parent) + '/inventory.db'
# TODO: Query that shows products that are being handled by a particular employee
# TODO: Code cleanup, make print table more readable
# TODO: Add product insertion and more queries
# TODO: Warehouses with more than one product, and the products in those warehouses

# Create connection to db
connection = sqlite3.connect(db_dir)
cur = connection.cursor()
# Turn on foreign key constraint
connection.execute("PRAGMA foreign_keys = ON;")

# Helper
def print_table(data, attr_names):
    print(tabulate(data, headers=attr_names, tablefmt="fancy_grid"))


def get_attr_names(cursor):
    return [description[0] for description in cursor.description]

# Interface
def interface():
    
    while True:

        print("Welcome to the inventory system.")
        print("1. Add a product")
        print("2. Product view/deletion")
        print("3. Employee view")
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
            
            warehouse = int(input("Warehouse id: "))

            # Printing out parts because each product must have parts, 
            # this relationship will be inserted into product/part rel table
            print("Below is a list of parts, select parts by id associated with the product:")
            res = cur.execute(GET_ALL_PARTS)
            print_table(res.fetchall(), get_attr_names(cur))

            parts = input("Enter part ids separated by commas: ")
            parts = [int(x.strip()) for x in parts.split(',')]
            # Make sure product is being added with parts
            
            if not parts:
                print("You must select at least one part.")
                continue
            # Insert into product table and parts_in_product rel table
            try:
                cur.execute(f'insert into product (name, quantity, cost, warehouse_id) values ("{name}", {quantity}, {cost}, {warehouse})')
                last_product_id = cur.lastrowid
                for part_id in parts:
                    cur.execute(f'insert into parts_in_product (product_id, part_id) values ({last_product_id}, {part_id})')
                connection.commit()
            except:
                print("Error inserting product, please check your inputs.")
                continue

        elif command.lower() == '2':
            # View all products in the inventory, 
            # this will next prompt user to view parts or warehouse of chosen product
            res = cur.execute(GET_ALL_PRODUCTS)
            print_table(res.fetchall(), get_attr_names(cur))

            chosen_product = int(input("Select a product by id to view details or delete: "))
            print("1. View parts associated with this product")
            print("2. View warehouse associated with this product")
            print("3. Delete this product from the database")
            choice = input("Enter your choice (1-3): ")
            # Selecting parts
            if choice == '1':
                res = cur.execute(f"select * from part where part_id in (select part_id from parts_in_product where product_id = {chosen_product})")
                print_table(res.fetchall(), get_attr_names(cur))

            # Selecting warehouse details
            elif choice == '2':
                res = cur.execute(f"select * from warehouse where warehouse_id in (select warehouse_id from product where product_id = {chosen_product})")
                print_table(res.fetchall(), get_attr_names(cur))

            elif choice == '3':
                print(chosen_product)
                # Delete product from parts_in_product rel table
                try:
                    cur.execute(f"delete from parts_in_product where product_id = {chosen_product};")
                    connection.commit()
                except:
                    print("Error deleting product from parts_in_product table")
                    continue
                # Delete product from database
                try:
                    cur.execute(f"delete from product where product_id = {chosen_product};")
                    connection.commit()
                    print("Product deleted successfully.")
                except:
                    print("Error deleting product")
                    continue
                

        elif command.lower() == '3':
            # View employee information
            # you can then select an employee to view
            res = cur.execute(GET_ALL_EMPLOYEES)
            print_table(res.fetchall(), get_attr_names(cur))
            print("Select an employee by id to view their warehouse details:")
            chosen_employee = int(input("Enter employee id: "))
            # View details for the selected employee
            res = cur.execute(f"select * from warehouse where warehouse_id in (select warehouse_id from employee where employee_id = {chosen_employee})")
            print_table(res.fetchall(), get_attr_names(cur))

        elif command.lower() == '4':
            # Special Queries
            print("Special Queries:")
            print("1. View employees with salary greater than average")
            print("2. View employees with salary under 100000 and their warehouse details")
            print("3. View products from warehouse with more than one product")
            special_query = input("Enter your choice (1-3): ")

            if special_query == '1':
                res = cur.execute(GET_EMPLOYEES_WITH_GREATER_AVG_SALARY)
                print_table(res.fetchall(), get_attr_names(cur))
            elif special_query == '2':
                res = cur.execute(GET_EMPLOYEES_UNDER_100000_SAL_WITH_WAREHOUSE)
                print_table(res.fetchall(), get_attr_names(cur))
            elif special_query == '3':
                res = cur.execute(GET_PRODUCTS_FROM_WAREHOUSE_WITH_MORE_THAN_ONE_PRODUCT)
                print_table(res.fetchall(), get_attr_names(cur))
            

        elif command.lower() == '5':
            print("Exiting the inventory system.")
            break

interface()