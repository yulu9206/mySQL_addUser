from flask import Flask, render_template, request, redirect, session, flash
from mysqlconnection import MySQLConnector
import md5
import os, binascii
app = Flask(__name__)
mysql = MySQLConnector(app,'group_assign') #database name
app.secret_key = 'ThisIsSecret'

@app.route('/users')
def index():
    # query = 'SELECT * FROM groups'
    query = "SELECT id, first_name, last_name, email, DATE_FORMAT(created_at, '%M %d %Y') as new_date FROM groups"
    groups = mysql.query_db(query)

    return render_template('index.html', groups=groups)

@app.route('/users/<id>')
def show(id):
    query = "SELECT id, first_name, last_name, email, DATE_FORMAT(created_at, '%M %d %Y') as new_date FROM groups WHERE id = " + id
    groups_show = mysql.query_db(query)
    return render_template('show.html', groups=groups_show)

@app.route('/users/new')
def add():
    return render_template('add.html')

@app.route('/create', methods=['POST'])
def create():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    print first_name, last_name, email

    query = "INSERT INTO groups (first_name, last_name, email, created_at) VALUES (:first_name, :last_name, :email, NOW())"


    query_data = {'first_name': first_name, 'last_name': last_name, 'email': email}
    mysql.query_db(query, query_data)
    # print 'before query'
    # print mysql.query_db(query, query_data)
    return redirect('/users')

@app.route('/users/<id>/edit')
def edit_page(id):
    # print id
    return render_template('edit.html', id=id)

@app.route('/users/<id>/edit', methods=['POST'])
def edit(id):
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    query = "UPDATE groups SET first_name = :first_name, last_name = :last_name, email = :email, created_at = NOW() WHERE ID = " + id

    query_data = {'first_name': first_name, 'last_name': last_name, 'email': email}

    mysql.query_db(query, query_data)

    return redirect('/users')

@app.route('/delete/<id>', methods=['POST'])
def delete(id):
    query = "DELETE FROM groups WHERE id = :id"
    query_data = {'id': id}
    mysql.query_db(query, query_data)
    return redirect('/users')

app.run(debug = True)
