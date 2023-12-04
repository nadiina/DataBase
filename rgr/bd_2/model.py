import psycopg2
import time

cursor = None
connection = None


def connect():
    try:
        global cursor, connection
        connection = psycopg2.connect(
            host="localhost",
            user="postgres",
            password="19401944",
            database="postgres",
            port="5432"
        )

        cursor = connection.cursor()

        print("Successfully CONNECTED to database FLowers")

    except Exception as _ex:
        print("Failed CONNECTION to database Flowers", _ex)


def disconnect():
    try:
        cursor.close()
        connection.close()
        print("Successfully DISCONNECTED from database FLowers")
    except Exception as _ex:
        print("Impossible to DISCONNECT from database FLowers", _ex)


def insert(choice: int, data: list) -> bool:
    if connection is None or cursor is None:
        return False
    else:
        try:
            if choice == 1:
                cursor.execute(f"""INSERT INTO public.\"deliveries\" (delivery_name, delivery_phone, availability) \
                                VALUES (\'{data[0]}\', \'{data[1]}\', {data[2]});""")
            elif choice == 2:
                cursor.execute(f"""INSERT INTO public.\"orders\" (order_date, order_status, total_cost, client_id, courier_id) \
                                VALUES (\'{data[0]}\', \'{data[1]}\', {data[2]}, {data[3]}, {data[4]};""")
            elif choice == 3:
                cursor.execute(f"""INSERT INTO public.\"flowers\" (flower_name, price, quantity_in_stock) \
                                VALUES (\'{data[0]}\', \'{data[1]}\', \'{data[2]}\');""")
            elif choice == 4:
                cursor.execute(f"""INSERT INTO public.\"orderflowers\" (flowers_id, quantity) \
                                VALUES (\'{data[0]}\', {data[1]});""")
            elif choice == 5:
                cursor.execute(f"""INSERT INTO public.\"customers\"(customer_name, address, customer_phone) \
                              VALUES (\'{data[0]}\', \'{data[1]}\', \'{data[2]}\');""")
            connection.commit()
        except Exception as _ex:
            print("Impossible to INSERT data into table", _ex)
            return False
    return True


def delete(table: str, key_name: str, key_val: str) -> bool:
    if connection is None or cursor is None:
        return False
    else:
        try:
            cursor.execute(f"""DELETE FROM public.\"{table}\" WHERE {key_name} = \'{key_val}\';""")
            connection.commit()
        except Exception as _ex:
            print(f"Impossible to DELETE data from table {table}", _ex)
            return False
    return True


def select_by_key(table: str, key_name: str, key_val: str) -> list:
    if connection is None or cursor is None:
        return []
    else:
        try:
            cursor.execute(f"""SELECT * FROM public.\"{table}\" WHERE {key_name} = \'{key_val}\';""")
        except Exception as _ex:
            print(f"Impossible to SELECT data from table {table} by key {key_name}", _ex)
            return []
    return cursor.fetchall()


def select_by_table(table: str, quantity: str = '100', offset: str = '0') -> list:
    if connection is None or cursor is None:
        return []
    else:
        try:
            if table == 'room/chambermaid' or table == 'room/guest':
                cursor.execute(f"""SELECT * FROM public.\"{table}\" ORDER BY {"room_id"} \
                                ASC limit {quantity} offset {offset};""")
            else:
                cursor.execute(f"""SELECT * FROM public.\"{table}\" ORDER BY {table + "_id"} \
                                ASC limit {quantity} offset {offset};""")
        except Exception as _ex:
            print(f"Impossible to SELECT data from table {table}", _ex)
            return []
    return cursor.fetchall()


