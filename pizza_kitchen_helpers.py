import mysql.connector as conn

def connect_pizza_database():
    db = conn.connect(host="localhost", user="root", passwd="", db="pizza_kitchen")
    cursor = db.cursor()
    return db, cursor

def html_top(title):
    print("""Content-type:text/html\n\n
    <!DOCTYPE html>
    <html lang="en">
        <head>
            <meta charset="utf-8"/>
            <title>{0}</title>
        </head>
        <body>""".format(title))

def html_tail():
    print("""    </body>
    </html>""")
