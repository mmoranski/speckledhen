# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 15:10:15 2017

@author: Moranski
"""
from flask import Flask, render_template, url_for, request, redirect, flash
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from databasesetup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
session = DBSession()

#%%

@app.route('/')
@app.route('/menus/<int:restaurant_id>/')

def menu(restaurant_id):
    menu = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id)
    return render_template('menu.html', menu = menu, items = items)


    

#%%

# New Menu Item

@app.route('/menus/<int:restaurant_id>/new/', methods=['GET','POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        newItem = MenuItem(name = request.form['name'], description = request.form['description'], course = request.form['course'], price = request.form['price'], restaurant_id = restaurant_id)
        session.add(newItem)
        session.commit()
        flash("new menu item created!")
        return redirect(url_for('menu', restaurant_id = restaurant_id))
    else: 
        return render_template('newmenuitem.html', restaurant_id = restaurant_id)
#%%

# Change name of Menu Item

@app.route('/menus/<int:restaurant_id>/<int:menu_id>/edit/', methods=['GET','POST'])
def editMenuItem(restaurant_id, menu_id):
    editedItem = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        session.add(editedItem)
        if request.form['price']:
            editedItem.price = request.form['price']
        session.add(editedItem)
        if request.form['description']:
            editedItem.description = request.form['description']
        session.add(editedItem)
        session.commit()
        flash(editedItem.name + " changed")
        return redirect(url_for('menu', restaurant_id=restaurant_id))
    else: 
        return render_template('editmenuitem.html', restaurant_id=restaurant_id, menu_id=menu_id, i=editedItem)
#%%

# Edit a price of a menu item

@app.route('/menus/<int:restaurant_id>/<int:menu_id>/edit-price/', methods=['GET','POST'])
def editPriceItem(restaurant_id, menu_id):
    PeditedItem = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        if request.form['price']:
            PeditedItem.price = request.form['price']
        session.add(PeditedItem)
        session.commit()
        flash(PeditedItem.name + " price changed")
        return redirect(url_for('menu', restaurant_id=restaurant_id))
    else: 
        return render_template('editpriceitem.html', restaurant_id=restaurant_id, menu_id=menu_id, i=PeditedItem)

#%%

# Edit a descrption of menu item

@app.route('/menus/<int:restaurant_id>/<int:menu_id>/edit-descr/', methods=['GET','POST'])
def editDescrItem(restaurant_id, menu_id):
    DeditedItem = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        if request.form['description']:
            DeditedItem.description = request.form['description']
        session.add(DeditedItem)
        session.commit()
        flash(DeditedItem.name + " description changed")
        return redirect(url_for('menu', restaurant_id=restaurant_id))
    else: 
        return render_template('editDescritem.html', restaurant_id=restaurant_id, menu_id=menu_id, i=DeditedItem)
    
#%%

# Delete menu Item

@app.route('/menus/<int:restaurant_id>/<int:menu_id>/delete/', methods=['GET','POST'])
def deleteMenuItem(restaurant_id, menu_id):
    itemToDelete = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash("item deleted")
        return redirect(url_for('menu', restaurant_id=restaurant_id))
    else: 
        return render_template('deletemenuitem.html', restaurant_id=restaurant_id, menu_id=menu_id, i=itemToDelete)

    return "Delete Item Page"
#%%

if __name__== '__main__':
    app.secret_key = 'butts'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
