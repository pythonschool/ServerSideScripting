#!/usr/local/bin/python3

import cgi
from pizza_kitchen_helpers import *

def process_form(form_data):
	inches = form_data.getvalue("inches")
	cost = form_data.getvalue("cost")
	return inches, cost
	
def insert_size(db, cursor,inches,cost):
	sql = "insert into size(inches,cost) values('{0}','{1}')".format(inches,cost)
	cursor.execute(sql)
	db.commit()
	


if __name__ == "__main__":
	try:
		html_top("Add Size to Database")
		form_data = cgi.FieldStorage()
		inches, cost = process_form(form_data)
		db,cursor = connect_pizza_database()
		insert_size(db,cursor,inches,cost)
		print("New Size was added successfully")
		cursor.close()
		html_tail()
	except:
		cgi.print_exception()

