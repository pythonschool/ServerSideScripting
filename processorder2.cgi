#!/usr/local/bin/python3

import cgi
from pizza_kitchen_helpers import *

def process_form(form_data):
	quantity = int(form_data.getvalue("quantity"))
	pizzas = []
	for each in range(quantity):
		pizza = int(form_data.getvalue("pizza{0}".format(each)))
		size = int(form_data.getvalue("size{0}".format(each)))
		pizzas.append((pizza,size))
	return quantity, pizzas
	
def calculate_pizza_quantities(pizzas):
	different_pizzas = set(pizzas)
	quantities = []
	for each in different_pizzas:
		num_pizza = pizzas.count(each)
		quantities.append((each[0],each[1],num_pizza))
	return quantities
	
def calculate_pizza_costs(db,cursor,quantities):

	costs = []
	
	for each in quantities:
	
		sql = "select cost from pizza where pizza_id='{0}'".format(each[0])
		cursor.execute(sql)
		pizza_cost = cursor.fetchall()
		pizza_cost = pizza_cost[0][0]
		
		
		sql = "select cost from size where inches='{0}'".format(each[1])
		cursor.execute(sql)
		size_cost = cursor.fetchall()
		size_cost = size_cost[0][0]
		
		total_cost = (pizza_cost + size_cost) * each[2]
		costs.append((each[0],each[1],each[2],total_cost))
	
	return costs
	
def get_pizza_name(db,cursor,pizza_id):
	sql = "select name from pizza where pizza_id='{0}'".format(pizza_id)
	cursor.execute(sql)
	pizza_name = cursor.fetchone()
	return pizza_name[0]
	
def calculate_total_order_cost(costs):
	total_cost = 0
	for each in costs:
		total_cost += each[3]
	return total_cost
		
def create_form(db,cursor,costs,quantity):
	form = """<form method="post" action="processorder3.cgi"/>
			<table>
				<tr>
					<th>Pizza</th>
					<th>Size</th>
					<th>Quantity</th>
					<th>Cost</th>
				</tr>
			"""
	orderitem = 0
	for each in costs:
		form += """
				<tr>
					<td><input type="text" name="pizza{0}" value="{1}" readonly /></td>
					<td><input type="text" name="size{0}" value="{2}" readonly /></td>
					<td><input type="text" name="quantity{0}" value="{3}" readonly /></td>
					<td><input type="text" name="cost{0}" value="{4}" readonly /></td>
				</tr>
				""".format(orderitem,get_pizza_name(db,cursor,each[0]),each[1],each[2],each[3])
		orderitem += 1
	form += """
			<tr>
				<td></td>
				<td></td>
				<th>Total Cost</th>
				<td><input type="text" name="total" value="{0}" readonly /></td>
			</tr>
			""".format(calculate_total_order_cost(costs))
	form += "</table><br/>"
	form += """
			<h2>Delivery Time</h2>
			<p>When would you like your pizza delivered</p>
			<br/>
			Date <input type="date" name="date" value="" placeholder="e.g. 2012-12-20"/>
			Time <input type="time" name="time" value="" placeholder="e.g. 10:50" />
			<br/>
			"""
	form += """
			<h2>Customer Information</h2>
			<p><b>Customer Number</b> <input type="number" name="customer" value="" placeholder="e.g. 112"/></p>
			<br/>
			"""
	
	form += """<input type="submit" name="submit" value="Delivery Confirmation"/>"""
	form += """<input type="hidden" name="quantity" value="{0}"/>""".format(quantity)
	form += "</form>"
	return form

if __name__ == "__main__":
	try:
		html_top("Select Pizzas")
		form_data = cgi.FieldStorage()
		quantity, pizzas = process_form(form_data)
		quantities = calculate_pizza_quantities(pizzas)
		db,cursor = connect_pizza_database()
		costs = calculate_pizza_costs(db,cursor,quantities)
		num_pizza_types = len(costs)
		form = create_form(db,cursor,costs,num_pizza_types)
		print("<h1>Pizza Kitchen</h1>")
		print("<h2>Order Summary</h2>")
		print("<p>You have selected the following</p>")
		print(form)
	except:
		cgi.print_exception()
		
	