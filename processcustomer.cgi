#!/usr/local/bin/python3

import cgi
from pizza_kitchen_helpers import *

def process_form(form_data):
	first_name = form_data.getvalue("first")
	last_name = form_data.getvalue("last")
	street = form_data.getvalue("street")
	town = form_data.getvalue("town")
	post_code = form_data.getvalue("postcode")
	email = form_data.getvalue("email")
	return first_name, last_name, street, town, post_code, email
	
def insert_customer(db, cursor,first_name, last_name, street, town, post_code, email):
	sql = """insert into customer 
	      (first_name, last_name, street_address, town, post_code, email_address) 
	      values ('{0}','{1}','{2}','{3}','{4}','{5}')
	      """.format(first_name, last_name, street, town, post_code, email)
	cursor.execute(sql)
	db.commit()

def select_customer(db,cursor,first_name, last_name, post_code):
	sql = """select customer_id
	         from customer
	         where first_name = '{0}' and last_name = '{1}' and post_code = '{2}'
	      """.format(first_name, last_name, post_code)
	cursor.execute(sql)
	customer_id = cursor.fetchall()
	return customer_id[0][0]
	


if __name__ == "__main__":
	try:
		html_top("New Customer Added")
		form_data = cgi.FieldStorage()
		first_name, last_name, street, town, post_code, email = process_form(form_data)
		db,cursor = connect_pizza_database()
		insert_customer(db, cursor,first_name, last_name, street, town, post_code, email)
		customer_id = select_customer(db,cursor,first_name, last_name, post_code)
		print("<h1>Pizza Kitchen</h1>")
		print("<h2>Customer Confirmation</h2>")
		print("<p>Thank you for registering with us. Your customer number is:</p>")
		print("<p><h1>{0}</h1></p>".format(customer_id))
		cursor.close()
		html_tail()
	except:
		cgi.print_exception()

