#!/usr/local/bin/python3

import cgi
from pizza_kitchen_helpers import *

def get_order_details(db,cursor):
    sql = "select * from customer_order order by order_id desc limit 10"
    cursor.execute(sql)
    orders = cursor.fetchall()
    return orders
    
def get_customer_details(db,cursor,customer_id):
    sql = "select * from customer where customer_id = '{0}'".format(customer_id)
    cursor.execute(sql)
    customer_details = cursor.fetchall()
    return customer_details[0]
    
def get_order_item_details(db,cursor,order_id):
    sql = "select * from order_item where order_id = '{0}'".format(order_id)
    cursor.execute(sql)
    order_items = cursor.fetchall()
    return order_items
    
def get_pizza_names(db,cursor,order_items):
    pizza_names = []
    for each in order_items:
        sql = "select name from pizza where pizza_id='{0}'".format(each[2])
        cursor.execute(sql)
        pizza = cursor.fetchall()
        pizza_names.append(pizza[0][0])
    return pizza_names
    
def create_customer_table(customer_details):
    table = """ <table>
                    <tr>
                        <th>First Name</th>
                        <td>{0}</td>
                    </tr>
                    <tr>
                        <th>Last Name</th>
                        <td>{1}</td>
                    </tr>
                    <tr>
                        <th>Street</th>
                        <td>{2}</td>
                    </tr>
                    <tr>
                        <th>Town</th>
                        <td>{3}</td>
                    </tr>
                    <tr>
                        <th>Post Code</th>
                        <td>{4}</td>
                    </tr>
                    <tr>
                        <th>E-Mail</th>
                        <td>{5}</td>
                    </tr>
                </table>
            """.format(customer_details[1],customer_details[2],customer_details[3],customer_details[4],customer_details[5],customer_details[6])
    return table
    

def create_pizza_table(pizza_names,order_items):

    table = "<table>"
    
    pizza = 0
    for each in order_items:
        table += """
                    <tr>
                        <td>{0} x </td>
                        <td>{1}</td>
                        <td> - {2} inches</td>
                    </tr>
                 """.format(each[4],pizza_names[pizza],each[3])
        pizza += 1
    table += "</table>"
    return table
    
def create_order_table(customer_details,pizza_names,order_items):
    customer_table = create_customer_table(customer_details)
    pizza_table = create_pizza_table(pizza_names,order_items)
    total_cost = calculate_order_cost(order_items)
    
    table = """<table>
                <tr>
                    <th>Customer Details</th>
                    <th>Pizzas</th>
                </tr>
                <tr>
                    <td>{0}</td>
                    <td>{1}</td>
                </tr>
                <tr>
                    <td colspan="2">
                        Order Total = {2}
                    </td>
                </tr>
                </table>""".format(customer_table,pizza_table,total_cost)
    
    return table
    
def calculate_order_cost(order_items):
    total_cost = 0
    
    for each in order_items:
        sql = "select cost from pizza where pizza_id='{0}'".format(each[2])
        cursor.execute(sql)
        pizza_cost = cursor.fetchall()
        pizza_cost = pizza_cost[0][0]
        
        sql = "select cost from size where inches='{0}'".format(each[3])
        cursor.execute(sql)
        size_cost = cursor.fetchall()
        size_cost = size_cost[0][0]
        
        total_cost += (pizza_cost + size_cost) * each[4]
    
    return total_cost
    
def create_recent_order_summary(orders):
    summary = ""
    
    for each in orders:
        customer_details = get_customer_details(db,cursor,each[3])
        order_items = get_order_item_details(db,cursor,each[0])
        pizza_names = get_pizza_names(db,cursor,order_items)
        order_table = create_order_table(customer_details,pizza_names,order_items)
        summary += order_table
        summary += "<br/>"
    
    return summary
        
        
        
    

if __name__ == "__main__":
    try:
        html_top("Recent Orders")
        db,cursor = connect_pizza_database()
        orders = get_order_details(db,cursor)
        summary = create_recent_order_summary(orders)
        print("<h1>Pizza Kitchen</h1>")
        print("<h2>Order Confirmation</h2>")
        print(summary)
    except:
        cgi.print_exception()
        
    