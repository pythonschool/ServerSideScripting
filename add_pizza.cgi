#!/usr/local/bin/python3

import cgi
from pizza_kitchen_helpers import *

def get_exisiting_pizzas(db,cursor):
    sql = "select * from pizza"
    cursor.execute(sql)
    pizza = cursor.fetchall()
    return pizza

def create_pizza_form():
    form = """
              <form method="post" action="processpizza.cgi">
                  <table>
                      <tr>
                            <th>Name</th>
                            <th>Cost</th>
                      </tr>
                      <tr>
                            <td><input type="text" name="pizza" placeholder="e.g. Hawaiian"/></td>
                            <td><input type="number" name="cost" min="1" max="6" step="0.1"/></td>
                      </tr>
                      <tr>
                          <td colspan="2">Description</td>
                      </tr>
                      <tr>
                          <td colspan="2">
                            <textarea rows="5" cols="60" name="description" placeholder="e.g. this pizza is topped with ham and pineapple">
                            </textarea>
                          </td>
                      </tr>
                  </table>
                  <input type="submit" name="submit" value="Add new pizza"/>
              </form>"""
    return form

def create_existing_pizza_list(pizzas):
    if len(pizzas) > 0:
        pizza_list = ""

        for existing in pizzas:
            table = """<table>
                  <tr>
                          <th>Name</th>
                          <td>{0}</td>
                        </tr>
                        <tr>
                          <th>Description</th>
                          <td>
                            <textarea rows="5" cols="60">
                            {1}
                            </textarea>
                          </td>
                        </tr>
                        <tr>
                          <th>Cost</th>
                          <td>{2}</td>
                        </tr>
                     </table><br/>""".format(existing[1],existing[2],existing[3])
            pizza_list += table
    else:
        pizza_list = "<p>There are currently no pizzas in the database</p>"

    return pizza_list

if __name__ == "__main__":
    html_top("Add Pizza")
    db,cursor = connect_pizza_database()
    print("<h1>Pizza Kitchen</h1>")
    print("<h2>Add New Pizza</h2>")
    form = create_pizza_form()
    print(form)
    print("<h2>Current Pizzas</h2>")
    pizzas = get_exisiting_pizzas(db,cursor)
    pizza_list = create_existing_pizza_list(pizzas)
    print(pizza_list)
    html_tail()
    cursor.close()

