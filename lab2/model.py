from sqlalchemy import Column, Integer, String, Date, Float, Boolean, ForeignKey, exc
from sqlalchemy.orm import relationship
from config import Session, engine, base
import distutils.util

session = Session()

def connection():
    try:
        base.metadata.create_all(engine)
        print("Successfully CONNECTED to database FLowers")

    except (Exception, exc.DBAPIError) as _ex:
        print("Impossible to CONNECTED to database FLowers\n", _ex)
        session.rollback()

# Definition of classes corresponding to database tables using SQLAlchemy ORM
# Each class represents a table in the database
class Deliveries(base):
            __tablename__ = 'deliveries'

            deliveries_id = Column(Integer, primary_key=True)
            delivery_name = Column(String)
            delivery_phone = Column(String)
            availability = Column(Boolean)

            def __init__(self, delivery_name, delivery_phone, availability, deliveries_id=-1):
                self.delivery_name = delivery_name
                self.delivery_phone = delivery_phone
                self.availability = availability
                if deliveries_id != -1:
                    self.deliveries_id = deliveries_id

            def __repr__(self):
                return "{:^12}{:^20}{:^20}{:^15}".format(self.deliveries_id, self.delivery_name, self.delivery_phone,
                                                         self.availability)

            def __str__(self):
                return f"{'deliveries_id':^12}{'delivery_name':^20}{'delivery_phone':^20}{'availability':^15}"


class Flowers(base):
    __tablename__ = 'flowers'

    flowers_id = Column(Integer, primary_key=True)
    flower_name = Column(String)
    price = Column(Float)
    quantity_in_stock = Column(Integer)

    def __init__(self, flower_name, price, quantity_in_stock, flowers_id=-1):
        self.flower_name = flower_name
        self.price = price
        self.quantity_in_stock = quantity_in_stock
        if flowers_id != -1:
            self.flowers_id = flowers_id

    def __repr__(self):
        return "{:^15}{:^15}{:^15}{:^15}".format(
            self.flowers_id, self.flower_name, self.price, self.quantity_in_stock
        )

    def __str__(self):
        return f"{'flowers_id':^15}{'flower_name':^15}{'price':^15}{'quantity_in_stock':^15}"

class Customers(base):
    __tablename__ = 'customers'

    customers_id = Column(Integer, primary_key=True)
    customer_name = Column(String)
    address = Column(String)
    customer_phone = Column(String)

    def __init__(self, customer_name, address, customer_phone, customers_id=-1):
        self.customer_name = customer_name
        self.address = address
        self.customer_phone = customer_phone
        if customers_id != -1:
            self.customers_id = customers_id

    def __repr__(self):
        return "{:^12}{:^20}{:^20}{:^15}".format(
            self.customers_id, self.customer_name, self.address, self.customer_phone
        )

    def __str__(self):
        return f"{'customers_id':^12}{'customer_name':^20}{'address':^20}{'customer_phone':^15}"


class Orders(base):
    __tablename__ = 'orders'

    orders_id = Column(Integer, primary_key=True)
    order_date = Column(Date)
    order_status = Column(String)
    total_cost = Column(Integer)
    client_id = Column(Integer, ForeignKey('customers.customers_id'))
    courier_id = Column(Integer, ForeignKey('deliveries.deliveries_id'))

    def __init__(self, order_date, order_status, total_cost, client_id, courier_id, orders_id=-1):
        self.order_date = order_date
        self.order_status = order_status
        self.total_cost = total_cost
        self.client_id = client_id
        self.courier_id = courier_id
        if orders_id != -1:
            self.orders_id = orders_id

    def __repr__(self):
        return "{:^12}{:^12}{:^20}{:^15}{:^15}{:^15}".format(
            self.orders_id, self.order_date, self.order_status,
            self.total_cost, self.client_id, self.courier_id
        )

    def __str__(self):
        return f"{'orders_id':^12}{'order_date':^12}{'order_status':^20}{'total_cost':^15}{'client_id':^15}{'courier_id':^15}"

