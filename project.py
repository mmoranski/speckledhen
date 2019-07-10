# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 15:10:15 2017

@author: Moranski
"""
from flask import Flask, session, render_template, url_for, request, redirect, flash
from flask_mysqldb import MYSQL
import MySQLdb.cursors
import re



app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Getpass'
app.config['MYSQL_DB'] = 'menudb'

# Intialize MySQL

mysql = MySQL(app)



#%%

@app.route('/')
@app.route('/menus/<varchar:menu_id>/')

def menu(menu_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT menu_id FROM restaurant WHERE id =%s' ('id'))
    menu = cursor.fetchone()
    cursor.close()
    cursor.execute('SELECT * from menuitems WHERE menu_id =%s' ('menu'))
    items = cursor.fetchone()
    cursor.close()
    items = session.query(menuitems).filter_by(menu_id = menu_id)
    return render_template('menu.html', menu = menu, items = items)

#%%

# New Menu Item

@app.route('/menus/<int:menu_id>/new/', methods=['GET','POST'])
def newMenuItem(menu_id):
    if request.method == 'POST':
            name = request.form['name']
            description = request.form['description']
            course_id = request.form['course_id']
            price = request.form['price']
            menu_id = menu_id
            
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM menuitems WHERE name =%s' ('name'))
            account = cursor.fetchone()
            if account:
                flash("Item already exists!")
            elif not 'name' or not 'price' or not 'description':
                flash("Please fill out the form")
            else:
                cursor.execute('INSERT INTO menuitems VALUES (%s, %s, %s, %s, %s)', ('menu_id', 'course_id', 'price', 'name', 'description'))
                mysql.connection.commit()

                flash("new menu item created!")
                return redirect(url_for('menu', menu_id = menu_id))   
    else: 
            return render_template('newmenuitem.html', menu_id = menu_id)
        
#%%

# Change Menu Items

@app.route('/menus/<int:menu_id>/<varchar:name>/edit/', methods=['GET','POST'])
def editMenuItem(menu_id, name):
# Gets info from the form
    try:
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        course_id = request.form['course_id']
    
        if request.method == 'POST': 
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            # If nots force data entry
            if not 'name' or not 'price' or not 'description' or not 'course_id':
                    flash("Please fill out the form")
            # Updates the database with form data
            else:
                cursor.execute("""
                       UPDATE menuitems 
                       SET name=%s, description=%s, course_id=%s, price=%s
                       WHERE name =%s""",
                       ('name', 'description', 'course_id', 'price'))
                flash(cursor.name + " changed")
                mysql.connection.commit()
                cursor.close()
                # redirects to menu page
                return redirect(url_for('menu', menu_id=menu_id))
        
        else: 
            return render_template('editmenuitem.html', menu_id=menu_id, name=name, i=editedItem)
        
#%%
# Delete menu Item          
@app.route('/menus/<int:restaurant_id>/<varchar:name>/delete/', methods=['GET','POST'])
def deleteMenuItem(name, menu_id):
    if request.method == 'POST':
        delete = mysql.connect()
        cursor = delete.cursor()
        cursor.execute("DELETE FROM menuitems WHERE name=%s", (name, menu_id))
        delete.commit()
        flash('Item deleted successfully!')
        cursor.close()
        delete.close()
        return redirect(url_for('menu', menu_id=menu_id))
    else: 
        return render_template('deletemenuitem.html', menu_id=menu_id, name=name, i=itemToDelete)

#%%

if __name__== '__main__':
    app.secret_key = 'butts'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
