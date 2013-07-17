#!/usr/local/bin/python3

import cgi
from pizza_kitchen_helpers import *

def process_form(form_data):
    pizza = form_data.getvalue("pizza")
    cost = form_data.getvalue("cost")
    description = form_data.getvalue("description")
    return pizza, cost, description
    
def insert_pizza(db, cursor,pizza,cost,description):
    sql = "insert into pizza(name,description,cost) values('{0}','{1}','{2}')".format(pizza,description,cost)
    cursor.execute(sql)
    db.commit()
    


if __name__ == "__main__":
    try:
        html_top("Add Pizza to Database")
        form_data = cgi.FieldStorage()
        pizza, cost, description = process_form(form_data)
        db,cursor = connect_pizza_database()
        insert_pizza(db,cursor, pizza, cost, description)
        print("New Pizza was added successfully")
        cursor.close()
        html_tail()
    except:
        cgi.print_exception()

