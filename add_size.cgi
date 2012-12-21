#!/usr/local/bin/python3

import cgi
from pizza_kitchen_helpers import *

def get_exisiting_sizes(db,cursor):
    sql = "select * from size"
    cursor.execute(sql)
    sizes = cursor.fetchall()
    return sizes

def create_size_form():
    form = """
              <form method="post" action="processsize.cgi">
                  <table>
                      <tr>
                          <th>Number of inches</th>
                          <th>Cost</th>
                      </tr>
                      <tr>
                          <td><input type="text" name="inches" placeholder="e.g. 12"/></td>
                          <td><input type="number" min="1" max="6" step="0.1"/></td>
                      </tr>
                  </table>
                  <input type="submit" name="submit" value="Add new size"/>
              </form>"""
    return form

def create_existing_size_table(sizes):
    if len(sizes) > 0:
        table = """<table>
                      <tr>
                          <th>Number of inches</th>
                          <th>Cost</th>
                      </tr>"""

        for existing in sizes:
            row = """<tr>
                         <td>{0}</td>
                         <td>{1}</td>
                     </tr>""".format(existing[0],existing[1])
            table += row

        table += "</table>"
    else:
        table = "<p>There are currently no sizes in the database</p>"

    return table

if __name__ == "__main__":
    html_top("Add Sizes")
    db,cursor = connect_pizza_database()
    print("<h1>Pizza Kitchen</h1>")
    print("<h2>Current Sizes</h2>")
    current_sizes = get_exisiting_sizes(db,cursor)
    size_table = create_existing_size_table(current_sizes)
    print(size_table)
    print("<h2>Add New Size</h2>")
    new_form = create_size_form()
    print(new_form)
    html_tail()

