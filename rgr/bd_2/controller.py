import model


def input_data(choice: int) -> list[str]:
    print("Input data separated by comma")
    data = ""
    if choice == 1:
        data = input('Table: deliveries. Input: delivery_name->text, delivery_phone->text, availability->boolean\n')
    elif choice == 2:
        data = input('Table: orders. Input: order_date->date, order_status->text, total_cost->numeric, client_id->int, courier_id->int\n')
    elif choice == 3:
        data = input('Table: flowers. Input: flower_name->text, price->numeric, quantity_in_stock\n')
    elif choice == 4:
        data = input('Table: orderFlowers. Input: flowers_id->int, quantity->int')
    elif choice == 5:
        data = input('Table: customers. Input: customer_name->text, address->text, customer_phone->text\n')
    return data.split(',')


def print_data(nums: list[int], rows):
    d = []
    for num in nums:
        if num == 1:
            d += ['deliveries_id', 'delivery_name', 'delivery_phone', 'availability']
        elif num == 2:
            d += ['orders_id', 'order_date', 'order_status', 'order_cost', 'client_id', 'courier_id']
        elif num == 3:
            d += ['flowers_id', 'flower_name', 'price', 'quantity_in_stock']
        elif num == 4:
            d += ['orderflowers_id', 'flowers_id', 'quantity']
        elif num == 5:
            d += ['customers_id', 'customer_name', 'address', 'customer_phone']

    names = []
    lengths = []
    rules = []
    rls = []
    for dd in d:
        names.append(dd)
        lengths.append(len(dd))
    for col in range(len(lengths)):
        for row in rows:
            rls.append(3 if type(row[col]) is not str else len(row[col]))
        lengths[col] = max([lengths[col]] + rls)
        rules.append("=" * lengths[col])
    format = " ".join(["%%-%ss" % l for l in lengths])
    result = [format % tuple(names), format % tuple(rules)]
    for row in rows:
        result.append(format % row)
    return "\n".join(result) + '\n'


def table_by_choice(choice: int) -> str:
    table = ""
    if choice == 1:
        table = 'deliveries'
    elif choice == 2:
        table = 'orders'
    elif choice == 3:
        table = 'flowers'
    elif choice == 4:
        table = 'orderflowers'
    elif choice == 5:
        table = 'customers'
    return table


def print_request(choice: int, id: str = '', quantity: str = '0', offset: str = '0') -> str:
    if choice <= 0 or choice > 7:
        return ""
    table = table_by_choice(choice)
    if not id:
        if quantity == '0':
            quantity = str(input('Input quantity of rows to print: '))
        rows = model.select_by_table(table, quantity, offset)
    else:
        if choice == 6 or choice == 7:
            rows = model.select_by_key(table, 'flowers_id', id)
        else:
            rows = model.select_by_key(table, table + '_id', id)
    return print_data([choice], rows)


def select_table(flag: bool = False) -> int:
    choice = -1
    if flag == True:
        print ("\n1. Generate data for all tables\n2. Generate data for one table")
        choice = int(input('\nChoose the table: '))
        while choice != 1 and choice != 2:
            choice = int(input('\nError. Choose the table: '))
        if choice == 1:
            choice = 8
    if flag == False or choice == 2:
        print('1. Deliveries\n2. Orders\n3. Flowers\n4. OrderFlowers\n5. Customers\n0. menu')
        choice = int(input('\nChoose the table: '))
    if choice > 8 or choice < 0:
        print('Incorrect number, try one more time')
        if flag == True:
            select_table(True)
        else:
            select_table()
    return choice


def insert_request(choice: int):
    if choice <= 0 or choice > 8:
        return
    rows = [i.strip() for i in input_data(choice)]
    if model.insert(choice, rows):
        print("Data INSERTED successfully")
    else:
        print("Impossible to insert data")