class OrderFlowers(base):
    __tablename__ = 'orderflowers'

    orderflowers_id = Column(Integer, primary_key=True)
    flowers_id = Column(Integer, ForeignKey('flowers.flowers_id'))
    quantity = Column(Integer)

    flower = relationship("Flowers")

    def __init__(self, flowers_id, quantity, orderflowers_id=-1):
        self.flowers_id = flowers_id
        self.quantity = quantity
        if orderflowers_id != -1:
            self.orderflowers_id = orderflowers_id

    def __repr__(self):
        return "{:^15}{:^15}{:^15}".format(
            self.orderflowers_id, self.flowers_id, self.quantity
        )

    def __str__(self):
        return f"{'orderflowers_id':^15}{'flowers_id':^15}{'quantity':^15}"


def insert(choice: int, data: list) -> bool:
    if len(data) < 2:
        return False
    else:
        try:
            if choice == 1:
                elem = Deliveries(*data)
            elif choice == 2:
                elem = Orders(*data)
            elif choice == 3:
                elem = Flowers(*data)
            elif choice == 4:
                elem = OrderFlowers(*data)
            elif choice == 5:
                elem = Customers(*data)
            session.add(elem)
            session.commit()
            print("Successfully INSERTED data into table:")
            print(elem)
            return True
        except (Exception, exc.DBAPIError) as _ex:
            print("Impossible to INSERT data into table\n", _ex)
            session.rollback()
            return False

tables = {
    'deliveries': Deliveries,
    'orders': Orders,
    'flowers': Flowers,
    'customers': Customers,
    'orderFlowers': OrderFlowers,
}
def select_by_key(table: str, key_name: str, key_val: str) -> list:
    try:
        table_obj = tables[table]
        return session.query(table_obj).filter(getattr(table_obj, key_name) == key_val).all()
    except (Exception, exc.DBAPIError) as _ex:
        print(f"Impossible to SELECT data from table {table} by key {key_name}\n", _ex)
        session.rollback()
        return []

def select_by_table(table: str, quantity: str = '100', offset: str = '0') -> list:
    try:
        table_obj = tables[table]
        key_name = table_obj.__tablename__ + '_id'  # Пример получения имени столбца с ID
        return session.query(table_obj).order_by(getattr(table_obj, key_name).asc()).offset(offset).limit(quantity).all()
    except (Exception, exc.DBAPIError) as _ex:
        print(f"Impossible to SELECT data from table {table}. Exception: {_ex}")
        session.rollback()
        return []


def delete(table: str, key_name: str, key_val: str) -> bool:
    try:
        if table == 'deliveries':
            table_obj = Deliveries
        elif table == 'orders':
            table_obj = Orders
        elif table == 'flowers':
            table_obj = Flowers
        elif table == 'orderFlowers':
            table_obj = OrderFlowers
        elif table == 'customers':
            table_obj = Customers

        session.query(table_obj).filter(getattr(table_obj, key_name) == key_val).delete()
        return True
    except (Exception, exc.DBAPIError) as _ex:
        print(f"Impossible to DELETE data from table {table}", _ex)
        session.rollback()
        return False

def update(choice: int, data: list, id1: int, id2: int = 0) -> bool:
    if len(data) < 2:
        return False
    else:
        try:
            if choice == 1:
                session.query(Deliveries).filter_by(deliveries_id=f"{id1}").update(
                    {Deliveries.delivery_name: data[0], Deliveries.delivery_phone: data[1],
                     Deliveries.availability: distutils.util.strtobool(data[2])})
            elif choice == 2:
                 session.query(Orders).filter_by(orders_id=f"{id1}").update(
                {Orders.order_date: data[0], Orders.order_status: distutils.util.strtobool(data[1]), Orders.total_cost: data[2],
                 Orders.client_id: data[3], Orders.courier_id: data[4]})
            elif choice == 3:
                session.query(Flowers).filter_by(flowers_id=f"{id1}").update(
                    {Flowers.flower_name: data[0], Flowers.price: data[1], Flowers.quantity_in_stock: data[2]})
            elif choice == 4:
                session.query(OrderFlowers).filter_by(orderFlowers_id=f"{id1}").update(
                    {OrderFlowers.flowers_id: data[0], OrderFlowers.quantity: distutils.util.strtobool(data[1])})
            elif choice == 5:
                session.query(Customers).filter_by(customers_id=f"{id1}").update(
                    {Customers.customer_name: data[0], Customers.address: data[1], Customers.customer_phone: data[2]})
            session.commit()
            return True
        except Exception as _ex:
            print("Impossible to UPDATE data into table", _ex)
            return False
