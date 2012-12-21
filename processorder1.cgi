#!/usr/local/bin/python3

import cgi
from pizza_kitchen_helpers import *

def process_form(form_data):
	num_pizzas = int(form_data.getvalue("pizza"))
	return num_pizzas
	
def get_available_pizzas(db,cursor):
	sql = "select * from pizza"
	cursor.execute(sql)
	pizzas = cursor.fetchall()
	return pizzas
	
def get_available_sizes(db,cursor):
	sql = "select * from size"
	cursor.execute(sql)
	sizes = cursor.fetchall()
	return sizes

def create_pizza_drop_down(pizzas,name):
	drop_down = """<select name="pizza{0}">""".format(name)
	for each in pizzas:
		drop_down += """<option value="{0}">{1}</option>""".format(each[0],each[1])
	drop_down += "</select>"
	return drop_down
	
def create_size_drop_down(sizes,name):
	drop_down = """<select name="size{0}">""".format(name)
	for each in sizes:
		drop_down += """<option value="{0}">{1}</option>""".format(each[0],each[0])
	drop_down += "</select>"
	return drop_down
	
def create_form(num_pizzas,pizzas,sizes):
	form = """<form method="post" action="processorder2.cgi"/>"""
	for each in range(num_pizzas):
		form += create_pizza_drop_down(pizzas,each)
		form += create_size_drop_down(sizes,each)
		form += "<br/>"
	form += """<input type="submit" name="submit" value="Summarise Order"/>"""
	form += """<input type="hidden" name="quantity" value="{0}"/>""".format(num_pizzas)
	form += "</form>"
	return form

if __name__ == "__main__":
	try:
		html_top("Select Pizzas")
		form_data = cgi.FieldStorage()
		num_pizzas = process_form(form_data)
		db,cursor = connect_pizza_database()
		pizzas = get_available_pizzas(db,cursor)
		sizes = get_available_sizes(db,cursor)
		form = create_form(num_pizzas,pizzas,sizes)
		print("<h1>Pizza Kitchen</h1>")
		print("<h2>Choose Pizza Types and Sizes</h2>")
		print(form)
		cursor.close()
		html_tail()
	except:
		cgi.print_exception()
		
	