def update(choice: int, data: list, id1: int, id2: int = 0) -> bool:
    if connection is None or cursor is None:
        return False
    else:
        try:
            if choice == 1:
                cursor.execute(f"""UPDATE public.\"deliveries\" SET delivery_name = \'{data[0]}\', \
                    delivery_phone = \'{data[1]}\', availability = {data[2]} WHERE deliveries_id = {id1};""")
            elif choice == 2:
                cursor.execute(f"""UPDATE public.\"orders\" SET order_date = \'{data[0]}\', order_status = \
                    \'{data[1]}\', total_cost = {data[2]}, client_id = {data[3]}, courier_id = {data[4]} WHERE orders_id = {id1};""")
            elif choice == 3:
                cursor.execute(f"""UPDATE public.\"flowers\" SET flower_name = \'{data[0]}\', price = \'{data[1]}\', \
                    quantity_in_stock = \'{data[2]}\' WHERE flowers_id = {id1};""")
            elif choice == 4:
                cursor.execute(f"""UPDATE public.\"orderflowers\" SET flowers_id = \'{data[0]}\', quantity = {data[1]}, \
                    WHERE orderflowers_id = {id1};""")
            elif choice == 5:
                cursor.execute(f"""UPDATE public.\"customers\" SET customer_name = \'{data[0]}\', address = \
                    \'{data[1]}\', customer_phone = {data[2]} WHERE customers_id = {id1};""")
            return True
        except Exception as _ex:
            print("Impossible to UPDATE data into table", _ex)
            return False


def generate(choice: int, count: int) -> bool:
    if connection is None or cursor is None:
        return False
    try:
        for i in range(count):
            if choice == 1:
                cursor.execute(f"""INSERT INTO public.\"deliveries\" (delivery_name, delivery_phone, availability) \
                                VALUES (substr(md5(random()::text), 0, 10), substr(md5(random()::text), 0, 10), \
                                        (round(random())::int)::boolean);""")
            elif choice == 2:
                cursor.execute(f"""INSERT INTO public.\"orders\" (order_date, order_status, total_cost, client_id, courier_id) \
                                SELECT NOW() + (random() * (NOW() - NOW() - '360 days')), \
                                    (substr(md5(random()::character varying(12)), 0, 12)), \
                                    (floor(random() * (25000 - 5000 + 1)) + 5000), \
                                    customers_id, deliveries_id FROM public."customers", public."deliveries" \
                                    order by random() limit 1;""")
            elif choice == 3:
                cursor.execute(f"""INSERT INTO public.\"flowers\" (flower_name, price, quantity_in_stock) \
                                SELECT substr(md5(random()::text), 0, 10), \
                                    (floor(random() * (25000 - 5000 + 1)) + 5000), \
                                    floor(random() * (1000 - 10 + 1) + 10);""")
            elif choice == 4:
                cursor.execute(f"""
                    INSERT INTO public.\"orderflowers\" (flowers_id, quantity)
                    SELECT (flowers_id FROM public."flowers" order by random() limit 1,
                    ( floor(random() * (25000 - 5000 + 1)) + 5000);
                """)
            elif choice == 5:
                cursor.execute(f"""INSERT INTO public.\"customers\" (customer_name, address, customer_phone) \
                                SELECT substr(md5(random()::text), 0, 10), \
                                   substr(md5(random()::text), 0, 10), \
                                   substr(md5(random()::text), 0, 10);""")
        connection.commit()
    except Exception as _ex:
        print("Impossible to GENERATE data to database FLowers", _ex)
        return False
    return True


def search(tables: list[str], key: str, value: str) -> tuple:
    if connection is None or cursor is None:
        return ()
    try:
        request = f"""SELECT * FROM public.\"{tables[0]}\" as first INNER JOIN public.\"{tables[1]}\" as second on first.\"{key}\" = second.\"{key}\" WHERE {value}"""
        print(f"SQL request: {request}")
        start_time = time.time_ns()
        cursor.execute(request)
        rows = cursor.fetchall()
        run_time = time.time_ns() - start_time
    except Exception as _ex:
        print("Impossible to SEARCH data in database FLowers", _ex)
        return ()
    return rows, run_time
