#/usr/local/bin/python3

import cgi
import mysql.connector as conn

def connect_pizza_database():
    db = conn.connect(host="localhost", user="root", passwd="", db="pizza_kitchen")
    cursor = db.cursor()
    return db, cursor

def create_pizza(db,cursor):
    sql = """create table pizza(
             pizza_id int not null auto_increment,
             name varchar(50) not null,
             description varchar(50) not null,
             cost decimal(5,2),
             primary key(pizza_id))"""
    cursor.execute(sql)
    db.commit()

def create_size(db,cursor):
    sql = """create table size(
             inches int not null,
             cost decimal(5,2),
             primary key(inches))"""
    cursor.execute(sql)
    db.commit()

def create_customer(db,cursor):
    sql = """create table customer(
             customer_id int not null auto_increment,
             first_name varchar(30) not null,
             last_name varchar(50) not null,
             street_address varchar(60) not null,
             town varchar(30) not null,
             post_code varchar(10) not null,
             email_address varchar(30) not null,
             primary key(customer_id))"""

    cursor.execute(sql)
    db.commit()

def create_customer_order(db,cursor):
    sql = """create table customer_order(
             order_id int not null auto_increment,
             date datetime not null,
             delivery_time datetime not null,
             customer_id int not null,
             primary key(order_id),
             foreign key(customer_id) references customer(customer_id)
             on update cascade on delete restrict)"""

    cursor.execute(sql)
    db.commit()

def create_order_item(db,cursor):
    sql = """create table order_item(
             order_item_id int not null auto_increment,
             order_id int not null,
             pizza_id int not null,
             inches int not null,
             quantity int not null,
             primary key(order_item_id),
             foreign key(order_id) references customer_order(order_id)
             on update restrict on delete cascade,
             foreign key(pizza_id) references pizza(pizza_id)
             on update cascade on delete cascade,
             foreign key(inches) references size(inches)
             on update cascade on delete cascade)"""

    cursor.execute(sql)
    db.commit()

if __name__ == "__main__":
    db, cursor = connect_pizza_database()
    create_pizza(db,cursor)
    create_size(db,cursor)
    create_customer(db,cursor)
    create_customer_order(db,cursor)
    create_order_item(db,cursor)
    cursor.close()
