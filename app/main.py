import csv

import psycopg2
from bokeh.embed import file_html
from bokeh.plotting import figure
from bokeh.resources import CDN
from flask import Flask

DB = "postgres"
USER = "user"
PASSWORD = "password"
HOST = "172.28.0.1"
PORT = 8888

try:
    conn = psycopg2.connect(
        database=DB,
        user=USER,
        password=PASSWORD,
        host=HOST,
        port=PORT
    )

    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute('''DROP TABLE IF EXISTS names''')
    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS names (id SERIAL PRIMARY KEY,year INTEGER, name TEXT, number INTEGER, 
        gender TEXT)''')

except psycopg2.Error as error:
    raise Exception(error)

app = Flask(__name__)


def create_year_plot(year, data):
    names = []
    count = []

    for d in data:
        names.append(d[0])
        count.append(d[1])

    p = figure(x_range=names, plot_height=250, title=str(year),
               toolbar_location=None, tools="")
    p.vbar(x=names, top=count, width=0.9)
    p.xgrid.grid_line_color = None
    p.y_range.start = 0

    return file_html(p, CDN, "year plot")


def create_name_plot(name, data):
    years = []
    for i in range(2000, 2020):
        years.append(str(i))

    count = []
    for d in data:
        count.append(d[1])

    p = figure(x_range=years, plot_height=250, title=name,
               toolbar_location=None, tools="")
    p.vbar(x=years, top=count, width=0.9)
    p.xgrid.grid_line_color = None
    p.y_range.start = 0

    return file_html(p, CDN, "name plot")


def fill_database(data_csv):
    with open(data_csv, mode="r") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        next(csv_reader)
        for row in csv_reader:
            try:
                sql = "INSERT INTO names (year, name, number, gender) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql, (row[0], row[1], row[2], row[3]))
            except psycopg2.Error as err:
                print("ERROR:", err)


@app.route("/year/<int:year>/<string:gender>")
def year(year, gender):
    try:
        sql = "SELECT name, number FROM names WHERE (year = %s AND gender = %s)"
        cursor.execute(sql, (year, gender))
    except psycopg2.Error as err:
        print("ERROR:", err)

    data = cursor.fetchall()
    return create_year_plot(year, data)


@app.route("/name/<string:name>/<string:gender>")
def name(name, gender):
    try:
        sql = "SELECT year, number FROM names WHERE (name = %s AND gender = %s)"
        cursor.execute(sql, (name, gender,))
    except psycopg2.Error as err:
        print("ERROR:", err)

    data = cursor.fetchall()
    return create_name_plot(name, data)


if __name__ == "__main__":
    fill_database("data.csv")
    app.run(host="0.0.0.0")
