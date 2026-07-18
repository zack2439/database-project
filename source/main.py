

def interface():
    print("Welcome to the inventory system.")
    print("1. Add an item")
    print("2. View all items")
    print("3. View Employees")
    print("4. Quit")

    while True:
        command = input("Enter your choice (1-4): ")
        
        if command.lower() == '1':
            # Add item to the inventory with insert into cmd,
            # item must have name, cost, quantity, warehouse, and parts
            print("Please enter the item details:")
            name = input("Name: ")
            cost = float(input("Cost: "))
            quantity = int(input("Quantity: "))
            warehouse = input("Warehouse: ")
            print("Below is a list of parts, select parts by id associated with the item:")
            
            pass

        elif command.lower() == '2':
            # View all items in the inventory, 
            # this will next prompt user to view parts or warehouse of chosen item
            pass

        elif command.lower() == '3':
            # View employee information
            # you can then select an employee to view
            pass

        elif command.lower() == '4':
            print("Exiting the inventory system.")
            break

interface()