def edit_request(choice: int):
    if choice <= 0 or choice > 7:
        return
    id = input("Enter id of row that you want to UPDATE\n"
               "\'p\' => print rows\n\'r\' => return to menu\n")
    id2 = ""
    if choice == 6 or choice == 7:
        id2 = input("Enter id2 of row that you want to UPDATE\n")
    if id == 'r':
        return
    elif id == 'p':
        offset = '0'
        while True:
            print(print_request(choice, quantity='15', offset=offset))
            id = input("Enter id of row that you want to UPDATE\n"
                        "\'n\' => next 15 rows\n\'b\' => previous 15 rows\n\'r\' => return to menu\n")
            if choice == 6 or choice == 7:
                id2 = input("Enter id2 of row that you want to UPDATE\n")
            if id == 'r':
                return
            elif id == 'n':
                offset = str(int(offset) + 15)
            elif id == 'b':
                offset = str(int(offset) - 15)
            else:
                break
    print_request(choice, id)
    print("If you don't want to UPDATE column -> write as it was")
    columns = input_data(choice)
    if choice == 6 or choice == 7:
        flag = model.update(choice, columns, int(id), int(id2))
    else:
        flag = model.update(choice, columns, int(id))
    if flag:
        print('UPDATED successfully')
    else:
        print("Impossible to UPDATE table")


def delete_request(choice: int):
    if choice <= 0 or choice > 7:
        return
    table = table_by_choice(choice)
    id = input("Enter id of row that you want to DELETE\n"
               "\'p\' => print rows\n\'r\' => return to menu\n")
    if id == 'r':
        return
    elif id == 'p':
        offset = '0'
        while True:
            print(print_request(choice, quantity='15', offset=offset))
            id = input("Enter id of row that you want to DELETE\n"
                       "\'n\' => next 15 rows\n\'b\' => previous 15 rows\n\'r\' => return to menu\n")
            if id == 'r':
                return
            elif id == 'n':
                offset = str(int(offset) + 15)
            elif id == 'b':
                offset = str(int(offset) - 15)
            else:
                break
    if choice == 6 or choice == 7:
        flag = model.delete(table, 'flowers_id', id)
    else:
        flag = model.delete(table, table + '_id', id)
    if flag:
        print('The row DELETED successfully')
    else:
        print("Impossible to DELETE the row")


def generator_request(choice: int):
    if choice <= 0 or choice > 8:
        return
    quantity = int(input('Input the data quantity to GENERATE: '))
    if choice == 8:
        print("Data GENERATED and INSERTED into table category successfully") \
            if model.generate(1, quantity) else print("Impossible to GENERATE and INSERT data into table deliveries")
        print("Data GENERATED and INSERTED into table deliveries successfully") \
            if model.generate(2, quantity) else print("Impossible to GENERATE and INSERT data into table orders")
        print("Data GENERATED and INSERTED into table orders successfully") \
            if model.generate(3, quantity) else print("Impossible to GENERATE and INSERT data into table flowers")
        print("Data GENERATED and INSERTED into table flowers successfully") \
            if model.generate(4, quantity) else print("Impossible to GENERATE and INSERT data into table orderflowers")
        print("Data GENERATED and INSERTED into table orderflowers successfully") \
            if model.generate(5, quantity) else print("Impossible to GENERATE and INSERT data into table customers")
        print("Data GENERATED and INSERTED into table customers successfully")
    elif 0 < choice < 8:
        print(f"Data GENERATED and INSERTED into table number {choice} successfully") \
            if model.generate(choice, quantity) \
            else print(f"Impossible to GENERATE and INSERT data into table number {choice}")


def search_request():
    tables = []
    tab = []
    print('Choose the first table')
    tab.append(select_table())
    tables.append(table_by_choice(tab[0]))
    print('Choose the second table')
    tab.append(select_table())
    tables.append(table_by_choice(tab[1]))
    key = input('Input the connecting key: ')
    print('Input the expression. Use "first" and "second" to address to the table attributes, if with string use like')
    value = input()
    rows = model.search(tables, key, value)
    print("\n", print_data(tab, rows[0]))
    print('Time of the executing program:', rows[1] / 1000, ' ms')


def menu():
    while True:
        print('\n1. INSERT data in table')
        print('2. EDIT data in table')
        print('3. DELETE data from table')
        print('4. PRINT rows')
        print('5. GENERATE random data')
        print('6. SEARCH data from tables')
        print('0. Exit')
        choice = int(input('\t\t\tChoose an option 1-6 or 0: '))
        if choice == 1:
            insert_request(select_table())
        elif choice == 2:
            edit_request(select_table())
        elif choice == 3:
            delete_request(select_table())
        elif choice == 4:
            print("\n", print_request(select_table()))
        elif choice == 5:
            generator_request(select_table(True))
        elif choice == 6:
            search_request()
        elif choice == 0:
            print("")
            return
