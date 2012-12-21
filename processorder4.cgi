#!/usr/local/bin/python3

import cgi
from pizza_kitchen_helpers import *

def process_form(form_data):
	quantity = int(form_data.getvalue("quantity"))
	pizzas = []
	for each in range(quantity):
		pizza = form_data.getvalue("pizza{0}".format(each))
		size = form_data.getvalue("size{0}".format(each))
		num = form_data.getvalue("quantity{0}".format(each))
		pizzas.append((pizza,size,num))
	date = form_data.getvalue("date")
	time = form_data.getvalue("time")
	customer = form_data.getvalue("customer")
	return quantity, pizzas, date, time, customer
	
def add_new_order(db,cursor,quantity, pizzas, date, time, customer):
	sql = """insert into customer_order(date,delivery_time,customer_id) values
			('{0}','{0} {1}:00','{2}')""".format(date,time,customer)
	cursor.execute(sql)
	db.commit()
	
	sql = """select order_id from customer_order where customer_id='{0}' order by order_id desc limit 1""".format(customer)
	cursor.execute(sql)
	order_id = cursor.fetchone()
	order_id = order_id[0]
	
	for each in pizzas:
		sql = """insert into order_item(order_id,pizza_id,inches,quantity) values
				('{0}','{1}','{2}','{3}')""".format(order_id,each[0],each[1],each[2])
		cursor.execute(sql)
	db.commit()
	
	return order_id
	
def get_customer_details(db,cursor,customer_id):
	sql = "select * from customer where customer_id='{0}'".format(customer_id)
	cursor.execute(sql)
	customer_details = cursor.fetchone()
	return customer_details
		
def create_confirmation(quantity, pizzas, cost, date, time, customer_details):
	confirmation = "<p>{0} {1} you are ordering:</p>".format(customer_details[1],customer_details[2])
	confirmation += """
					<table>
						<tr>
							<th>Pizza</th>
							<th>Size</th>
							<th>Quantity</th>
							<th>Cost</th>
						</tr>
					"""
					
	for each in pizzas:
		confirmation += """
						<tr>
							<td>{0}</td>
							<td>{1}</td>
							<td>{2}</td>
							<td>{3}</td>
						</tr>
						""".format(each[0],each[1],each[2],each[3])
	
	confirmation += """
					<tr>
						<td></td>
						<td></td>
						<th>Total Cost</th>
						<td>{0}</td>
					</tr>
					""".format(cost)
	
	confirmation += "</table>"
	
	confirmation += """
					<p>
					To be delivered at {0} on {1} to:
					<ul>
						<li>{2}</li>
						<li>{3}</li>
						<li>{4}</li>
					</ul>
					</p>
					""".format(time, date, customer_details[3],customer_details[4],customer_details[5])
	return confirmation

def get_pizza_id(db,cursor,pizzaname):
	sql = "select pizza_id from pizza where name='{0}'".format(pizzaname)
	cursor.execute(sql)
	name = cursor.fetchone()
	return name[0]
	
def create_form(db, cursor, quantity, pizzas, date, time, customer_id):
	form = """
			<form method="post" action="processorder4.cgi" />
			<input type="hidden" name="customer" value="{0}"/>
			<input type="hidden" name="date" value="{1}"/>
			<input type="hidden" name="time" value="{2}"/>
			<input type="hidden" name="quantity" value="{3}"/>
			""".format(customer_id,date,time,quantity)
	
	orderitem = 0
	for each in pizzas:
		form += """
				<td><input type="hidden" name="pizza{0}" value="{1}" readonly /></td>
				<td><input type="hidden" name="size{0}" value="{2}" readonly /></td>
				<td><input type="hidden" name="quantity{0}" value="{3}" readonly /></td>
				""".format(orderitem, get_pizza_id(db,cursor,each[0]),each[1],each[2])
		orderitem += 1
	
	form += """
			<br/><input type="submit" name="submit" value="Confirm Order"/>
			</form>
			"""
			
	return form	

if __name__ == "__main__":
	try:
		html_top("Order Confirmation")
		form_data = cgi.FieldStorage()
		quantity, pizzas, date, time, customer = process_form(form_data)
		db,cursor = connect_pizza_database()
		order_id = add_new_order(db,cursor,quantity, pizzas, date, time, customer)
		print("<h1>Pizza Kitchen</h1>")
		print("<h2>Order Confirmation</h2>")
		print("<p>Thank you for your order! Your order number is: {0}</p>".format(order_id))
		print("""<p><a href="new_order.html">Another Order?</a></p>""")
	except:
		cgi.print_exception()
		
	