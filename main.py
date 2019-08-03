# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 11:11:22 2019

@author: Moranski
"""

from flask import Flask, render_template, url_for, request, redirect
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password1'
app.config['MYSQL_DB'] = 'menudb'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route('/')
def users():
    cur = mysql.connection.cursor()
    
    #cur.execute('''INSERT INTO menuitems VALUES (3, 4, '$6', 'test', 'Describing things')''')
    
    #following line prints menuitems table in the root directory
    cur.execute('''SELECT * FROM menuitems''')
    mysql.connection.commit()
    rv = cur.fetchall()
    return str(rv)


@app.route("/<menu_ID>/menu.html")
def menu(menu_ID):
    cur = mysql.connection.cursor()   
    cur.execute('''SELECT * FROM menuitems WHERE menu_ID=(%s)''', (menu_ID,))
    mysql.connection.commit()
    data = cur.fetchall()
    return render_template("menu.html", menu_ID=menu_ID, data=data)

# Adds item to database. Need to update newmenuitem.html to have drop down menu for menu_id and course. 
# Course and menu_ID lists should be populated by the database
    
@app.route("/<menu_ID>/newMenuitem.html", methods=['GET', 'POST'])
def NewItem(menu_ID):
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM restaurant''')
    data = cur.fetchall()
    mysql.connection.commit() 
    
    if request.method == 'POST':
        menu_ID=menu_ID
        name = request.form['name']
        description = request.form['description']
        course_id = request.form['course_id']
        price = request.form['price']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO menuitems (menu_id, course_id, price, name, description) VALUES (%s, %s, %s, %s, %s)", (menu_ID, course_id, price, name, description))
        mysql.connection.commit()
        return redirect(url_for('menu', menu_ID=menu_ID))    
    else:
        return render_template("newMenuitem.html", menu_ID=menu_ID, data=data)

@app.route("/newMenu.html", methods=['GET', 'POST'])
def NewMenu():
    if request.method == 'POST':
        menu_ID = request.form['menu_id']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO restaurant (menu_id) VALUES (%s)", (menu_ID,))
        mysql.connection.commit()
        return redirect(url_for('menu', menu_ID=menu_ID))    
    else:
        return render_template("newMenu.html")

@app.route("/<menu_ID>/<item>/editmenuitem.html", methods=['GET', 'POST'])
# <item> is what editItem will use as item, same goes for menu_ID. 
def editItem(menu_ID, item):
    #Edit item with the given name, identified by unique item_ID called item.
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM menuitems WHERE item_ID=(%s)''', (item,))
    data = cur.fetchall()
    mysql.connection.commit()    

    if request.method == 'POST':     
        name = request.form['name']
        description = request.form['description']
        course_id = request.form['course_id']
        price = request.form['price']
        cur = mysql.connection.cursor()
        cur.execute("UPDATE menuitems SET name=%s, description=%s, course_id=%s, price=%s WHERE item_ID=%s", (name, description, course_id, price, item))
        mysql.connection.commit()
        return redirect(url_for('menu', menu_ID=menu_ID))    
    
    else:
        return render_template("editmenuitem.html", data=data, menu_ID=menu_ID, item_ID=item)

@app.route("/<menu_ID>/<item>/deleteMenuitem.html", methods=['GET', 'POST'])
def deleteItem(menu_ID, item):
    cur = mysql.connection.cursor()
    cur.execute('''SELECT name FROM menuitems WHERE item_ID=(%s)''', (item,))
    data = cur.fetchall()
    mysql.connection.commit()   
    if request.method == 'POST':
         cur = mysql.connection.cursor()
         cur.execute(''' DELETE FROM menuitems WHERE item_ID=(%s)''', (item,))
         mysql.connection.commit()
         return redirect(url_for('menu', menu_ID=menu_ID))  
    else:
        return render_template("deleteMenuItem.html", data=data, menu_ID=menu_ID, item_ID=item)
    
if __name__ == "__main__":
    app.run(debug=True)